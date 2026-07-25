#!/usr/bin/env node

import { spawnSync } from 'node:child_process'

const allowedAdvisories = new Set([
  'https://github.com/advisories/GHSA-52cp-r559-cp3m',
  'https://github.com/advisories/GHSA-h67p-54hq-rp68'
])
const blockingSeverities = new Set(['high', 'critical'])

const audit = spawnSync('npm', ['audit', '--json'], {
  encoding: 'utf8',
  maxBuffer: 10 * 1024 * 1024,
  shell: false
})

let report
try {
  report = JSON.parse(audit.stdout)
} catch (error) {
  process.stderr.write(audit.stderr)
  throw new Error(`npm audit did not return valid JSON: ${error.message}`)
}

const blocking = []
const accepted = []
for (const vulnerability of Object.values(report.vulnerabilities || {})) {
  if (!blockingSeverities.has(vulnerability.severity)) continue
  const advisoryUrls = vulnerability.via
    .filter((item) => typeof item === 'object')
    .map((item) => item.url)
  const isDocumentedJsYamlException = vulnerability.name === 'js-yaml' &&
    vulnerability.isDirect === false &&
    advisoryUrls.length > 0 &&
    advisoryUrls.every((url) => allowedAdvisories.has(url))
  ;(isDocumentedJsYamlException ? accepted : blocking).push(vulnerability)
}

for (const vulnerability of accepted) {
  process.stderr.write(
    `accepted bounded upstream advisory: ${vulnerability.name} ${vulnerability.range}\n`
  )
}
if (blocking.length) {
  for (const vulnerability of blocking) {
    process.stderr.write(
      `unapproved ${vulnerability.severity} vulnerability: ${vulnerability.name} ${vulnerability.range}\n`
    )
  }
  process.exitCode = 1
} else {
  process.stdout.write('npm audit gate passed; no unapproved high or critical vulnerabilities\n')
}

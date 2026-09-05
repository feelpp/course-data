#!/usr/bin/env node

import { spawnSync } from 'node:child_process'

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

if (audit.error || audit.signal || report.error || !report.vulnerabilities ||
    typeof report.vulnerabilities !== 'object' || ![0, 1].includes(audit.status)) {
  throw new Error('npm audit failed to produce a complete vulnerability report')
}

const blocking = Object.values(report.vulnerabilities)
  .filter((vulnerability) => blockingSeverities.has(vulnerability.severity))
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

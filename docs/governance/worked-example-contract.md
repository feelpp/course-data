# Worked-example authoring and review contract

## Purpose

The course webpage is a primary learning environment, not a catalogue pointing elsewhere. Every canonical worked example must let a student identify the question, understand the mathematics, follow the implementation, inspect the evidence, and state a defensible conclusion without instructor-only material.

This contract applies to all 12 foundation and seven analytical lesson pages. Seventeen examples also generate student notebooks from the same AsciiDoc; the mathematical-background and reproducible-delivery examples remain page-only because transparent hand calculations are the appropriate implementation.

## Required five-part structure

Each `== Worked example` section contains exactly these level-three sections in this order:

1. `Context`
2. `Method`
3. `Implementation`
4. `Results`
5. `Conclusion`

Each section has a stable `worked-<slug>-<part>` ID and a matching `worked-example-<part>` role. Each includes a visible importance statement such as `Essential (P0)` or `Core (P1)`.

### Context

State:

- the stakeholder or research question;
- observational and decision units;
- data provenance and important constraints;
- target quantity, prediction, or decision;
- units and expected scale;
- consequences of a materially wrong answer.

Context is always Essential (P0).

### Method

State:

- mathematical objects and notation;
- the objective, estimator, transformation, invariant, or decision rule;
- assumptions and validity conditions;
- a baseline, oracle, or comparator;
- intermediate hand calculations where they expose the mechanism;
- relevant sources of approximation, estimation, selection, or numerical error.

Method is Essential (P0) for foundational operations and Core (P1) for the principal Master's-level technique.

### Mathematical insight

When a theorem, identity, invariant, optimisation property, stability result, or error relation materially explains the method, it belongs on the lesson page inside `Method`, not only in code comments or instructor notes.

Use a titled `IMPORTANT` block beginning with `Mathematical insight —`. The block must:

- name the insight in operational language;
- state the mathematical property or formula;
- explain why it changes implementation or interpretation;
- state what the property does not guarantee;
- display its importance meaning.

A callout is not valuable merely because it contains notation. It should help a student predict behaviour, reject an invalid method, interpret an error, or transfer the idea to a new setting.

### Implementation

For notebook-backed examples:

- use deterministic, commented Python;
- declare data paths, seeds, split boundaries, and resource budgets;
- compute from reviewed data or a fully declared synthetic case;
- assert invariants and hand-calculated oracles;
- avoid hidden state, undeclared network access, and unbounded output;
- keep preprocessing and selection inside the correct fit boundary;
- generate named evidence used by the result table or figure.

For page-only examples, a complete hand calculation and semantic decision table are preferable to artificial code.

### Results

Present:

- a bounded semantic table, scalar evidence record, or justified figure;
- units, denominators, precision, and tolerance;
- baseline, oracle, or invariant comparison;
- uncertainty or sensitivity when the claim requires it;
- a direct prose statement of what the result shows.

Figures are required only when geometry, distribution, dependence, time, space, or diagnostics carry meaning. They require alternative text, captions, prose interpretation, and redundant non-colour encoding.

### Conclusion

Begin with the answer to the context question. Then state:

- what is observation, estimation, prediction, or decision;
- practical and statistical/numerical significance;
- assumptions actually challenged by the evidence;
- residual measurement, sampling, model, selection, numerical, software, or population-shift error;
- the next validation step and generalisation boundary.

Do not turn association into causation, training fit into future performance, a tolerance into statistical confidence, or one deterministic split into population certainty.

## Page and notebook parity

The AsciiDoc page is canonical. Generated notebooks must preserve:

- the five headings in order;
- the Mathematical insight callout as readable Markdown;
- equations and symbol definitions;
- code-cell order and source;
- table/figure production code;
- transfer tasks and importance meanings.

Student notebooks contain no pre-executed outputs or private solution material. The built webpage embeds reviewed results so that it remains independently teachable.

## Review checklist

A reviewer should be able to answer yes to all of the following:

- Can a student state the question and unit of analysis?
- Is the method distinguishable from its Python implementation?
- Is every important symbol defined?
- Is the valuable mathematical insight visible and explained?
- Does the implementation test an invariant or hand oracle?
- Is every numerical claim traceable to displayed evidence?
- Are units, denominator, baseline, uncertainty, and tolerance present where relevant?
- Does the conclusion answer before qualifying?
- Are residual error and the generalisation boundary explicit?
- Does the notebook preserve the same reasoning chain?
- Can the transfer task be solved by adapting the method rather than copying the result?

Automated checks enforce structure and parity. Instructor mathematical review, accessibility review, and real-student usability review remain human release gates.

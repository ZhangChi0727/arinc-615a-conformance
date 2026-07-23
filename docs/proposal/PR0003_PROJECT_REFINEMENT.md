# Proposal

Repository Refinement

Target

PR #3

Status

Proposal Only

No action shall be taken before PR #2 is merged.

---

# Objective

Improve repository consistency without changing the research methodology.

This proposal intentionally excludes

- probabilistic model
- mathematical model
- verification methodology

All changes are repository-level refinements.

---

# Proposal 1

Terminology

Add

docs/terminology.md

Purpose

Single source of truth for terminology.

Initial entries

Verification Point

Requirement

Requirement Item

Evidence

Oracle

Coverage

Confidence

Conformance

Fault Model

Mutation

Future documents shall reference this file.

Priority

High

---

# Proposal 2

Research Architecture

Add

docs/architecture.md

Content

One complete pipeline

ARINC Specification

↓

Requirement Extraction

↓

Verification Point

↓

Requirement Model

↓

Test Case

↓

Execution

↓

Evidence

↓

Confidence

↓

Conformance

Purpose

Provide one authoritative overview of the research workflow.

Priority

Medium

---

# Proposal 3

Review Process

Add

docs/review/REVIEW_GUIDELINE.md

Define

Repository Review

Engineering Review

Methodology Review

Research Review

Purpose

Standardize future reviews.

Priority

Medium

---

# Proposal 4

Research Decision Log

Add

docs/review/DESIGN_DECISIONS.md

Record important design decisions.

Examples

Why Verification Point

Why Layered DTMC

Why Bayesian Confidence

Why Mutation Analysis

Purpose

Preserve research rationale.

Priority

Medium

---

# Proposal 5

Repository Consistency

Review

README

TRACKS

RESEARCH_OUTLINE

Cross references only.

No structural rewrite.

Priority

Low

---

# Out of Scope

The following topics shall not be addressed in PR #3.

Implementation

Protocol State Machine

Probabilistic Model

Verification Algorithm

Research Questions

Any mathematical redesign

Those topics belong to future PRs.

---

# Expected Result

After PR #3

the repository shall have

- unified terminology
- unified architecture description
- standardized review process
- preserved research rationale

without changing any scientific contribution.
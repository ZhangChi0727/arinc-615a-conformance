# PR #2 Review

Reviewer: ChatGPT (Methodology Review)
Status: Request Changes

---

# Summary

This PR substantially improves the research methodology of the project and
successfully introduces a probabilistic extension for protocol conformance
verification.

The overall methodology is internally consistent and suitable as the basis
of future implementation and publication.

Repository Review:
APPROVED

Engineering Review:
APPROVED

Methodology Review:
REQUEST CHANGES

Research Review:
APPROVED WITH COMMENTS

The requested changes are limited to mathematical rigor and do not require
redesigning the methodology.

---

# Blocking Issues

## M-1 Hidden Markov Model Definition

Severity:
Blocking

Problem

The current document defines θ as the hidden state.

Mathematically this is incorrect.

In an HMM:

Hidden State
    Z_k

Observation
    X_k

Model Parameters
    θ

are three different concepts.

θ cannot simultaneously be the hidden state.

Otherwise Baum-Welch estimation is no longer mathematically well-defined.

Recommendation

Replace

    Hidden State = θ

with

    Hidden State = Z_k

where Z_k denotes the latent implementation conformance state.

Example hidden states

- Conforming
- Retry Fault
- Timeout Fault
- Sequence Fault
- File Integrity Fault

θ shall instead denote

- Transition probabilities
- Emission probabilities
- Initial distribution

Expected Result

The probabilistic model becomes a mathematically valid Hidden Markov Model.

---

## M-2 Confidence Aggregation

Severity:
Blocking

Problem

Current formulation

    C(path)=Πθ_i

implicitly assumes independence.

The methodology never establishes this assumption.

Recommendation

Redefine path confidence as conditional confidence.

Example

C(path)

=

Π P(v_i | v_(i-1))

where

v_i

denotes verification evidence.

The text should explicitly state that confidence is accumulated along the
verification evidence graph instead of multiplying independent probabilities.

Expected Result

Reviewer concern regarding statistical independence is eliminated.

---

## M-3 Weakest Link Metric

Severity:
Blocking

Problem

Protocol confidence is defined as

min θ_i

without justification.

Reviewer will inevitably ask

Why minimum?

Recommendation

Add one paragraph explaining that

the metric is intentionally conservative
and represents a lower bound of protocol confidence.

Mention

Safety Engineering

or

Conservative Assurance Metric.

Expected Result

The metric becomes theoretically justified.

---

# Non-blocking Suggestions

## Bayesian Posterior

Suggested

Posterior

Beta(c+1/2,n-c+1/2)

Posterior Mean

(c+1/2)/(n+1)

Reason

Completes the Bayesian inference chain.

Priority

Low

---

## Mutation Score

Replace

Mutation Score ≈ Diagnostic Coverage

with

Mutation Score is used as an empirical estimator of diagnostic coverage.

Reason

The former is mathematically stronger than justified.

Priority

Low

---

## Conformance Proof

Future work.

Current Definition 5 can later be promoted into a theorem.

No action required for this PR.

---

# Merge Recommendation

After resolving

M-1
M-2
M-3

this PR should be merged without further redesign.

No repository restructuring is recommended within this PR.
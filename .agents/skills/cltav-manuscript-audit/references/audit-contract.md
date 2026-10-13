# Manuscript audit contract

Run only the passes relevant to the request, but report which were applied.

1. **Claim pass:** map each material claim to a project claim ID or explain why
   it is background/context. Flag unsupported strength, causal inflation,
   novelty claims, and scope leakage.
2. **Citation pass:** verify identity, locator, access level, and whether the
   cited proposition supports the exact sentence. Abstract-only evidence must be
   labelled and must not support full-text detail.
3. **Technical consistency pass:** check terminology, symbols, units, algorithm
   duties, interface names, figure/table references, and the declared source
   and model boundaries.
4. **Status pass:** separate planned, implemented, executed, reviewed, and
   approved states. A test pass is not automatically a scientific result.
5. **Language pass:** improve clarity and compression only after the earlier
   passes. Recheck every edited name, number, qualifier, and citation.
6. **Build and render pass:** run the existing manuscript build/check workflow
   when files changed, then inspect the rendered pages for layout regressions.

Use finding categories `BLOCKING`, `MATERIAL`, `EDITORIAL`, and `OPEN-HUMAN`.
`OPEN-HUMAN` includes standard interpretation, boundary screening, authorship,
institutional disclosure, novelty approval, and final scientific approval.

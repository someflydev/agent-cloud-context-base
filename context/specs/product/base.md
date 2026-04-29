---
accb_origin: canonical
accb_source_path: context/specs/product/base.md
accb_role: product
accb_version: 1
---

# Baseline Product Intent

Derived repositories must make their cloud-facing purpose explicit before a
slice is called real. The product statement names the consumer, the trigger
boundary, the expected effect, and the proof that shows the effect crossed the
cloud boundary.

Every meaningful slice answers:

- Who or what consumes the result.
- Which trigger boundary becomes newly true.
- What behavior would count as broken.
- Which validation result proves the slice is real.
- Which cost or quota envelope the slice consumes.

When these answers are missing, implementation is still exploratory. The agent
may build a narrow proof, but completion remains `incomplete` until the product
intent and proof path are both explicit.

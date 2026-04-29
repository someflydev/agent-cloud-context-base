# accb Payload Metadata

Composition rules and payload metadata for derived `.accb/` bundles.
`profile-rules.json` lands in PROMPT_04.

Composition rules are consumed by `scripts/accb_payload.py` in PROMPT_16.
Adding a new doctrine, anchor, archetype, manifest, or support service to the
system requires an entry here so the payload composer can include it in derived
`.accb/` bundles.

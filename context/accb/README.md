# accb Payload Metadata

Composition rules and payload metadata for derived `.accb/` bundles.

`profile-rules.json` is the machine-readable bridge between the context corpus
and generated repo payloads. It declares default doctrine, anchors, routers,
capabilities, manifest capabilities, and support-service capability mappings.

Composition rules are consumed by [`../../scripts/accb_payload.py`](../../scripts/accb_payload.py).
Adding a new doctrine, anchor, archetype, manifest, or support service requires
an entry here so the payload composer can include it in derived `.accb/`
bundles.

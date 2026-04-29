# Specs

Spec modules are canonical narrative layers that become `.accb/specs/*.md` in
derived repositories. The baseline layers are product, architecture, agent, and
evolution, with later prompts adding overlays for archetypes, capabilities,
stacks, doctrine, and routers.

Every non-README spec carries frontmatter so the payload composer can preserve
origin metadata. `scripts/accb_payload.py` lands in PROMPT_16 and consumes these
modules when building derived `.accb/` payloads.

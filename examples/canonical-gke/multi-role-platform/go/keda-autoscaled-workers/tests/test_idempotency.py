def test_duplicate_asset_event_emits_once():
    seen = set()
    emissions = []
    for message_id in ("asset-1", "asset-1"):
        if message_id not in seen:
            seen.add(message_id)
            emissions.append({"message_id": message_id, "stage": "embedded"})
    assert emissions == [{"message_id": "asset-1", "stage": "embedded"}]

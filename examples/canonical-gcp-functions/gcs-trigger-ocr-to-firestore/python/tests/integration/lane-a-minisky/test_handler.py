from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from handler import Clients, handle_gcs_object


class Firestore:
    def __init__(self) -> None:
        self.claimed: set[str] = set()
        self.metadata: dict[str, dict] = {}

    def claim_generation(self, dedupe_key: str, payload: dict) -> bool:
        if dedupe_key in self.claimed:
            return False
        self.claimed.add(dedupe_key)
        return True

    def write_metadata(self, dedupe_key: str, payload: dict) -> None:
        self.metadata[dedupe_key] = payload


class Vision:
    def ocr(self, bucket: str, name: str, generation: str) -> str:
        return f"ocr:{bucket}/{name}@{generation}"


class PubSub:
    def publish(self, topic: str, payload: dict) -> None:
        return None


def main() -> None:
    clients = Clients(Firestore(), Vision(), PubSub())
    result = handle_gcs_object({"id": "evt-local", "data": {"bucket": "docs", "name": "scan.png", "generation": "1"}}, clients)
    assert result["ok"]


if __name__ == "__main__":
    main()

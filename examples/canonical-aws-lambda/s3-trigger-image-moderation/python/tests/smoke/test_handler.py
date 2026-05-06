import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

from handler import Clients, DuplicateObjectVersion, lambda_handler


class Table:
    def __init__(self):
        self.items = {}

    def put_item(self, **kwargs):
        item = kwargs["Item"]
        pk = item["pk"]
        if kwargs.get("ConditionExpression") and pk in self.items:
            raise DuplicateObjectVersion()
        self.items[pk] = item


class Rekognition:
    def detect_labels(self, **kwargs):
        return {"Labels": [{"Name": "Document"}]}

    def detect_moderation_labels(self, **kwargs):
        return {"ModerationLabels": [{"Name": "Explicit Nudity"}]}


class Events:
    def __init__(self):
        self.entries = []

    def put_events(self, **kwargs):
        self.entries.extend(kwargs["Entries"])


class HandlerSmokeTest(unittest.TestCase):
    def test_flags_image_and_emits_event(self):
        table = Table()
        events = Events()
        result = lambda_handler(event("v1"), clients=Clients(table, Rekognition(), events))
        self.assertEqual(result["decision"], "FLAG")
        self.assertEqual(len(table.items), 1)
        self.assertEqual(len(events.entries), 1)


def event(version):
    return {"Records": [{"s3": {"bucket": {"name": "images"}, "object": {"key": "a.jpg", "versionId": version}}}]}


if __name__ == "__main__":
    unittest.main()

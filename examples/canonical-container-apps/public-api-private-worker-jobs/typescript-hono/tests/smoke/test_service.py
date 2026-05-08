import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


class HonoPublicWorkerTests(unittest.TestCase):
    def test_service_exposes_public_worker_and_job_routes(self) -> None:
        source = (ROOT / "src" / "index.ts").read_text()
        self.assertIn("/healthz", source)
        self.assertIn("/readyz", source)
        self.assertIn("/submit", source)
        self.assertIn("/process", source)
        self.assertIn("/retry", source)

    def test_service_documents_azure_boundaries(self) -> None:
        source = (ROOT / "src" / "index.ts").read_text()
        self.assertIn("service-bus", source)
        self.assertIn("key-vault", source)
        self.assertIn("managed-identity", source)
        self.assertIn("keda-servicebus-queue-depth", source)


if __name__ == "__main__":
    unittest.main()

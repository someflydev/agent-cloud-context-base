import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


class DotnetPublicWorkerTests(unittest.TestCase):
    def test_program_exposes_public_worker_and_job_routes(self) -> None:
        program = (ROOT / "src" / "Accb.ContainerApps.PublicWorker" / "Program.cs").read_text()
        self.assertIn("/healthz", program)
        self.assertIn("/readyz", program)
        self.assertIn("/submit", program)
        self.assertIn("/process", program)
        self.assertIn("/retry", program)

    def test_program_documents_azure_boundaries(self) -> None:
        program = (ROOT / "src" / "Accb.ContainerApps.PublicWorker" / "Program.cs").read_text()
        self.assertIn("service-bus", program)
        self.assertIn("key-vault", program)
        self.assertIn("managed-identity", program)
        self.assertIn("keda-servicebus-queue-depth", program)


if __name__ == "__main__":
    unittest.main()

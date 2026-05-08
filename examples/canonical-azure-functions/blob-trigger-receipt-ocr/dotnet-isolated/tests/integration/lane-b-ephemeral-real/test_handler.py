import pathlib
import shutil
import subprocess
import sys

example = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(example))

from tests.smoke.test_handler import process_blob

if shutil.which("dotnet"):
    subprocess.run(
        ["dotnet", "run", "--project", str(example / "tests/smoke/HandlerHarness.csproj")],
        check=True,
    )

assert process_blob("lane-b/receipt.pdf", "real-cloud-etag")["cosmos_document"]["blob_version"] == "real-cloud-etag"
print("lane-b Azure blob receipt ocr dotnet probe passed")

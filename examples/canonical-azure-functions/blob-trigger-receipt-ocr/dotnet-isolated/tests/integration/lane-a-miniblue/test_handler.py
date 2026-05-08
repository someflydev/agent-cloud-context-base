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

assert process_blob("lane-a/receipt.pdf", "azurite-1")["event_grid_event"]["data"]["blob_version"] == "azurite-1"
print("lane-a-miniblue blob receipt ocr dotnet passed")

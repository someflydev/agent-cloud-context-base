import os
import subprocess


ENDPOINT = os.environ.get("MINISTACK_ENDPOINT_URL", "http://localhost:4566")
PREFIX = os.environ.get("ACCB_TEST_PREFIX", "accb-test")


def run_aws(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["aws", "--endpoint-url", ENDPOINT, *args],
        text=True,
        capture_output=True,
        check=False,
    )


def test_ministack_resources_exist_after_bootstrap():
    bucket = run_aws("s3api", "head-bucket", "--bucket", f"{PREFIX}-images-test")
    assert bucket.returncode == 0, bucket.stderr

    table = run_aws("dynamodb", "describe-table", "--table-name", f"{PREFIX}-decisions-test")
    assert table.returncode == 0, table.stderr

    queue = run_aws("sqs", "get-queue-url", "--queue-name", f"{PREFIX}-events-test")
    assert queue.returncode == 0, queue.stderr

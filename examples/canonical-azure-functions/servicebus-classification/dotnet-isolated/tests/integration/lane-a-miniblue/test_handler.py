import pathlib
import sys

example = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(example))

from tests.smoke.test_handler import classify

assert classify("lane-a-msg", "billing issue")["topic"] == "team-billing"
print("lane-a-miniblue servicebus classification passed")

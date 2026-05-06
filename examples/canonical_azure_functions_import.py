from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_python_handler(relative_path: str) -> ModuleType:
    path = Path(__file__).resolve().parents[1] / relative_path
    spec = importlib.util.spec_from_file_location("accb_azure_function_handler", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load handler from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

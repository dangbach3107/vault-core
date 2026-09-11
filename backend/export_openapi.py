"""Export/check the default wire contract, independently of local environment values."""

import argparse
import json
from pathlib import Path

from backend.app.core.config import REPOSITORY_ROOT, Settings
from backend.app.main import create_app

CONTRACT = REPOSITORY_ROOT / "contracts" / "openapi.json"


def contract_text() -> str:
    settings = Settings(
        _env_file=None,
        project_name="VAULT Core",
        version="0.1.0",
        api_v1_str="/api/v1",
        environment="development",
        database_url="",
    )
    return json.dumps(create_app(settings).openapi(), indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = contract_text()
    if args.check:
        if not CONTRACT.exists() or CONTRACT.read_text(encoding="utf-8") != expected:
            raise SystemExit("OpenAPI is stale. Run python -m backend.export_openapi.")
        print("OpenAPI contract is current.")
    else:
        CONTRACT.parent.mkdir(parents=True, exist_ok=True)
        CONTRACT.write_text(expected, encoding="utf-8", newline="\n")
        print(f"Exported {CONTRACT.relative_to(REPOSITORY_ROOT)}")


if __name__ == "__main__":
    main()

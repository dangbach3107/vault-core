"""Start an isolated local PostgreSQL container; preserve existing settings and data."""
import json
import re
import secrets
import shutil
import subprocess

from dotenv import dotenv_values

from backend.app.core.config import REPOSITORY_ROOT


def main():
    root = REPOSITORY_ROOT
    docker = shutil.which("docker")
    if not docker:
        raise SystemExit("Install/start Docker Desktop before running this command.")
    local = root / ".tmp" / "database.json"
    local.parent.mkdir(exist_ok=True)
    if local.exists():
        config = json.loads(local.read_text(encoding="utf-8"))
    else:
        password = secrets.token_hex(24)
        prefix = f"postgresql+psycopg://vault:{password}@127.0.0.1:55432/"
        config = {"password": password, "database_url": prefix + "vault", "test_database_url": prefix + "vault_test"}
        local.write_text(json.dumps(config, indent=2), encoding="utf-8")
    env_file = root / ".tmp" / "database.env"
    env_file.write_text(f"VAULT_LOCAL_DB_PASSWORD={config['password']}\n", encoding="utf-8")
    command = [docker, "compose", "--env-file", str(env_file), "up", "-d", "--wait", "--wait-timeout", "120"]
    result = subprocess.run(command, cwd=root)
    if result.returncode:
        raise SystemExit("PostgreSQL did not start. Check Docker Desktop and port 55432. Existing credentials were preserved.")
    env_path = root / ".env"
    if not env_path.exists():
        shutil.copyfile(root / ".env.example", env_path)
    values = dotenv_values(env_path)
    if not values.get("DATABASE_URL"):
        content = env_path.read_text(encoding="utf-8")
        line = f'DATABASE_URL="{config["database_url"]}"'
        if re.search(r"^DATABASE_URL=.*$", content, flags=re.MULTILINE):
            content = re.sub(r"^DATABASE_URL=.*$", lambda _: line, content, flags=re.MULTILINE)
        else:
            content += "\n" + line + "\n"
        env_path.write_text(content, encoding="utf-8")
        print("Configured the previously empty DATABASE_URL in ignored .env.")
    else:
        print("Preserved the existing DATABASE_URL. Local test database is available separately.")
    print("PostgreSQL is ready on 127.0.0.1:55432. Databases: vault and vault_test.")
    print("Credentials remain in ignored .tmp/database.json and .tmp/database.env. Keep these when restarting the container.")


if __name__ == "__main__":
    main()

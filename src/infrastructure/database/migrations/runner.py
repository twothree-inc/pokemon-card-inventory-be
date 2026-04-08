"""
Migration runner — applies SQL files under migrations/ in version order.

Each file must be named:  <version>_<name>.sql  (e.g. 0001_create_table.sql)
Applied versions are recorded in the _migrations table so each file runs once.
"""

import re
from pathlib import Path

from supabase import Client

MIGRATIONS_DIR = Path(__file__).parents[4] / "migrations"
VERSION_RE = re.compile(r"^(\d+)_(.+)\.sql$")


def _parse(path: Path) -> tuple[str, str] | None:
    """Return (version, name) or None if filename doesn't match."""
    m = VERSION_RE.match(path.name)
    return (m.group(1), m.group(2).replace("_", " ")) if m else None


def _applied_versions(client: Client) -> set[str]:
    try:
        resp = client.table("_migrations").select("version").execute()
        return {row["version"] for row in (resp.data or [])}
    except Exception:
        # Table doesn't exist yet — first-ever run
        return set()


def _execute_sql(client: Client, sql: str) -> None:
    """Run raw SQL via Supabase RPC helper (requires pg_execute or direct REST)."""
    # Supabase Python SDK doesn't expose raw SQL directly; use the rpc approach
    # via a helper function, or split on semicolons and use the table API.
    # For full raw SQL support create a pg_execute RPC in your Supabase project:
    #   CREATE OR REPLACE FUNCTION pg_execute(query text) RETURNS void AS $$
    #   BEGIN EXECUTE query; END; $$ LANGUAGE plpgsql SECURITY DEFINER;
    client.rpc("pg_execute", {"query": sql}).execute()


def run_migrations(client: Client) -> list[str]:
    """Apply all pending migrations. Returns list of applied version strings."""
    applied = _applied_versions(client)
    files = sorted(
        (p for p in MIGRATIONS_DIR.glob("*.sql") if _parse(p)),
        key=lambda p: _parse(p)[0],  # sort by version prefix
    )

    ran: list[str] = []
    for path in files:
        version, name = _parse(path)
        if version in applied:
            continue

        sql = path.read_text(encoding="utf-8").strip()
        _execute_sql(client, sql)

        # Record as applied (skip for the bootstrap migration itself)
        if path.name != "0001_create_migrations_table.sql":
            client.table("_migrations").insert(
                {"version": version, "name": name}
            ).execute()
        else:
            # After the table is created we can insert safely
            _execute_sql(
                client,
                f"INSERT INTO _migrations (version, name) VALUES ('{version}', '{name}') "
                f"ON CONFLICT (version) DO NOTHING",
            )

        ran.append(f"{version} — {name}")
        print(f"  [ok] {version} — {name}")

    return ran


def run_seed(client: Client) -> None:
    """Insert seed data using the Supabase table API (idempotent via upsert)."""
    from src.infrastructure.database.seed_data import seed_all

    seed_all(client)

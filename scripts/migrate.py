#!/usr/bin/env python3
"""
Run pending migrations against the configured Supabase project.

Usage:
    python scripts/migrate.py
"""

import sys
from pathlib import Path

# Allow running from project root without installing the package
sys.path.insert(0, str(Path(__file__).parents[1]))

from src.infrastructure.database.client import get_supabase_client
from src.infrastructure.database.migrations.runner import run_migrations


def main() -> None:
    print("Running migrations...")
    client = get_supabase_client()
    applied = run_migrations(client)
    if applied:
        print(f"\nApplied {len(applied)} migration(s).")
    else:
        print("Nothing to migrate — already up to date.")


if __name__ == "__main__":
    main()

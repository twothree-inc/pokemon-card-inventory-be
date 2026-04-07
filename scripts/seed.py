#!/usr/bin/env python3
"""
Apply seed data to the configured Supabase project.

Usage:
    python scripts/seed.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.infrastructure.database.client import get_supabase_client
from src.infrastructure.database.migrations.runner import run_seed


def main() -> None:
    print("Seeding database...")
    client = get_supabase_client()
    run_seed(client)
    print("Done.")


if __name__ == "__main__":
    main()

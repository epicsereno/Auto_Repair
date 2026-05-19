#!/usr/bin/env bash
set -euo pipefail

db_path="${AUTO_REPAIR_DB:-data/auto_repair.sqlite3}"
backup_dir="data/backups"
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"

if [[ ! -f "$db_path" ]]; then
  printf 'Database not found: %s\n' "$db_path" >&2
  exit 1
fi

mkdir -p "$backup_dir"
backup_path="$backup_dir/auto_repair_${timestamp}.sqlite3"
cp "$db_path" "$backup_path"
printf 'Created database backup: %s\n' "$backup_path"

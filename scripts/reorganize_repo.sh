#!/usr/bin/env bash
set -euo pipefail

mkdir -p config scripts data/raw data/processed data/backups reports/generated reports/templates archives/old_versions

move_if_present() {
  local source="$1"
  local target="$2"

  if [[ -f "$source" && "$source" != "$target" ]]; then
    mkdir -p "$(dirname "$target")"
    mv -n "$source" "$target"
    printf 'Moved %s -> %s\n' "$source" "$target"
  fi
}

move_if_present "daily_market_report.py" "scripts/daily_market_report.py"
move_if_present "market_monitor_config.json" "config/market_monitor_config.json"
move_if_present "turbo-the-tech-dev.log" "archives/old_versions/turbo-the-tech-dev.log"

printf 'Repository reorganization pass complete.\n'

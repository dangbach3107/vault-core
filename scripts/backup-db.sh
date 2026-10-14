#!/usr/bin/env bash
# Dump the PostgreSQL database (profiles, deals, rooms AND uploaded files) to a gzip-compressed SQL file.
# Usage: DATABASE_URL=postgresql://... ./scripts/backup-db.sh [output-dir]
# Needs `pg_dump` at least as new as the server (Neon runs a recent PostgreSQL).
set -euo pipefail

: "${DATABASE_URL:?Set DATABASE_URL (the same value the app uses)}"
OUT_DIR="${1:-backups}"
mkdir -p "$OUT_DIR"

# The app accepts postgresql+psycopg://; pg_dump wants plain postgresql://.
URL="${DATABASE_URL/postgresql+psycopg:/postgresql:}"
FILE="$OUT_DIR/vault-$(date +%Y%m%d-%H%M%S).sql.gz"

pg_dump --no-owner --no-privileges "$URL" | gzip > "$FILE"
echo "Backup written to $FILE ($(du -h "$FILE" | cut -f1))"
echo "Restore into an empty database with:  gunzip -c $FILE | psql \"\$TARGET_DATABASE_URL\""

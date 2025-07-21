#!/bin/bash
set -euo pipefail

LOG_FILE="reports/prime_spiral_log.txt"
MAX_SIZE=1048576  # 1 MB
ARCHIVE_DIR="reports/archive"

mkdir -p "$ARCHIVE_DIR"

if [ -f "$LOG_FILE" ]; then
  FILE_SIZE=$(stat -c%s "$LOG_FILE")
  if [ "$FILE_SIZE" -ge "$MAX_SIZE" ]; then
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    gzip -c "$LOG_FILE" > "$ARCHIVE_DIR/prime_spiral_log_$TIMESTAMP.gz"
    > "$LOG_FILE"  # Truncate the log file
    echo "Log file rotated and compressed to $ARCHIVE_DIR/prime_spiral_log_$TIMESTAMP.gz"
  fi
fi

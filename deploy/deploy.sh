#!/usr/bin/env bash
# Deploy the landing to the Hetzner server via rsync over SSH.
# Usage: deploy/deploy.sh [ssh-host]   (default: estx-bridge from ~/.ssh/config)
# Only git-tracked files are sent; repo tooling is excluded. Files removed
# from git are removed from the server too (--delete).
set -euo pipefail
HOST="${1:-estx-bridge}"
DEST="/var/www/estx.exchange"
cd "$(dirname "$0")/.."

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
git ls-files -z \
  | grep -zvE '^(\.github/|\.gitignore$|\.htaccess$|README\.md$|SETUP-GUIDE\.md$|build-legal\.py$|deploy/)' \
  | rsync -a --from0 --files-from=- ./ "$STAGE/"

rsync -az --delete -e ssh "$STAGE/" "$HOST:$DEST/"
ssh "$HOST" "chown -R www-data:www-data $DEST && find $DEST -type d -exec chmod 755 {} + && find $DEST -type f -exec chmod 644 {} + && nginx -t -q && systemctl reload nginx"
echo "Deployed $(git rev-parse --short HEAD) to $HOST:$DEST"

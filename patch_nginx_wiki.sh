#!/bin/bash
# Patches the live Nginx config on EC2 to add /wiki/ location block.
# Run once on EC2: bash patch_nginx_wiki.sh

set -e

CONF="/etc/nginx/conf.d/gladly.conf"
WIKI_BUILD="/var/www/halo-insight/wiki/build"

echo "==> Checking wiki build dir exists..."
if [ ! -d "$WIKI_BUILD" ]; then
    echo "ERROR: $WIKI_BUILD not found. Run 'cd /var/www/halo-insight/wiki && npm install && npm run build' first."
    exit 1
fi

echo "==> Backing up $CONF..."
cp "$CONF" "${CONF}.bak.$(date +%Y%m%d%H%M%S)"

echo "==> Checking if /wiki/ block already present..."
if grep -q "location /wiki/" "$CONF"; then
    echo "INFO: /wiki/ location block already exists in $CONF — nothing to do."
    nginx -t && systemctl reload nginx
    exit 0
fi

echo "==> Injecting /wiki/ location block before 'location /'..."
# Insert the wiki block before the first "location /" line
sed -i '/^\s*location \/ {/i\
\
    # Wiki — Docusaurus static build\
    location /wiki/ {\
        alias '"$WIKI_BUILD"'/;\
        try_files $uri $uri/ /wiki/index.html;\
        expires 1h;\
        add_header Cache-Control "public, must-revalidate";\
    }\
' "$CONF"

echo "==> Testing Nginx config..."
nginx -t

echo "==> Reloading Nginx..."
systemctl reload nginx

echo "==> Done. https://insight.halocollar.com/wiki/ should now serve the Halo Wiki."

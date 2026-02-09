#!/usr/bin/env bash

URL="https://api.coinbase.com/v2/prices/ETH-USD/spot"
INTERVAL=1   # seconds between requests
COUNT=120    # total requests

for i in $(seq 1 $COUNT); do
  TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
  echo "$TS request=$i status=$STATUS"
  sleep $INTERVAL
done
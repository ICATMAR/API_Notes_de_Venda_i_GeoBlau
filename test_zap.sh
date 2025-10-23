#!/bin/bash

# Executar OWASP ZAP baseline scan
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://host.docker.internal:8000 \
  -r zap_report.html \
  -w zap_report.md

echo "Report generat: zap_report.html"
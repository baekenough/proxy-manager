#!/bin/bash
DOMAIN=$1

# 현재 스크립트의 디렉토리 경로
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 인증서 및 키 파일 경로
SSL_DIR="$PROJECT_ROOT/volumes/ssl"
CERT_FILE="$SSL_DIR/proxy-manager.crt"
KEY_FILE="$SSL_DIR/proxy-manager.key"

# 인증서 및 키 생성
openssl req -newkey rsa:2048 -nodes -keyout "$KEY_FILE" -x509 -days 365 -out "$CERT_FILE" -subj "/CN=$DOMAIN"

echo "SSL certificate and key have been generated for domain: $DOMAIN."

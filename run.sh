#!/bin/bash

set -a
. ./.env
set +a

project_root=$PROJECT_ROOT
main_network=$MAIN_NETWORK_NAME
domain_url=${DOMAIN_URL:-localhost}  # DOMAIN_URL이 공백이거나 설정되지 않은 경우 localhost 사용

# SSL 디렉토리와 파일 경로 설정
ssl_dir="$project_root/volumes/ssl"
cert_file="$ssl_dir/proxy-manager.crt"
key_file="$ssl_dir/proxy-manager.key"

current_date=$(date +%s)

# 인증서 유효기간 확인
check_cert_expiry() {
    if [ -f "$cert_file" ]; then
        cert_expiry_date=$(openssl x509 -enddate -noout -in "$cert_file" | cut -d= -f2)
        cert_expiry_date_seconds=$(date -d "$cert_expiry_date" +%s)
        if [ "$current_date" -ge "$cert_expiry_date_seconds" ]; then
            return 1
        else
            return 0
        fi
    else
        return 1
    fi
}

# 인증서 확인
if ! check_cert_expiry; then
    "$project_root/scripts/generate_certificates.sh" "$domain_url"
fi

if docker network inspect $main_network &>/dev/null; then
    docker network rm $main_network
fi

docker network create --driver bridge $main_network

python3 "$project_root/scripts/python/generate_proxy_conf.py"

envsubst < "$project_root/docker-compose.template.yml" > "$project_root/docker-compose.yml"

docker-compose down
docker-compose up -d

echo "Nginx and services are up and running."

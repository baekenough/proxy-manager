#!/bin/bash

set -a
. ./.env
set +a

# .env 파일에서 프로젝트 위치와 메인 네트워크 이름을 로드합니다
project_root=$PROJECT_ROOT
main_network=$MAIN_NETWORK_NAME

# 모든 Docker Compose 서비스를 중지하고 제거합니다
docker-compose down

# .env에 지정된 메인 네트워크를 제거합니다
if docker network inspect $main_network &>/dev/null; then
    docker network rm $main_network
fi

echo "Nginx and services have been stopped."

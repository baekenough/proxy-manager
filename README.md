# Proxy Manager

## 개요

이 프로젝트는 Nginx 리버스 프록시 설정을 관리하기 위한 스크립트 모음을 포함하고 있습니다.
`proxy.json` 파일을 기반으로 Nginx 설정을 생성하고 Docker Compose를 사용하여 서비스를 관리합니다.

## 요구 사항

- `bash`
- `python3`
- `jq`

## .env 예시
``` sh
PROJECT_ROOT=${PWD}
MAIN_NETWORK_NAME=proxy-manager_network
DOMAIN_URL=your-domain-url
```

## proxy.json 예시

`proxy.json` 파일은 관리할 서비스 목록을 정의합니다. 각 서비스는 `name`, `domain`, `host`, `port`, `use_https` 필드를 포함합니다.

```json
{
    "services": [
        {
            "name": "Nginx main",
            "domain": "proxy-manager.com",
            "host": "",
            "port": "443",
            "use_https": true
        },
        {
            "name": "api-spring",
            "domain": "api.proxy-manager.com",
            "host": "192.168.0.100",
            "port": "8080",
            "use_https": true
        }
    ]
}
```

## 스크립트 사용법

### ./run.sh
 - docker compose 서비스를 시작하고, 필요한 네트워크 연결을 설정합니다.
 - 만약 SSL 인증서가 없거나 유효기간이 경과했다면 인증서를 재생성합니다.

### ./stop.sh
 - Docker Compose 서비스를 중지하고, 네트워크를 정리합니다.

### ./scripts/generate_certificates.sh
 - proxy-manager의 SSL 인증서를 생성합니다.

### ./scripts/manage_proxy.sh
 - 프록시 서비스를 관리하기 위한 인터페이스를 제공합니다.
 - 스크립트를 실행하면 다음과 같은 옵션 메뉴가 나타납니다:

```bash
Proxy Manager
1. List services
2. Add service
3. Remove service
4. Generate proxy configuration
5. Exit
Select an option:
```

1. List services: 현재 proxy.json 파일에 정의된 서비스 목록을 표시합니다.
2. Add service: 새로운 서비스를 추가합니다.
3. Remove service: 기존 서비스를 제거합니다.
4. Generate proxy configuration: Nginx 프록시 설정 파일을 생성합니다.
5. Exit: 스크립트를 종료합니다.

#### 서비스 추가
```bash
Select an option: 2
Service name: New Service
Domain: new.service.com # 가비아, AWS Route 53 등에서 도메인을 구매하거나 외부 아이피를 입력하세요.
Host (blank -> localhost): 192.168.0.101 # 같은 docker network에 있는 서비스가 아니라면 필수로 입력해야 합니다.
Port: 8080
Use HTTPS (Y/N): Y
```
 - 이후 ./scripts/manag_proxy.sh에서 4. Generate proxy configuration를 선택
 - run.sh로 proxy-manager를 재실행하면 proxy.json 파일과 volumes/conf.d/proxy.conf 파일이 업데이트되어 
   Nginx가 새로운 서비스를 프록시할 수 있도록 구성됩니다.
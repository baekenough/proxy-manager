import json
import os
from dotenv import load_dotenv

load_dotenv()

# 현재 작업 디렉토리를 자동으로 감지하여 PROJECT_ROOT로 설정합니다.
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '../..'))

def load_services(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def save_services(json_file, data):
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def list_services(data):
    for i, service in enumerate(data['services']):
        host = service.get('host', 'localhost') or 'localhost'
        print(f"{i + 1}. {service['name']} - {service['domain']} -> {host}:{service['port']} (HTTPS: {service.get('use_https', False)})")

def add_service(json_file):
    data = load_services(json_file)
    name = input("Service name: ")
    domain = input("Domain: ")
    host = input("Host (blank -> localhost): ").strip() or 'localhost'
    port = input("Port: ")
    use_https = input("Use HTTPS (Y/N): ").strip().lower() == 'y'

    new_service = {
        "name": name,
        "domain": domain,
        "host": host,
        "port": port,
        "use_https": use_https
    }

    data['services'].append(new_service)
    save_services(json_file, data)
    print("Service added.")

def remove_service(json_file):
    data = load_services(json_file)
    list_services(data)
    index = int(input("삭제할 서비스의 번호를 입력해주세요.: ")) - 1

    if 0 <= index < len(data['services']):
        removed_service = data['services'].pop(index)
        save_services(json_file, data)
        print(f"Removed service: {removed_service['name']}")
    else:
        print("잘못된 입력입니다.")

def generate_proxy_conf():
    json_file = os.path.join(project_root, 'proxy.json')
    output_file = os.path.join(project_root, 'volumes', 'conf.d', 'proxy.conf')
    with open(json_file, 'r') as f:
        data = json.load(f)

    conf_lines = []

    for service in data['services']:
        name = service['name'].replace(" ", "_")
        domain = service['domain']
        host = service.get('host', 'localhost') or 'localhost'
        port = service['port']
        use_https = service.get('use_https', False)
        scheme = 'https://' if use_https else 'http://'
        target_with_port = f"{host}:{port}"

        server_block = f"""
# {name}
upstream {name} {{
    server {target_with_port};
}}

server {{
    listen 443 ssl;
    server_name {domain};

    ssl_certificate /etc/nginx/ssl/proxy-manager.crt;
    ssl_certificate_key /etc/nginx/ssl/proxy-manager.key;

    location / {{
        proxy_pass {scheme}{target_with_port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
        conf_lines.append(server_block)

    with open(output_file, 'w') as f:
        f.write("\n".join(conf_lines))

if __name__ == "__main__":
    json_file = os.path.join(project_root, 'proxy.json')

    while True:
        print("\nProxy Manager")
        print("1. List services")
        print("2. Add service")
        print("3. Remove service")
        print("4. Generate proxy configuration")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            data = load_services(json_file)
            list_services(data)
        elif choice == '2':
            add_service(json_file)
        elif choice == '3':
            remove_service(json_file)
        elif choice == '4':
            generate_proxy_conf()
        elif choice == '5':
            break
        else:
            print("잘못된 선택입니다. 유효한 옵션 번호를 입력해주세요.")

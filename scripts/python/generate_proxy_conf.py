import json
import os

# 현재 스크립트의 디렉토리 경로
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '../..'))

def generate_proxy_conf(json_file, output_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    conf_lines = []

    for service in data['services']:
        name = service['name'].replace(" ", "_")  # 이름에 공백이 있을 경우 언더스코어로 대체
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
    output_file = os.path.join(project_root, 'volumes', 'conf.d', 'proxy.conf')
    generate_proxy_conf(json_file, output_file)

import json
import requests

WORKER_URL = "https://trending.minixsrv.workers.dev"

try:
    response = requests.get(WORKER_URL, timeout=30)
    response.raise_for_status()
    data = response.json()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Berhasil memperbarui data.json melalui Cloudflare Worker!")

except Exception as e:
    print(f"Error mengambil data dari Worker: {e}")
    exit(1)

import json
import requests

WORKER_URL = "https://trending.minixsrv.workers.dev"

try:
    response = requests.get(WORKER_URL, timeout=30)
    
    # Cetak status dan isi mentah jika bukan status 200 OK
    if response.status_code != 200:
        print(f"Worker Error Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        exit(1)

    data = response.json()

    # Cek jika ada error dari isi JSON Worker
    if "error" in data:
        print(f"Error dari Worker: {data['error']}")
        exit(1)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Berhasil memperbarui data.json!")

except json.decoder.JSONDecodeError:
    print("Error: Respons dari Worker bukan format JSON valid.")
    print("Isi respons yang diterima:", response.text)
    exit(1)
except Exception as e:
    print(f"Error mengambil data: {e}")
    exit(1)

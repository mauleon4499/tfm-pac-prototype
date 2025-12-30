import requests
import time

def calculate_mttd(elastic_url, start_time_epoch):
    # Nota: start_time_iso debe ser formateado adecuadamente en prod
    DETECTION_QUERY = {
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {"request_body": "whoami"}},
                    {"range": {"time_local": {"gte": "now-10m"}}}
                ]
            }
        }
    }
    
    # Cálculo del tiempo de detección
    # (Simulamos un polling)
    print("[*] Consultando SIEM...")
    try:
        res = requests.get(f"{elastic_url}/pac-logs-*/_search", json=DETECTION_QUERY)
        hits = res.json().get("hits", {}).get("hits", [])
        if hits:
            # log_time_unix simulado de la respuesta
            mttd = time.time() - start_time_epoch
            print(f"[RESULTADO] MTTD: {mttd} segundos")
    except Exception as e:
        print(f"[-] Error consultando Elastic: {e}")
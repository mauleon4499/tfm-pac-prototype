import os
import time
import sys
from termcolor import colored
from modules.fuzzing import run_fuzzing_module
from modules.api_abuse import run_api_abuse_module
from modules.ttp_emulation import run_ttp_module
from elastic_reporter import calculate_mttd

TARGET_URL = os.getenv("TARGET_URL", "http://nginx-proxy:80")
ELASTIC_URL = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")

def main():
    print(colored("=== INICIANDO PRUEBAS ADVERSARIALES CONTINUAS (PAC) ===", "cyan"))
    time.sleep(10) # Wait for Nginx
    
    # Ejecución de Módulos
    run_fuzzing_module(TARGET_URL)
    
    # Simulamos tokens para el ejemplo
    run_api_abuse_module(TARGET_URL, user_a_token="eyJhb...", user_b_id="2")
    
    run_ttp_module(TARGET_URL)
    
    # Cálculo de métricas
    calculate_mttd(ELASTIC_URL, time.time())

if __name__ == "__main__":
    main()
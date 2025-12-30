Integración de Red-Team en el SDLC: Prototipo PAC (Pruebas Adversariales Continuas)

Este repositorio contiene el artefacto software desarrollado como parte del Trabajo Fin de Máster (TFM) del Máster Universitario en Ciberseguridad de la UNIR (Universidad Internacional de La Rioja).

Título del TFM: Integración de Red-Team en el SDLC: Extensión práctica a OWASP SAMM y prototipo automatizado
Autor: Sergio Mauleón Cristóbal

Descripción del Proyecto

Este proyecto implementa un prototipo funcional de la metodología PAC (Pruebas Adversariales Continuas). Su objetivo es automatizar la ejecución de ataques simulados (Red Teaming) dentro del ciclo de vida de desarrollo de software (SDLC) para validar la resiliencia de las aplicaciones de forma continua.

A diferencia de las herramientas tradicionales (SAST/DAST), este prototipo se centra en:
1.  Validación de Lógica de Negocio: Detección de fallos complejos como BOLA y BFLA.
2.  Emulación de Adversarios: Ejecución de Tácticas, Técnicas y Procedimientos (TTPs) mapeados a MITRE ATT&CK.
3.  Medición de Detección (Blue Team): Cálculo automático del **MTTD (Mean Time to Detect)** integrándose con un SIEM (ELK Stack).

Arquitectura del Laboratorio

El entorno se despliega mediante Docker Compose simulando una arquitectura DevSecOps completa dividida en tres zonas aisladas:
Objetivo (Target): `juice-shop`, `nginx-proxy` (WAF) --> Aplicación vulnerable OWASP Juice Shop protegida por un WAF simulado que genera logs normalizados.
Ataque (Red Team): `attacker-pac` --> Contenedor efímero basado en Python que orquesta los módulos de ataque y consulta el estado de detección.
Defensa (Blue Team): `elasticsearch`, `logstash`, `kibana` --> Stack ELK para la ingesta de logs, correlación de eventos y cálculo de métricas de resiliencia.

Instalación y Despliegue

Requisitos Previos
- Docker Engine
- Docker Compose

Ejecución Rápida
El prototipo está diseñado para ser desplegado en un solo paso, simulando un pipeline de CI/CD:

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd pac-tfm

# 2. Desplegar la infraestructura y ejecutar las pruebas
docker-compose up --build

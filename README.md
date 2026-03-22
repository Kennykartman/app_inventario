# App Inventario Técnico

Herramienta personal para gestión y control de instalaciones técnicas de seguridad electrónica.

## Descripción
Aplicación desarrollada en Python para registrar y dar seguimiento a clientes, equipos instalados, asignaciones y planes de mantenimiento. Diseñada con principios de POO y acceso remoto seguro vía VPN.

## Tecnologías
- Python 3.12
- PostgreSQL
- psycopg2
- python-dotenv

## Estructura del proyecto
- `models/` — Clases del modelo de datos (Cliente, Equipo, Asignación, Mantenimiento)
- `ui/` — Interfaces de usuario por módulo
- `db.py` — Conexión a base de datos mediante variables de entorno
- `main.py` — Punto de entrada de la aplicación

## Seguridad
Las credenciales de conexión se manejan mediante variables de entorno (`.env`) 
excluidas del repositorio vía `.gitignore`.

## Estado
🚧 En desarrollo activo
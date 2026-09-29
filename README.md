# app-presupuestos

Aplicación de escritorio desarrollada en Python para la gestión comercial y generación automática de presupuestos en PDF.

---

## Características
* Gestión de Presupuestos: Alta, baja, modificación y consulta de presupuestos (ABM).
* Control de Materias Primas: Administración e inventario de insumos y materiales.
* Exportación Automática: Generación de reportes y documentos comerciales en PDF.
* Conexión Dinámica: Configuración y selección de base de datos SQLite.

---

## Tecnologías Utilizadas
* Lenguaje: Python 3.x
* GUI: Tkinter
* Base de Datos: SQLite (`torneria.db`)
* Generación de PDF: ReportLab

---

## Arquitectura del Proyecto (Patrón MVC)

El proyecto está modularizado aplicando el patrón Model-View-Controller (MVC) para separar la lógica de negocio, la interfaz gráfica y el acceso a datos:

### Estructura de Capas
* Modelos (`*modelo.py`): Gestión de la persistencia y consultas SQL a la base de datos SQLite.
* Vistas (`*vista.py`): Interfaces gráficas desarrolladas en Tkinter para la interacción con el usuario.
* Controladores (`*controlador.py`): Lógica de negocio que orquesta la interacción entre vistas y modelos.

### Módulos Principales
| Módulo | Descripción |
| :--- | :--- |
| `principal*.py` | Punto de entrada de la aplicación y navegación general. |
| `abmpresupuestos*.py` / `presupuestos*.py` | Gestión integral de presupuestos (alta, baja, modificación y consulta). |
| `mp*.py` / `mpabm*.py` | Gestión de materias primas e insumos. |
| `pdf.py` | Motor de generación de reportes comerciales en PDF. |
| `seleccionbd.py` | Configuración y conexión dinámica a la base de datos. |

---

## Base de Datos
La base de datos SQLite (`torneria.db`) no se incluye en el repositorio por buenas prácticas de versionado. El sistema ejecuta las sentencias de inicialización (`CREATE TABLE IF NOT EXISTS`) de forma transparente al iniciar la aplicación por primera vez.

---

## Instalación y Ejecución

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/LuppoM/app-presupuestos.git](https://github.com/LuppoM/app-presupuestos.git)
   cd app-presupuestos

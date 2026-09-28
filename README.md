# app-presupuestos
Aplicación de escritorio en Python para gestión comercial y generación automática de presupuestos en PDF.
### Arquitectura del Proyecto (Patrón MVC)

El proyecto está modularizado aplicando el patrón **Model-View-Controller (MVC)** para separar la lógica de negocio, la interfaz gráfica y el acceso a datos:

- **Modelos (`*modelo.py`):** Gestión de la persistencia y consultas SQL a la base de datos SQLite (`torneria.db`).
- **Vistas (`*vista.py`):** Interfaces de usuario desarrolladas en Tkinter para la interacción con el usuario.
- **Controladores (`*controlador.py`):** Lógica de negocio que orquesta la interacción entre las vistas y los modelos.
- **Módulos Principales:**
  - `principal*.py`: Punto de entrada de la aplicación y navegación general.
  - `abmpresupuestos*.py` / `presupuestos*.py`: Módulos para alta, baja, modificación y consulta de presupuestos.
  - `mp*.py` / `mpabm*.py`: Gestión de materias primas e insumos.
  - `pdf.py`: Motor de generación de reportes comerciales en PDF.
  - `seleccionbd.py`: Configuración y conexión dinámica a la base de datos.

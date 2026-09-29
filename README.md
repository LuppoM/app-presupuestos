# Sistema de Gestión de Órdenes de Trabajo (OT)

Sistema de gestión de mantenimiento industrial y trazabilidad operacional diseñado bajo arquitectura **MVC (Model-View-Controller)** para optimizar el control de mantenimiento en planta.

---

##  Tecnologías Utilizadas

- **Lenguaje:** Python
- **Interfaz Gráfica (GUI):** Tkinter
- **Base de Datos:** SQLite / MySQL
- **Generación de Reportes:** ReportLab (exportación dinámica a PDF)
- **Despliegue:** PyInstaller (compilación a ejecutable independiente `.exe`)

---

##  Características Principales

- **Gestión de Órdenes de Trabajo:** Registro, seguimiento y trazabilidad completa de OTs preventivas y correctivas.
- **Control de Mantenimiento:** Organización de tareas por equipo, prioridad y estado.
- **Generación de Reportes:** Creación automática de reportes e informes operacionales en formato PDF.
- **Métricas y KPIs:** Facilita el análisis de tiempos de parada y la recolección de datos para el cálculo de eficiencia (**OEE**).
- **Separación de Responsabilidades:** Código estructurado mediante patrón MVC para garantizar escalabilidad y fácil mantenimiento.

---

##  Arquitectura del Proyecto

```text
├── config/          # Configuraciones y conexión a base de datos
├── controllers/     # Lógica de negocio y controladores
├── models/          # Modelos de datos y consultas SQL
├── views/           # Interfaz de usuario (Tkinter)
├── reports/         # Plantillas y generador de PDF (ReportLab)
├── assets/          # Recursos estáticos (imágenes, íconos)
└── main.py          # Punto de entrada de la aplicación

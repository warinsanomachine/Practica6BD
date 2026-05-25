# Sistema de Gestión de Consultorio Médico 
Equipo:
    
    Flores Vargas Augusto Hazel

    Linares Medina Fernando Agustín

    Hernández Zúñiga Andrea Verónica

    Angeles Salinas Daniel Alejandro

Este proyecto consiste en un sistema para la agendacion de citas en un consultorio medico privado para facilitar el trabajo de los doctores al momento de agendar citas médicas. También ayuda a los administradores a mantener un orden en el registro de los doctores que trabajan en cierta intitución, incluyendo sus respectivas especialidades y horarios de trabajo, pudiendo modificar los registros de manera rápida .Para el paciente, el programa ayuda a pedir la cita médica sin necesidad de hacer una fila presencial, puede ver los horarios y doctores disponibles para la fecha que requiera ser atendido.

El proyecto está completamente contenedorizado utilizando **Docker** y **Docker Compose**, lo que garantiza un despliegue inmediato sin necesidad de configuraciones locales de bases de datos o intérpretes de Python. 

# Resumen de la Base de Datos
El diseño del consultorio médico abarca las siguientes 8 entidades perfectamente normalizadas mediante claves primarias y foráneas rígidas:

├──consultorios
├──especialidad
├──situaciones
├──medicamentos 
├──usuarios 
├──doctores
├──citas 
├──mensajes

---

## 🛠️ Tecnologías Utilizadas

* **Motor de Base de Datos:** PostgreSQL 17 (Alpine)
* **Lenguaje de Programación:** Python 3.10
* **Control de Entorno:** Docker & Docker Compose
* **Librerías Python:** Psycopg2-binary (Driver de conexión a PostgreSQL)

---

## 📂 Estructura del Proyecto

```text
.
├── docker-compose.yml     # Orquestador de servicios (Base de datos y Aplicación)
├── Dockerfile             # Receta de construcción para el contenedor de Python
├── requirements.txt       # Dependencias del sistema de la aplicación
├── .env.example           # Plantilla de variables de entorno (Pública)
├── init.sql               # Script de inicialización (DDL y DML de 105 tuplas)
├── menu.py                # Interfaz de línea de comandos interactiva (CLI)
└── README.md              # Documentación general del proyecto

Requisitos Previos
El único requisito de software para ejecutar este proyecto es tener instalado y en ejecución:
    Docker Desktop (o Docker Engine en entornos Linux).

Instrucciones de Instalación y Despliegue
Sigue estos pasos en orden desde la terminal de tu sistema (asegúrate de estar posicionado en la raíz de la carpeta del proyecto):

    1. Configurar las Variables de Entorno (Seguridad):
Crea una copia del archivo .env.example y renómbrala como .env:
cp .env.example .env
Abre el archivo .env recién creado con tu editor de texto preferido y define tus credenciales personalizadas (el archivo .gitignore evitará que este archivo se suba a GitHub):

Fragmento de código
DB_USER=admin
DB_PASS=tu_contraseña_secreta
DB_NAME=consultorio

    2. Construir y Levantar los Servicios
Para compilar la aplicación por primera vez y descargar las imágenes del motor de base de datos, ejecuta:
docker-compose up -d --build

Este comando descargará PostgreSQL 17, ejecutará de forma automática el script init.sql para crear la base de datos con sus restricciones y llenara la base de datos con 105 registros.

    3. Ejecutar el Menú Interactivo (CLI)
Para interactuar con el sistema y ejecutar las 20 consultas complejas, lanza el contenedor de la aplicación en modo interactivo con el siguiente comando:
docker-compose run --rm app

A partir de este momento, se desplegará un menú numérico en tu terminal donde podrás seleccionar cualquier opción para visualizar simultáneamente su representación en:

1.Álgebra Relacional
2.Cálculo Relacional de Tuplas (CRT)
3.Cálculo Relacional de Dominios (CRD)
4.Sentencia SQL ejecutable con resultados en tiempo real.

Control y Mantenimiento de Contenedores
Para gestionar el ciclo de vida del entorno de contenedores en segundo plano, utiliza los siguientes comandos estándar:

Verificar el estado de los servicios:
docker-compose ps

Pausar el sistema (Detener sin borrar datos):
docker-compose stop

Apagar y limpiar el entorno por completo (Recomendado al finalizar):
docker-compose down

Aquí tienes una versión corregida, estructurada y mejorada de tu archivo `README.md`.

Se corrigieron errores ortográficos (como acentos y errores de dedo), se estandarizó el formato de los comandos utilizando bloques de código adecuados (reemplazando los `=` y `_` que causaban inconsistencias) y se agregó el **Paso 1** en la instalación, ya que el archivo original saltaba directamente al paso 2 omitiendo la configuración del archivo `.env`.

---

```markdown
# Sistema de Gestión de Consultorio Médico

### 👥 Equipo de Desarrollo
* Flores Vargas Augusto Hazel
* Linares Medina Fernando Agustín
* Hernández Zúñiga Andrea Verónica
* Angeles Salinas Daniel Alejandro

---

## 📝 Descripción del Proyecto
Este proyecto consiste en un sistema para la **agendación de citas** en un consultorio médico privado, diseñado para facilitar el trabajo de los doctores al momento de gestionar sus agendas. 

También ayuda a los administradores a mantener un control ordenado en el registro de los médicos que laboran en la institución, incluyendo sus respectivas especialidades y horarios de trabajo, permitiendo modificar los registros de manera rápida y eficiente.

Para el paciente, el programa optimiza el proceso al permitirle solicitar una cita médica sin necesidad de hacer filas de forma presencial; además, puede visualizar los horarios y doctores disponibles para la fecha específica en la que requiera ser atendido.

El proyecto está completamente contenedorizado utilizando **Docker** y **Docker Compose**, lo que garantiza un despliegue inmediato sin necesidad de realizar configuraciones locales de bases de datos o instalar intérpretes de Python.

---

## 🗄️ Resumen de la Base de Datos
El diseño de la base de datos del consultorio médico abarca **8 entidades** perfectamente normalizadas mediante claves primarias y foráneas rígidas:

* ├── `consultorios`
* ├── `especialidad`
* ├── `situaciones`
* ├── `medicamentos`
* ├── `usuarios`
* ├── `doctores`
* ├── `citas`
* ├── `mensajes`

<img width="1214" height="851" alt="image" src="https://github.com/user-attachments/assets/6913928d-29fb-4f95-b693-5dca1e68428c" />

<img width="1128" height="767" alt="image" src="https://github.com/user-attachments/assets/0b0b9726-8dd6-4d6f-9aed-cf32a078d032" />

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

```

---

## 📋 Requisitos Previos

El único requisito de software para ejecutar este proyecto es tener instalado y en ejecución:

* **Docker Desktop** (o Docker Engine en entornos Linux).

---

## 🚀 Instrucciones de Instalación y Despliegue

Sigue estos pasos en orden desde la terminal de tu sistema (asegúrate de estar posicionado en la raíz de la carpeta del proyecto):

### 1. Configurar las Variables de Entorno

Antes de levantar los servicios, crea un archivo `.env` local clonando la plantilla provista en el repositorio:

```bash
cp .env.example .env

```

*(Puedes abrir el archivo `.env` y ajustar las credenciales de la base de datos si lo consideras necesario).*

### 2. Construir y Levantar los Servicios

Para compilar la aplicación por primera vez y descargar las imágenes del motor de base de datos, ejecuta:

```bash
docker-compose up -d --build

```

Este comando descargará PostgreSQL 17, ejecutará de forma automática el script `init.sql` para estructurar las tablas con sus respectivas restricciones y llenará la base de datos con un total de 105 registros.

### 3. Ejecutar el Menú Interactivo (CLI)

Para interactuar con el sistema y ejecutar las 20 consultas complejas, lanza el contenedor de la aplicación en modo interactivo con el siguiente comando:

```bash
docker-compose run --rm app

```

A partir de este momento, se desplegará un menú numérico en tu terminal donde podrás seleccionar cualquier opción para visualizar simultáneamente su representación en:

1. **Álgebra Relacional**
2. **Cálculo Relacional de Tuplas (CRT)**
3. **Cálculo Relacional de Dominios (CRD)**
4. **Sentencia SQL** ejecutable con resultados reflejados en tiempo real.

---

## 🔄 Control y Mantenimiento de Contenedores

Para gestionar el ciclo de vida del entorno de contenedores en segundo plano, utiliza los siguientes comandos estándar:

* **Verificar el estado de los servicios:**
```bash
docker-compose ps

```


* **Pausar el sistema** (Detiene los contenedores temporalmente sin borrar los datos):
```bash
docker-compose stop

```


* **Apagar y limpiar el entorno por completo** (Recomendado al finalizar el uso para liberar recursos del sistema):
```bash
docker-compose down

```



```

```

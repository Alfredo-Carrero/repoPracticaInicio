# Práctica de Docker: Workflow de Desarrollo Python

Este repositorio es una demostración de un entorno de desarrollo profesional basado en Docker para una aplicación web simple con Flask.

El objetivo principal no es la aplicación en sí, sino el **flujo de trabajo (workflow)** que la rodea. Se utiliza Docker y Docker Compose para crear un entorno de desarrollo consistente que incluye testing automatizado con **Pytest**, formateo de código con **Black**, y validaciones automáticas antes de cada commit usando **Git hooks**.

## 🚀 Tecnologías Utilizadas

- **Python 3.11**
- **Flask** (Como aplicación web de ejemplo)
- **Docker & Docker Compose**
- **Pytest** (Para testing)
- **Black** (Para formateo de código)
- **Git** (Hooks `pre-commit`)

---

## 🏁 Puesta en Marcha

Para levantar el entorno de desarrollo, solo necesitas tener **Docker Desktop** y **Git** instalados.

1.  **Clonar el repositorio**

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd repoPracticaInicio
    ```

2.  **Construir la imagen de desarrollo**
    Este comando utiliza `docker-compose.yml` y `Dockerfile.dev` para construir la imagen que contiene todas las dependencias de desarrollo (como `pytest` y `black`).
    `bash
docker compose build dev
`

---

## ⚙️ Comandos del Workflow

Todos los comandos de desarrollo se ejecutan dentro del contenedor `dev` usando `docker compose run`.

### 1. Ejecutar los Tests (Pytest)

Ejecuta la suite de tests definida en la carpeta `tests/`.

```bash
docker compose run --rm -T dev pytest
```

### 2. Verificar el Formato (Black)

Comprueba si el código cumple con las guías de estilo de Black, pero no modifica ningún archivo. Es ideal para integración continua o hooks.

```bash
docker compose run --rm -T dev black --check .
```

### 3. Auto-formatear el Código (Black)

Formatea automáticamente todo el código Python del proyecto para que cumpla con las reglas de Black. Gracias al volumen montado en `docker-compose.yml`, los cambios se reflejarán inmediatamente en tus archivos locales.

```bash
docker compose run --rm -T dev black .
```

### 4. Acceder a una Shell Interactiva

Si necesitas depurar o ejecutar comandos manualmente dentro del contenedor de desarrollo:

```bash
docker compose run --rm dev bash
```

---

## 🤖 Hook Pre-commit

Este proyecto está configurado con un hook `pre-commit` de Git para automatizar la calidad del código.

- **¿Qué hace?** Antes de que Git finalice un `commit`, este script se ejecuta automáticamente.
- **¿Cómo funciona?** El script ejecuta dos comandos:
  1.  `docker compose run ... black --check .` (Verifica el formato)
  2.  `docker compose run ... pytest` (Ejecuta los tests)
- **¿Cuál es el resultado?** Si cualquiera de los dos comandos falla (ya sea por un error de formato o un test roto), el `commit` se **cancela** automáticamente. Esto asegura que solo código funcional y bien formateado llegue al repositorio.

### Instalación del Hook

La carpeta `.git/hooks` no se clona con el repositorio. Para activarlo, debes hacerlo manually:

1.  **Crear el archivo:**

    ```bash
    touch .git/hooks/pre-commit
    ```

2.  **Hacerlo ejecutable:**

    ```bash
    chmod +x .git/hooks/pre-commit
    ```

3.  **Pegar el contenido:**
    Abre el archivo `.git/hooks/pre-commit` y pega el siguiente script:

    ```sh
    #!/bin/sh
    #
    # Hook pre-commit para ejecutar Black y Pytest dentro de Docker.
    # Si cualquier comando falla, el commit se abortará.

    # 1. Asegura que el script falle si un comando falla
    set -e

    # 2. Imprime un mensaje al usuario
    echo "Ejecutando hook pre-commit: Chequeando formato con Black..."

    # 3. Ejecuta Black (el mismo comando que usaste)
    docker compose run --rm -T dev black --check .

    # 4. Imprime un mensaje al usuario
    echo "Ejecutando hook pre-commit: Corriendo tests con Pytest..."

    # 5. Ejecuta Pytest (el mismo comando que usaste)
    docker compose run --rm -T dev pytest

    # 6. Si todo fue bien, permite el commit
    echo "¡Todo correcto! Procediendo con el commit..."
    exit 0
    ```

---

## 📦 Ejecutar la Aplicación (Modo Producción)

Aunque el foco es el desarrollo, también puedes construir y ejecutar la imagen de producción (que usa el `Dockerfile` principal):

1.  **Construir la imagen de producción:**

    ```bash
    docker build -t mi-app:1.0 .
    ```

2.  **Ejecutar el contenedor:**

    ```bash
    docker run --rm -p 8000:8000 mi-app:1.0
    ```

3.  **Verificar en el navegador:**
    Abre `http://localhost:8000` en tu navegador.

---

## 📂 Estructura de Archivos Clave

- `Dockerfile`: Define la imagen de **producción**. Es una imagen limpia solo con lo necesario para _ejecutar_ la app.
- `Dockerfile.dev`: Define la imagen de **desarrollo**. Hereda de la base de Python e instala herramientas adicionales como `pytest` y `black`.
- `docker-compose.yml`: Orquesta el servicio `dev`. Se encarga de construir la imagen `Dockerfile.dev`, montar el código fuente actual (`.`) dentro del contenedor (`/app`) y configurar el `PYTHONPATH`.
- `.dockerignore`: Excluye archivos y carpetas (como `.git`, `venv`, `__pycache__`) del "contexto" de Docker. Esto hace que las _builds_ sean más rápidas y limpias.
- `pytest.ini`: Archivo de configuración para Pytest. Le dice dónde encontrar los tests (`tests`) y qué archivos debe considerar (`test_*.py`).
- `tests/test_app.py`: Contiene los tests de la aplicación.

## 👤 Autor

- **Alfredo Carrero**

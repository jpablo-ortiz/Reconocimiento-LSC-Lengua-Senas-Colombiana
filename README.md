# Reconocimiento LSC Lengua Señas Colombiana

... TODO

---

# Tabla de contenidos

- [Background](#background)
- [Configuración del entorno](#configuración-del-entorno)
- [Uso](#uso)
- [Changelog](#changelog)
- [Administradores](#administradores)
- [Contribuciones](#contribuciones)
- [Seguridad](#seguridad)
- [Licencia](#licencia)

# Background

... TODO

# Configuración del entorno
## Pasos previos
1. Crear archivo .env en la carpeta backend con la siguiente plantilla:
```
# ----------------- Variables -------------------

PYTHONUNBUFFERED = 1
DB_URL = "mongodb://mongo-db/NombreDB"
PATH_DB = "./resources"
SECRET = "SECRET_STRING_TO_ENCODE_TOKEN"

# --------------------- PATHS --------------------

PATH_PREDICTED_IMG = "./LSC_recognizer_model/data/interim/Signs"

PATH_RAW_SIGNS = "./LSC_recognizer_model/data/raw/Signs"
PATH_RAW_NUMPY = "./LSC_recognizer_model/data/processed/Numpy"

PATH_CHECKPOINTS_LOAD = "./LSC_recognizer_model/models/modelo-principal"
PATH_CHECKPOINTS_SAVE = "./LSC_recognizer_model/models/modelo-prueba"
```
## Aclaraciones entorno de ejecución
1. Siempre ejecutar los comandos indicados desde la raíz del proyecto.
2. Para el backend existen dos sistemas para la compilación del código:
    - Docker - Image Tensorflow:
        - Este sistema se debe usar en su mayoría para todos los procesos para la IA, entrenamiento, datos, etc.
    - Env python:
        - Solo usar en caso de problemas o conflictos. Ej: No se detecta las cámaras del pc con OpenCV en Docker.

## Docker
<details>
    <summary>Scripts y comandos para usar docker</summary>

## Uso 🖥️

Aplicación y uso muy sencillos. 😇

Cree y ejecute su docker-compose con el siguiente comando:

```bash
docker compose up
# Para ejecutar en background agregar el comando -d al final
```

Si quiere ingresar al terminal del aplicativo, puede ejecutar el siguiente comando (Tenga en cuenta que se pone el nombre del servicio y no del contenedor):

```bash
docker attach <Nombre-Servicio>
```

## Advertencia 🚨

Si por alguna razón al ejecutar la aplicación obtiene ciertos errores o complicaciónes intente ejecutar uno de los siguientes comandos antes de realizar el "**up**".

```bash
# En el caso de ejecución normal
docker-compose -f docker-compose.yml build
```

</details>

## Env Python

<details>
    <summary style="cursor: pointer; size: 100px;">Scripts y comandos para usar env python</summary>

## Script para generar entorno de python aislado (env) con librerías
Este comando permite generar un entorno de python aislado y cuenta con un parámetro que permite elegir la versión de python que se va a usar.
- Advertencia: En el caso de querer usar una versión de python especifica debe tener en cuenta que esta versión esté instalada en el sistema.

Para windows - powershell ejecutar en la terminal:

```powershell
# Sin parametros (python por defecto en el sistema)
./backend/scripts/crear_env_con_requirements_env_txt.ps1

# Con parametro (python 3.7)
./backend/scripts/crear_env_con_requirements_env_txt.ps1 -pyver 3.7
```

Para linux - bash ejecutar en la terminal:

```bash
# Sin parametros (python por defecto en el sistema)
./backend/scripts/crear_env_con_requirements_env_txt.sh

# Con parametro (python 3.7)
./backend/scripts/crear_env_con_requirements_env_txt.sh 3.7
```

## Script para activar en terminal el entorno de python aislado (env)

Para windows - powershell ejecutar en la terminal:

```powershell
. ./backend/env/Scripts/activate
```

Para linux - bash ejecutar en la terminal:

```bash
. ./backend/env/bin/activate
```

## Script para generar requirements.env.txt con librerías python usadas en el env

Para windows - powershell ejecutar en la terminal:

```powershell
./backend/scripts/generar_requirements_env_txt.ps1
```
Para linux - bash ejecutar en la terminal:

```bash
./backend/scripts/generar_requirements_env_txt.sh
```
</details>


# Uso

... TODO

# Changelog

[Conoce las últimas mejoras y cambios del proyecto](CHANGELOG.MD).

# Administradores

- [@jpablo-ortiz](https://github.com/jpablo-ortiz)
- [@kennethLeonel](https://github.com/kennethLeonel)
- [@camilosan10](https://github.com/camilosan10)
- [@CristianJavierDaCamaraSousa](https://github.com/CristianJavierDaCamaraSousa)

# Contribuciones

Como equipo queremos sentar las bases para el desarrollo de una herramienta capaz de realizar el reconocimiento de señas en entornos reales y cotidianos, por este motivo queremos abrir las puertas a un desarrollo colaborativo y que se puedan hacer contribuciones con ideas, código, etc.

Eres bienvenido aquí <3.

- Si tiene una pregunta, un comentario o un informe de bug para este proyecto, [abra un nuevo issue](https://github.com/jpablo-ortiz/Reconocimiento-LSC-Lengua-Senas-Colombiana/issues).
- Si desea contribuir con código, consulte el archivo [CONTRIBUTING](CONTRIBUCIÓN.md) para obtener más información sobre el entorno de desarrollo.
- Solo te pedimos que seas respetuoso. Lea nuestro [código de conducta](CODE_OF_CONDUCT.md).

# Seguridad

Si encuentra una vulnerabilidad de seguridad en este proyecto o cualquier otra iniciativa relacionada, infórmenos enviando un correo electrónico a tesislscjaveriana@gmail.com o al correo ortizrubio09@gmail.com.

# Licencia

El código de este proyecto es software libre bajo la [BSD 3-Clause "New" or "Revised" License](LICENSE).

---
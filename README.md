# Inicializando entorno
## Aclaraciones
1. Siempre ejecutar los comandos dados desde la raíz del proyecto.
2. Para el backend existen dos sistemas para la compilación del código:
    - Docker - Image Tensorflow:
        - Este sistema se debe usar en su mayoría para todos los procesos para la IA, entrenamiento, datos, etc.
    - Env python:
        - Solo usar en caso de problemas o conflictos. Ej: No se detecta las cámaras del pc con OpenCV en Docker.

## Docker
<details>
    <summary>Scripts y comandos para usar docker</summary>
    <br>

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

## Advertencia ⚠️

Si por alguna razón al ejecutar la aplicación obtiene ciertos errores o complicaciónes intente ejecutar uno de los siguientes comandos antes de realizar el "**up**".

```bash
# En el caso de ejecución normal
docker-compose -f docker-compose.yml build
```

</details>
<br>

## Env Python

<details>
    <summary style="cursor: pointer; size: 100px;">Scripts y comandos para usar env python</summary>
    <br>

## Script para generar entorno de python aislado (env) con paquetes necesarios

Para windows - powershell ejecutar en la terminal:

```powershell
./backend/scripts/crear_env_con_requirements_env_txt.ps1
```
Para linux - bash ejecutar en la terminal:

```bash
./backend/scripts/crear_env_con_requirements_env_txt.sh
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

## Script para generar requirements.env.txt con los paquetes usados en el env

Para windows - powershell ejecutar en la terminal:

```powershell
./backend/scripts/generar_requirements_env_txt.ps1
```
Para linux - bash ejecutar en la terminal:

```bash
./backend/scripts/generar_requirements_env_txt.sh
```
</details>

<!-- Espacio en blanco -->
<br>

---


# Aclaraciones

En este repositorio existen dos sistemas para la compilación del código:
- Docker - Image Tensorflow:
    - Este sistema se debe usar en su mayoría para todos los procesos para la IA, entrenamiento, datos, etc.
- Env python:
    - Solo usar en caso de problemas o conflictos. Ej: No se detecta las cámaras del pc en OpenCV.

# Docker

## Uso 🖥️

Aplicación y uso muy sencillos. 😇

Cree y ejecute su docker-compose con el siguiente comando:

```bash
docker compose -f docker-compose.yml up
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


# Env Python
<details>
<summary style="cursor: pointer; size: 100px;">
Scripts y comandos para usar env de python</summary>
## Script para generar entorno de python aislado (env) con paquetes necesarios

Para windows - powershell ejecutar en la terminal:

```powershell
./scripts/crear_env_con_requirements_env_txt.ps1
```
Para linux - bash ejecutar en la terminal:

```bash
./scripts/crear_env_con_requirements_env_txt.sh
```

## Script para activar 

Para windows - powershell ejecutar en la terminal:

```powershell
. ./env/Scripts/activate
```

Para linux - bash ejecutar en la terminal:

```bash
. ./env/bin/activate
```

## Script para generar requirements.env.txt con los paquetes usados en el env

Para windows - powershell ejecutar en la terminal:

```powershell
./scripts/generar_requirements_env_txt.ps1
```
Para linux - bash ejecutar en la terminal:

```bash
./scripts/generar_requirements_env_txt.sh
```
</details>

<!-- Espacio en blanco -->
<br>

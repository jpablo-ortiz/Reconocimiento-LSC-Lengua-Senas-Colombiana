# Colombian Sign Language (LSC) Recognition

Colombian Sign Language (LSC) recognition system based on the deep learning model of neural networks for the detection and classification of gestures or signs of the hearing impaired communities.

This system is composed of two parts:

1. backend: it is responsible for the detection and classification of gestures or signs of the hearing impaired communities and for managing the user interaction with the technical concepts such as models, model training, new sign registration, versioning, and sign prediction. 
   
   This is orchestrated with the Python framework [FastAPI](https://fastapi.tiangolo.com/) for the creation of a RESTful API; and with the NoSQL database ([TinyDB](https://tinydb.readthedocs.io/en/latest/)), and the storage folders for models and signs.

2. Frontend: it is in charge of the interaction of the non-technical user with the system, either to translate signs to text and/or voice, or to register new signs in the system. This is orchestrated with the [Angular] framework (https://angular.io/) for the creation of a web application.

The project aims to be a fully functional and usable application in everyday cases of interaction with communities that make use of LSC, but the project being a deliverable of university thesis work is in **alpha state** and to achieve the goal of stable productive system requires the [contribution](#contributions) of the developer community for the implementation of new features and bug fixes, using quality standards and good development practices. [More Information](#contributions).

---

# Table of Contents

- Background](#background)
- [Environment Configuration](#environment-configuration)
- Usage](#usage)
- Changelog](#changelog)
- Administrators](#administrators)
- Contributions](#contributions)
- Security](#security)
- License](#license)

# Background

This project aims to provide the hearing impaired community and the different parties that want to continue with the development of the system to be carried out, an implementation capable of providing interpretation of the signs present in the LSC, however, it is necessary to supplement the database of the lexicon of this language, Therefore, the different actors such as people and institutions interested, are given the opportunity to help increase the extensibility of the signs intuitively coming to have the innovation of new projects in which the promotion of social inclusion of the deaf population in our society is developed or takes place. 

The project fundamentally needs volumes of data, in this case images, videos for the previous obtaining of information such as the different signs of the LSC that allow us to train the unstructured data through the use of machine learning techniques such as training models, mainly neural networks. In this way, our system will be able to classify and clearly show the meaning of the sign made and that eventually we can offer an efficient and applicable system in various social and state aspects where it is possible to reduce the communication gap between people with hearing impairment and those who do not.  

## Environment configuration
## Previous steps
1. Create .env file in the backend folder with the following template:
```
# ----------------- Variables -------------------

PYTHONUNBUFFERED = 1
DB_URL = "mongodb://mongo-db/NombreDB".
PATH_DB = "./resources"
SECRET = "SECRET_STRING_TO_ENCODE_TOKEN"

# --------------------- PATHS --------------------

PATH_PREDICTED_IMG = "./LSC_recognizer_model/data/interim/Signs"

PATH_RAW_SIGNS = "./LSC_recognizer_model/data/raw/Signs"
PATH_RAW_NUMPY = "./LSC_recognizer_model/data/processed/Numpy"

PATH_CHECKPOINTS_LOAD = "./LSC_recognizer_model/models/model-principal"
PATH_CHECKPOINTS_SAVE = "./LSC_recognizer_model/models/model-processed."
```
## Clarifications execution environment
1. Always execute the indicated commands from the root of the project.
2. For the backend there are two systems for code compilation:
    - Docker - Image Tensorflow:
        - This system should mostly be used for all processes for AI, training, data, etc.
    - Env python:
        - Only use in case of problems or conflicts. Ex: No detection of pc cameras with OpenCV in Docker.

## Docker
<details>
    <summary>Scripts and commands to use docker</summary>.
  
  ## Use 🖥️

Very easy application and use. 😇

Create and run your docker-compose with the following command:

````bash
docker compose up
# To run in background add the -d command at the end.
```

If you want to enter the terminal of the application, you can run the following command (Note that you put the name of the service and not the container):

````bash
docker attach <Service-Name>
```
  
 ## Warning 🚨

If for some reason when running the application you get certain errors or complications try running one of the following commands before performing the "**up**".

````bash
# In the case of normal execution
docker-compose -f docker-compose.yml build
```

</details>

## Env Python

<details>
    <summary style="cursor: pointer; size: 100px;">Scripts and commands to use env python</summary>.

## Script to generate isolated python environment (env) with libraries.
This command allows you to generate an isolated python environment and has a parameter that allows you to choose the python version to use.
- Warning: In case you want to use a specific python version you must make sure that this version is installed on the system.

For windows - powershell run in the terminal:

```powershell
# No parameters (default python on the system)
./backend/scripts/create_env_with_requirements_env_txt.ps1

# With parameter (python 3.7)
./backend/scripts/create_env_with_requirements_env_txt.ps1 -pyver 3.7
```
  
  For linux - bash run in the terminal:

````bash
# No parameters (python default on system)
./backend/scripts/create_env_with_requirements_env_txt.sh

# With parameter (python 3.7)
./backend/scripts/create_env_with_requirements_env_txt.sh 3.7
```

## Script to activate in terminal the isolated python environment (env)

For windows - powershell run in terminal:

````powershell
. ./backend/env/Scripts/activate
```

For linux - bash run in terminal:

````bash
. ./backend/env/bin/activate
```

## Script to generate requirements.env.txt with python libraries used in the env

For windows - powershell run in terminal:
  
  ````powershell
./backend/scripts/generate_requirements_env_txt.ps1
```
For linux - bash run in terminal:

````bash
./backend/scripts/generate_requirements_env_txt.sh
```
</details>


# Usage

~~ COMING SOON ~~

# Changelog

[Learn about the latest improvements and changes to the project](CHANGELOG.MD).

# Administrators

- [@jpablo-ortiz](https://github.com/jpablo-ortiz)
- [@kennethLeonel](https://github.com/kennethLeonel)
- [@camilosan10](https://github.com/camilosan10)
- [@CristianJavierDaCamaraSousa](https://github.com/CristianJavierDaCamaraSousa)
  
  # Contributions

As a team we want to lay the groundwork for the development of a tool capable of performing sign recognition in real and everyday environments, for this reason we want to open the doors to a collaborative development and that you can make contributions with ideas, code, etc.

You are welcome here <3.

- If you have a question, comment or bug report for this project, [open a new issue](https://github.com/jpablo-ortiz/Reconocimiento-LSC-Lengua-Senas-Colombiana/issues).
- If you would like to contribute code, see the [CONTRIBUTING](CONTRIBUTING.md) file for more information about the development environment.
- We only ask that you be respectful. Read our [code of conduct](CODE_OF_CONDUCT.md).

# Security

If you find a security vulnerability in this project or any other related initiative, please inform us by sending an email to tesislscjaveriana@gmail.com or email ortizrubio09@gmail.com.

# License

The code in this project is free software under the [BSD 3-Clause "New" or "Revised" License](LICENSE).

---

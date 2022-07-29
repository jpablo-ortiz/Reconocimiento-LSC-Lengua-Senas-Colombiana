# Recomendación: Cuando se inicie el proyecto dejar una versión y no el lastest

# ---------------------------- Images ----------------------------
# Tensorflow with GPU and Jupyter: tensorflow/tensorflow:latest-gpu-jupyter
# Tensorflow with only GPU: tensorflow/tensorflow:latest-gpu
# Tensorflow with CPU and Jupyter: tensorflow/tensorflow:latest-jupyter
# Tensorflow with only CPU: tensorflow/tensorflow:latest
# ----------------------------------------------------------------

# ============== Tensorflow with GPU and Jupyter ==============

FROM tensorflow/tensorflow:latest-gpu-jupyter as GPU-Jupyter

COPY ./requirements.docker.txt .
RUN pip install --no-cache-dir -r requirements.docker.txt

COPY ./app/Sign-Language/requirements_gpu.txt .
RUN pip install --no-cache-dir -r requirements_gpu.txt

#RUN apt-get update
#RUN apt install -y libgl1-mesa-glx

# ================== Tensorflow with only GPU =================

FROM tensorflow/tensorflow:latest-gpu as GPU

COPY ./requirements.docker.txt .
RUN pip install --no-cache-dir -r requirements.docker.txt

COPY ./app/Sign-Language/requirements_gpu.txt .
RUN pip install --no-cache-dir -r requirements_gpu.txt

#RUN apt-get update
#RUN apt install -y libgl1-mesa-glx

# ============== Tensorflow with CPU and Jupyter ==============

FROM tensorflow/tensorflow:latest-jupyter as CPU-Jupyter

COPY ./requirements.docker.txt .
RUN pip install --no-cache-dir -r requirements.docker.txt

COPY ./app/Sign-Language/requirements_cpu.txt .
RUN pip install --no-cache-dir -r requirements_cpu.txt

#RUN apt-get update
#RUN apt install -y libgl1-mesa-glx

# ================== Tensorflow with only CPU =================

FROM tensorflow/tensorflow:latest as CPU

COPY ./requirements.docker.txt .
RUN pip install --no-cache-dir -r requirements.docker.txt

COPY ./app/Sign-Language/requirements_cpu.txt .
RUN pip install --no-cache-dir -r requirements_cpu.txt

#RUN apt-get update
#RUN apt install -y libgl1-mesa-glx

# =============================================================
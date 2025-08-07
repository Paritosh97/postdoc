FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

ARG USER_NAME=dreamers
ARG GROUP_NAME=dreamers
ARG UID=1000
ARG GID=1000

# Set compute capability for nerfacc and tiny-cuda-nn
# See https://developer.nvidia.com/cuda-gpus and limit number to speed-up build
ENV TORCH_CUDA_ARCH_LIST="6.0 6.1 7.0 7.5 8.0 8.6 8.9 9.0+PTX"
ENV TCNN_CUDA_ARCHITECTURES=90;89;86;80;75;70;61;60


ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:/home/${USER_NAME}/.local/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}
ENV LIBRARY_PATH=${CUDA_HOME}/lib64/stubs:${LIBRARY_PATH}

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libegl1-mesa-dev \
    libgl1-mesa-dev \
    libgles2-mesa-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    python-is-python3 \
    python3.10-dev \
    python3-pip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create group and user, but DO NOT switch yet
RUN groupadd -g ${GID} ${GROUP_NAME} \
    && useradd -ms /bin/sh -u ${UID} -g ${GID} ${USER_NAME}

# Set Python 3.10 as default BEFORE switching user (must be done as root)
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# NOW switch to non-root user
USER ${USER_NAME}

RUN pip install --upgrade pip setuptools==69.5.1 ninja
RUN pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --index-url https://download.pytorch.org/whl/cu118
# Install nerfacc and tiny-cuda-nn before installing requirements.txt
# because these two installations are time consuming and error prone
RUN pip install git+https://github.com/KAIR-BAIR/nerfacc.git@v0.5.2
RUN pip install git+https://github.com/NVlabs/tiny-cuda-nn.git#subdirectory=bindings/torch

# Clone the repository
WORKDIR /workspace
RUN git clone https://github.com/GGGHSL/GraphDreamer.git

# Install the requirements
WORKDIR /workspace/GraphDreamer
RUN pip install -r requirements.txt --no-cache-dir

CMD ["/bin/bash"]

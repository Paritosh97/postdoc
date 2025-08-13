FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

ARG USER_NAME=urbanarchitect
ARG GROUP_NAME=urbanarchitect
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
    git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Create group and user, but DO NOT switch yet
RUN groupadd -g ${GID} ${GROUP_NAME} \
    && useradd -ms /bin/sh -u ${UID} -g ${GID} ${USER_NAME}

# Set Python 3.10 as default BEFORE switching user (must be done as root)
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# NOW switch to non-root user
USER ${USER_NAME}

RUN pip install --upgrade pip setuptools==69.5.1 ninja

# Clone the repository
WORKDIR /workspace
RUN git clone https://github.com/UrbanArchitect/UrbanArchitect

# Install the requirements
WORKDIR /workspace/UrbanArchitect


RUN pip install --no-cache-dir torch==2.0.1+cu118 torchvision==0.15.2+cu118 --index-url https://download.pytorch.org/whl/cu118
RUN pip install --no-cache-dir git+https://github.com/KAIR-BAIR/nerfacc.git@v0.5.2
RUN pip install --no-cache-dir git+https://github.com/NVlabs/tiny-cuda-nn.git#subdirectory=bindings/torch

RUN pip install --no-cache-dir \
    transformers==4.33.3 \
    tokenizers==0.13.3 \
    coloredlogs==15.0.1 \
    einops==0.7.0 \
    imageio==2.31.5 \
    numpy==1.26.0 \ 
    opencv-python==4.8.0.76 \
    Pillow==10.0.1 \
    scipy==1.11.3 \ 
    scikit-image==0.21.0 \
    xformers==0.0.22

RUN pip install --no-cache-dir "git+https://github.com/facebookresearch/pytorch3d.git"

RUN git lfs install

# Create models directory and clone Hugging Face repos
RUN mkdir -p /workspace/UrbanArchitect/models \
    && git clone https://huggingface.co/openai/clip-vit-base-patch32 /workspace/UrbanArchitect/models/clip-vit-base-patch32 \
    && git clone https://huggingface.co/stabilityai/stable-diffusion-2-1 /workspace/UrbanArchitect/models/stable-diffusion-2-1

RUN wget -O /workspace/UrbanArchitect/models/checkpoint-100000.pth https://home.paritosh-sharma.com/index.php/s/FxpSGwaKHDApCxJ/download

CMD ["/bin/bash"]

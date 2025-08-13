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
RUN git clone https://github.com/GGGHSL/GraphDreamer.git

# Install the requirements
WORKDIR /workspace/GraphDreamer

RUN pip install --no-cache-dir torch==2.0.1+cu118 torchvision==0.15.2+cu118 --index-url https://download.pytorch.org/whl/cu118
RUN pip install --no-cache-dir git+https://github.com/KAIR-BAIR/nerfacc.git@v0.5.2
RUN pip install --no-cache-dir git+https://github.com/NVlabs/tiny-cuda-nn.git#subdirectory=bindings/torch

RUN pip install --no-cache-dir \
    lightning==2.0.4 \ 
    omegaconf==2.3.0 \ 
    jaxtyping==0.2.20 \ 
    typeguard==4.0.0 \ 
    diffusers==0.17.1 \ 
    transformers==4.30.2 \ 
    accelerate==0.20.3 \ 
    opencv-python==4.8.0.74 \ 
    tensorboard==2.13.0 \ 
    matplotlib==3.7.1 \ 
    libigl==2.5.3.dev0 \ 
    xatlas==0.0.7 \ 
    trimesh==3.22.3 \ 
    networkx==3.1 \ 
    pysdf==0.1.8 \ 
    PyMCubes==0.1.4 \ 
    wandb==0.15.4 \ 
    gradio==3.35.2 \ 
    torchmetrics==1.0.0rc1 \ 
    IPython==8.14.0 \ 
    ipywidgets==8.0.6 \ 
    xformers==0.0.20 \ 
    bitsandbytes==0.39.1 \ 
    sentencepiece==0.1.99 \ 
    safetensors==0.3.1 \ 
    huggingface_hub==0.15.1 \ 
    einops==0.6.1 \ 
    kornia==0.6.12 \ 
    taming-transformers-rom1504==0.0.6 \ 
    controlnet_aux==0.0.6 \ 
    torch-ema==0.2 \ 
    tensorboardX==2.6.1 \ 
    tqdm==4.65.0 \ 
    ninja==1.11.1 \ 
    numpy==1.24.4 \ 
    scipy==1.11.1 \ 
    imageio-ffmpeg==0.4.8 \  
    git+https://github.com/NVlabs/nvdiffrast.git \ 
    git+https://github.com/openai/CLIP.git \ 
    git+https://github.com/ashawkey/envlight.git \
    imageio[ffmpeg]>=0.4.8 \
    trimesh[easy]==3.22.3

CMD ["/bin/bash"]

FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

ARG USER_NAME=dreamers
ARG GROUP_NAME=dreamers
ARG UID=1000
ARG GID=1000

ENV TORCH_CUDA_ARCH_LIST="6.0 6.1 7.0 7.5 8.0 8.6 8.9 9.0+PTX"
ENV TCNN_CUDA_ARCHITECTURES=90;89;86;80;75;70;61;60
ENV FORCE_CUDA=1

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
    nano \
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

WORKDIR /workspace

RUN git clone https://github.com/threestudio-project/threestudio.git
RUN git clone https://github.com/DSaurus/threestudio-stable-nerf-renderer.git /workspace/threestudio/custom/threestudio-stable-nerf-renderer/
RUN git clone https://github.com/DSaurus/threestudio-mvdream.git /workspace/threestudio/custom/threestudio-mvdream/
RUN git clone https://github.com/DSaurus/threestudio-4dfy.git /workspace/threestudio/custom/threestudio-4dfy/
RUN git clone https://github.com/GGGHSL/GraphDreamer.git
RUN git clone https://github.com/YangLing0818/Trans4D.git /workspace/Trans4D/
RUN cp -r /workspace/threestudio/load /workspace/Trans4D/
RUN git clone https://github.com/bytedance/MVDream.git /workspace/Trans4D/extern/MVDream
RUN pip install -e /workspace/Trans4D/extern/MVDream 
RUN git clone --recursive https://github.com/ashawkey/diff-gaussian-rasterization.git /workspace/Trans4D/diff-gaussian-rasterization
RUN pip install /workspace/Trans4D/diff-gaussian-rasterization
RUN pip install /workspace/Trans4D/simple-knn

RUN pip install --no-cache-dir torch==2.6.0+cu124 torchvision==0.21.0+cu124 --index-url https://download.pytorch.org/whl/cu124
RUN pip install --no-cache-dir git+https://github.com/KAIR-BAIR/nerfacc.git@v0.5.2
RUN pip install --no-cache-dir git+https://github.com/NVlabs/tiny-cuda-nn.git#subdirectory=bindings/torch
RUN pip install --no-cache-dir git+https://github.com/NVlabs/nvdiffrast.git
RUN pip install --no-cache-dir git+https://github.com/ashawkey/envlight.git
RUN pip install --no-cache-dir xformers==0.0.16

RUN pip install --no-cache-dir absl-py==1.4.0 accelerate==1.10.0 bitsandbytes==0.47.0 controlnet_aux==0.0.10 diffusers==0.34.0 einops==0.8.1 huggingface-hub==0.34.4 imageio==2.37.0 imageio-ffmpeg==0.6.0 jaxtyping==0.3.2 kornia==0.8.1 libigl==2.5.0 lightning==2.0.0 matplotlib==3.10.0 networkx==3.4.2 omegaconf==2.3.0 open3d==0.19.0 opencv-python==4.12.0.88 plotly==5.24.1 PyMCubes==0.1.6 pysdf==0.1.9 safetensors==0.6.2 sentencepiece==0.2.0 taming-transformers-rom1504==0.0.6 tensorboard==2.19.0 torchmetrics==1.8.1 transformers==4.55.0 trimesh==4.7.3 typeguard==4.4.4 wandb==0.21.1 xatlas==0.0.11 git+https://github.com/openai/CLIP.git numpy==2.0.2 pytorch-lightning==2.5.3 scipy==1.15 tqdm==4.67.1

CMD ["/bin/bash"]

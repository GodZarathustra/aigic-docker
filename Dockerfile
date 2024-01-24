FROM nvidia/cuda:11.8.0-devel-ubuntu22.04
LABEL maintainer="Martin Chan @osiutino"

ARG BRANCH_OR_TAG=master
ARG BUILD_DATE
ARG BUILD_VERSION

LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.version="${BRANCH_OR_TAG}_${BUILD_VERSION}"

RUN apt update && apt install -y --no-install-recommends \
        bash ca-certificates wget git gcc sudo libgl1 libglib2.0-dev python3-dev google-perftools \
        && rm -rf /var/lib/apt/lists/*

RUN echo "LD_PRELOAD=/usr/lib/libtcmalloc.so.4" | tee -a /etc/environment

RUN useradd --home /app -M app -K UID_MIN=10000 -K GID_MIN=10000 -s /bin/bash
RUN mkdir /app
RUN chown app:app -R /app
RUN usermod -aG sudo app
RUN echo 'app ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER app
WORKDIR /app/

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-$(uname -m).sh
RUN bash ./Miniconda3-latest-Linux-$(uname -m).sh -b \
    && rm -rf ./Miniconda3-latest-Linux-$(uname -m).sh

# RUN git clone --depth 1 --branch $BRANCH_OR_TAG https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /app/stable-diffusion-webui

COPY stable-diffusion-webui /app/stable-diffusion-webui

ENV PATH /app/miniconda3/bin/:$PATH

# RUN conda create -n sd python=3.6

# RUN conda activate sd

RUN conda install python="3.10" -y

# RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

# RUN conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -y

WORKDIR /app/stable-diffusion-webui

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

RUN pip install opencv-python facexlib scipy

RUN pip install pyyaml -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install tb-nightly -i https://mirrors.aliyun.com/pypi/simple

RUN pip install basicsr -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install gfpgan -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install clip -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY launch-test.py .

# RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# RUN python3 launch-test.py --skip-torch-cuda-test

COPY server /app/server

COPY start.sh /app/

RUN pip install oss2 flask -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app/server

RUN sudo chmod -R 777 .

WORKDIR /app/

CMD bash start.sh

# RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# RUN python3 launch.py

# RUN touch install.log && \
#     timeout 2h bash -c "./webui.sh --skip-torch-cuda-test --no-download-sd-model 2>&1 | tee install.log &" && \
#     sleep 5 && while true; do grep -q "No checkpoints found." install.log && exit 0; grep -q "ERROR" install.log && exit 1; sleep 3; done


# sudo docker run --rm --gpus all nvidia/cuda:11.8.0-devel-ubuntu22.04 nvidia-smi

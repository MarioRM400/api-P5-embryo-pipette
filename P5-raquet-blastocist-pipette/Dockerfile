FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

LABEL "author"="code"

RUN apt update && \
    apt install --no-install-recommends -y \
    libsm6 libxext6 ffmpeg python3-pip python3-venv

RUN apt install curl -y

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install -U -q --no-cache-dir \
    pip \
    wheel

# COPY requirements.txt .
RUN pip install "fastapi[standard]"
RUN pip install uvicorn
RUN pip install pillow
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install yolov5
# RUN pip3 install -q --no-cache-dir -r requirements.txt

ADD app/ app/
ADD Weights/ Weights/

EXPOSE 9051

# USER www-data

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9051"]
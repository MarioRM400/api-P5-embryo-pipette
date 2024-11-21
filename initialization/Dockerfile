FROM debian:stable-slim
WORKDIR /src

RUN apt update && \
    apt install --no-install-recommends -y \
    libsm6 libxext6 ffmpeg python3-pip python3-venv

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY src/. .

CMD [ "python3", "initialization.py" ]
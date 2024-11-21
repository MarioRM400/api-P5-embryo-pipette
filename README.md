# api-P5-raquet-blastocist-pipette

We developed a REST-API for egg detection (YOLOv5).

> **_NOTE:_** conda environments, Docker GPU, and DVC dependencies need to be installed

- **Conda environments:**

  - fastapi: Used to run API created with `envfastapi.yml`
  - p12.2: Used to download model weights from bucket with `make push`.

- **Docker GPU:** Packages needed to use GPU in docker container.
- **DVC:** makefile creates `.venv` that will download data with rigth dvc version (3.47.0) that is in `data-req.txt`.

## ⬇️ Installing dependencies

- Conda environment :

  Use `envfastapi.yml` to create environment that will run this API.

  ```bash
  # create environment
  conda env create -f envfastapi.yml
  ```

- Docker GPU (nvidia)

  Please visit this link for more info
  https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

      ```bash
      # Get and update packages
      curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
        && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
          sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
          sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
        && \
          sudo apt-get update

      # Install nvidia container toolkit
      sudo apt-get install -y nvidia-container-toolkit

      # Setting docker runtime configuration
      sudo nvidia-ctk runtime configure --runtime=docker

      # Restart docker service
      sudo systemctl daemon-reload
      sudo systemctl restart docker
      ```

## 👨🏻‍💻Usage

### 🔑 1.- Clone this repository

```
git clone git@github.com:conceivable-life/api-P5-raquet-blastocist-pipette_tip.git
```

### ☁️ 2.-Download data from bucket

- ⚠️**First**, create conda environment ⚠️

  This environment will be used only to download model weights with dependencies in `data-req.txt` file.

  ```sh
  # create and activate conda environment
  conda create -n p12.2 python=3.12.2 -y
  conda activate p12.2

  ```

- Download data

  ```sh
  # google cloud authentication
  gcloud auth application-default login

  # download data with dvc
  make pull
  ```

### 🚢3.-Build docker image and run a container

There are 2 options that could be used to run a container.

- Linux
- WSL (windows)

We are using a docker compose yaml file to create the image and a container from it.

```bash
# image and container creation
docker compose up -d

# stop container
docker compose down
```

## 📃API documentation

See the documentation here `http://localhost:9051/docs` and `http://localhost:9051/redoc`.

### Test API inference with Python

To test the API, we can use images the script 'test_api.py'

```bash
python test_api.py
```

The processed images will be stored in the `output/` directory in the first case. The labeled video will be viewed
during the script execution in the second case.

## Test API inference with curl

Make a request using `curl`:

```bash
curl -X 'POST' \
'http://localhost:9051/predict/' \
-H 'accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-F 'image=@test_inference.jpg;type=image/jpeg'
```

API response for an image that contains a single object of interest (example):

```bash
{
    "response": {
        "response": {
            "racket": [
                {
                    "id": 0,
                    "bounding_box": [
                        762.8421020507812,
                        1210.255126953125,
                        1024.8201904296875,
                        1399.7818603515625
                    ],
                    "confidence": 0.99
                },
                {
                    "id": 1,
                    "bounding_box": [
                        852.5689697265625,
                        1282.4476318359375,
                        940.5763549804688,
                        1346.5899658203125
                    ],
                    "confidence": 0.94
                },
                {
                    "id": 3,
                    "bounding_box": [
                        870.0145874023438,
                        1292.2591552734375,
                        919.4967651367188,
                        1331.8936767578125
                    ],
                    "confidence": 0.92
                },
                {
                    "id": 4,
                    "bounding_box": [
                        804.5952758789062,
                        1258.582275390625,
                        982.3280639648438,
                        1367.6109619140625
                    ],
                    "confidence": 0.78
                }
            ],
            "embryo": [
                {
                    "id": 2,
                    "bounding_box": [
                        884.9662475585938,
                        1298.4132080078125,
                        911.2677612304688,
                        1328.48876953125
                    ],
                    "confidence": 0.94
                }
            ]
        }
    }
}
```

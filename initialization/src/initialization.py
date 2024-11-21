import cv2
import requests
import sys
import os
from pathlib import Path


def main():
    cwd = os.getcwd()
    full_path = Path(os.path.join(cwd, IMAGE))

    if full_path.is_file():
        img = cv2.imread(str(full_path))
        img_encode = cv2.imencode(".jpg", img)[1].tobytes()

        try:
            response = requests.post(
                URL, files={"file": (str(full_path), img_encode, "image/jpeg")}
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            sys.exit(f"Request failed: {e}")

        # try:
        #     with open(full_path, "rb") as img_encode:
        #         response = requests.post(URL, files={"file": img_encode})
        #     response.raise_for_status()
        # except Exception as e:
        #     sys.exit("%s" % e)

        response_data = response.json()
        print(
            "API Response:", response_data
        )  # Print the full API response for debugging
        data = response_data.get("response", {})
    else:
        print(
            """\timage does not exist\n
        Note: Execute initialization.py from its path location"""
        )


if __name__ == "__main__":
    print("----------Performing first inference----------")
    URL = "http://172.30.0.3:9051/predict"
    IMAGE = "image.png"
    main()

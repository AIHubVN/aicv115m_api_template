# AICovidVN API Template

## Setup

Please follow these steps to reproduce:

0. Clone this repo, go to inside and make new venv `virtualenv venv`
1. Install sox: (macos) `brew install sox`, (linux) `sudo apt install sox`
2. Install ffmpeg: (linux) `sudo apt-get install ffmpeg`
3. Activate to new venv `source venv/bin/active`
4. Install required packages/libs using `pip install -r requirements.txt`
5. Create .env file `cp .env-example .env` and change username, password for authentication.

## Train
If the "weights" directory is empty, retrain the model to get the weights used for the API with the following steps:

1. Run script: `python create_dataset.py` to get training and testing data.
2. Train model: `python train.py`

## Use API

This repository using Fast API to create API.

```bash
python main.py
```
View more detail and test API at http://localhost:8000/docs

Test API using python script:
```python
import requests
import json
import time
import hashlib

url = 'http://localhost:8000/api/predict/'

token = hashlib.sha256("{}:{}".format(user, password).encode()).hexdigest() # Insert username and password
headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer ' + token
}

uuid = "" # Insert user id here.
audio_path = "" # Insert file path of audio file here.
gender = None # Insert gender here.
age = None # Insert age here.
cough_type = None # Insert type of cough here.

metadata = json.dumps({"uuid": uuid, "subject_gender" : gender, "subject_age" : age, "subject_cough_type": cough_type})
files = {
    'meta': (None, metadata),
    'audio_file': (audio_name, open(audio_path, 'rb')),
}

response = requests.post(url, headers=headers, files=files).json()
print(response)
```

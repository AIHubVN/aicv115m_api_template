# AICovidVN API Template

This template using [FastAPI](https://fastapi.tiangolo.com/) to create API.

## Requirements
* uvicorn
* fastapi
* pydub (use to convert the format of audio files)

## Directory & file structures


```
api_template
│   .gitignore
│   requirements.txt
│   README.md
│   process.py - main script to process and predict results
│   serve.py - main script to start API
│   run_server.sh
│
└───data/ - datasets are saved here
│   │   ...
│
└───weights/ - trained models are saved here
│   │   ...
│
└───configs/ - holds configuration for training, testing or inference
│   │   __init__.py
│   │   ...
│
└───modules/ - ALL YOUR SOURCE CODE PUT HERE
│   │   __init__.py
│   │   ...
│
└───docs/ - put the report, instructions to use the code here
│   │   tutorial.md
│   │   ...
│
```

A few important files you need to pay attention and modify:
1. `process.py`: Rewrite the "predict" function to match your source code
2. `docs/tutorials.md`: Write a few lines about how to train, test and inference using API with dataset
3. Put all your source code in `modules` folder and your config in `configs` folder.

## Testing

After processing and refactoring the source code, you can start API in the following ways:

```bash
python serve.py
```
or
```bash
chmod +x run_server.sh
./run_server.sh
```
View more details and test API at http://localhost:8000/docs

Or test API using python script:
```python
import requests
import json
import time

url = 'http://localhost:8000/api/predict/'
headers = {
    'accept': 'application/json'
}

uuid = "" # Insert user id here.
audio_path = "" # Insert file path of audio file here.
gender = None # Insert gender here.
age = None # Insert age here.
cough_type = None # Insert type of cough here.
health_status = None # Insert health status here.
note = None # Insert note here

metadata = json.dumps(
    {
        "uuid": uuid,
        "subject_gender" : gender,
        "subject_age" : age,
        "subject_cough_type": cough_type,
        "subject_health_status": health_status,
        "note": note
    }
)

files = {
    'meta': (None, metadata),
    'audio_file': (audio_name, open(audio_path, 'rb')),
}

response = requests.post(url, headers=headers, files=files).json()
print(response)
```

## Acknowledgements
This template is used to assist the teams participating in ["AICovidVN 115M Challenge"](https://aihub.vn/competitions/22) to submit the final solution according to the organizer's standards.

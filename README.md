# AICovidVN API Template

This template using [FastAPI](https://fastapi.tiangolo.com/) to create API. A valid solution submission needs to:
- Execute successfully 3 scripts under scripts/.
- Execute `docker-compose up` command to start serving.

You're free to fork this template and apply it to your team's solution. Then you can send back the solution as a .zip file. More information will be provided via email.

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
│   main.py - main script to start train or create submission
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
scripts/ - command use for train, create submission, run service
│   │   run_train.sh
│   │   run_submission.sh
│   │   run_service.sh
│
```

A few important files you need to pay attention and modify:
1. `process.py`: Rewrite the "predict" function to match your source code.
2. `main.py`: Add your function to train and create submission here.
3. `docs/tutorials.md`: Write a few lines about how to train, test and inference using API with dataset.
4. Put all your source code in `modules` folder and your config in `configs` folder.

## Training

After processing and refactoring the source code, try training the model:

```bash
chmod +x scripts/run_train.sh
./scripts/run_train.sh
```

## Testing
### 01. Run serving on host machine
After processing and refactoring the source code, you can start API in the following way:

```bash
chmod +x scripts/run_service.sh
./scripts/run_service.sh
```

### 02. Build and run with Docker
- How to install docker-compose: check this [guideline](https://docs.docker.com/compose/install/).
- Build and start serving:
```bash
docker-compose up
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

## Submit
You can create submission by:

```bash
chmod +x scripts/run_submission.sh
./scripts/run_submission.sh
```

## Acknowledgements
- This template is used to assist the teams participating in ["AICovidVN 115M Challenge"](https://aihub.vn/competitions/22) to submit the final solution according to the organizer's standards.
- Feature Extractors are employed from https://github.com/nutiapps/aicovidvn115m.

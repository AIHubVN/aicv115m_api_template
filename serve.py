import time
import json
import uvicorn
import aiofiles
import pandas as pd
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Form, HTTPException

from configs import AssetsConfig
from process import predict, convert_to_wav


class Metadata(BaseModel):
    uuid: str = None
    subject_gender: Optional[str] = None
    subject_age: Optional[int] = None
    subject_cough_type: Optional[str] = None
    subject_health_status: Optional[str] = None
    note: Optional[str] = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}


@app.post("/api/predict/")
async def predict_assessment(meta: Metadata = Form(...), audio_file: UploadFile = File(None, media_type='audio/wav')):
    timestamp = time.time()

    if not meta.uuid:
        raise HTTPException(status_code=404, detail="UUID not found")

    # save audio
    ext = audio_file.filename.split(".")[-1]
    audio_path = str(
        AssetsConfig.AUDIO_PATH / "{}-{}.{}".format(meta.uuid, timestamp, ext))
    async with aiofiles.open(audio_path, 'wb') as f:
        content = await audio_file.read()  # async read
        await f.write(content)  # async write

    if ext != "wav":
        try:
            audio_path = convert_to_wav(audio_path)
        except:
            raise HTTPException(
                status_code=418, detail="Oops! The current API does not support handling {} files.".format(ext))

    # processing data
    metadata_json = {
        "uuid": meta.uuid,
        "subject_gender": meta.subject_gender,
        "subject_age": meta.subject_age,
        "subject_cough_type": meta.subject_cough_type,
        "subject_health_status": meta.subject_health_status,
        "note": meta.note,
        "file_path": audio_path
    }

    df = pd.DataFrame([metadata_json])
    assessment = predict(df)

    metadata_json['assessment'] = assessment

    # save metadata
    metadata_path = str(
        AssetsConfig.META_PATH / "{}-{}.json".format(meta.uuid, timestamp))
    with open(metadata_path, 'w') as f:
        json.dump(metadata_json, f)

    return {"assessment": assessment}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0")

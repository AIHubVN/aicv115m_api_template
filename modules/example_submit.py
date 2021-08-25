import os
import joblib
import zipfile
import pandas as pd

from configs.example_config import Config
from modules.example_dataset import make_acoustic_feat


def create_submission():

    df = pd.read_csv(str(Config.ROOT_TEST_DIR /
                     "private_test_sample_submission.csv"))
    df['file_path'] = df['uuid'].apply(lambda x: str(
        Config.ROOT_TEST_DIR / f"private_test_audio_files/{x}.wav"))

    X = make_acoustic_feat(df)
    model = joblib.load(str(Config.WEIGHT_PATH / "example_model.h5"))
    y_predict = model.predict(X)

    df['assessment_result'] = y_predict
    sub = df[['uuid', 'assessment_result']]
    sub.to_csv("results.csv", index=None)

    Config.SUBMISSION_PATH.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(Config.SUBMISSION_PATH / "results.zip"), 'w') as zf:
        zf.write('results.csv')
    os.remove('results.csv')

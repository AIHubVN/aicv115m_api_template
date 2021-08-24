import os
from pydub import AudioSegment

import joblib
from configs.example_config import Config
from modules.example_dataset import make_acoustic_feat


def convert_to_wav(file_path):
    """
    This function is to convert an audio file to .wav file

    Args:
        file_path (str): paths of audio file needed to be convert to .wav file

    Returns:
        new path of .wav file
    """
    ext = file_path.split(".")[-1]
    assert ext in [
        "mp4", "mp3", "acc"], "The current API does not support handling {} files".format(ext)

    sound = AudioSegment.from_file(file_path, ext)
    wav_file_path = ".".join(file_path.split(".")[:-1]) + ".wav"
    sound.export(wav_file_path, format="wav")

    os.remove(file_path)
    return wav_file_path


def predict(df):
    """
    This function is to predict class/probability.

    Args:
        df (dataFrame): include audio path and metadata information.

    Returns:
        assessment (float): class/probability

    """
    feat = make_acoustic_feat(df)
    model = joblib.load(str(Config.WEIGHT_PATH / "example_model.h5"))
    positive_proba = model.predict_proba(feat)[0][1]
    return positive_proba

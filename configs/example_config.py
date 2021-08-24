from pathlib import Path


class Config:
    DATASET_PATH = Path("./data")
    DATASET_PATH.mkdir(parents=True, exist_ok=True)
    ROOT_TRAIN_DIR = DATASET_PATH / "example_aicv115m_final_public_train"
    ROOT_TEST_DIR = DATASET_PATH / "example_aicv115m_final_private_test"

    WEIGHT_PATH = Path("./weights")
    WEIGHT_PATH.mkdir(parents=True, exist_ok=True)

    SUBMISSION_PATH = Path("./submissions")

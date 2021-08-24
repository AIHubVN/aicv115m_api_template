import joblib
import lightgbm as lgb
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from configs.example_config import Config
from modules.example_dataset import prepare_training_data


def prepare_training_data(Config):
    df = pd.read_csv(str(Config.ROOT_TRAIN_DIR / "public_train_metadata.csv"))
    df['file_path'] = df['uuid'].apply(lambda x: str(
        Config.ROOT_TRAIN_DIR / f"public_train_audio_files/{x}.wav"))

    X = df.drop(["assessment_result"], axis=1)
    y = df['assessment_result']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.2)
    X_train, X_val = make_acoustic_feat(X_train), make_acoustic_feat(X_val)

    return X_train, X_val, y_train, y_val


def train():
    X_train, X_val, y_train, y_val = prepare_training_data(Config)

    model = lgb.LGBMClassifier(class_weight='balanced',
                               num_leaves=31,
                               max_depth=-1,
                               min_child_samples=2,
                               learning_rate=0.02,
                               n_estimators=100,
                               colsample_bytree=0.75,
                               subsample=0.75,
                               n_jobs=-1,
                               random_state=42
                               )
    model.fit(X_train, y_train)
    y_val_pred = model.predict(X_val)
    print(f"AUC score: {roc_auc_score(y_val, y_val_pred):12.4f}")

    joblib.dump(model, str(Config.WEIGHT_PATH / "example_model.h5"))


if __name__ == "__main__":
    train()

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AICovidVN API Template")
    parser.add_argument('action', type=str, choices=['train', 'submit'])
    args = parser.parse_args()

    if args.action == "train":
        from modules.example_train import train
        train()
    if args.action == "submit":
        from modules.example_submit import create_submission
        create_submission()

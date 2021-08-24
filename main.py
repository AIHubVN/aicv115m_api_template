import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AICovidVN API Template")
    parser.add_argument('action', type=str, choices=['train', 'submit'])
    args = parser.parse_args()

    if args.action == "train":
        """
        Add script to train model here
        """
        pass
    if args.action == "submit":
        """
        Add script to create submission here
        """
        pass

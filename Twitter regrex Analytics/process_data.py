import pandas as pd

from src.feature_engineering import create_features


INPUT_FILE = "data/tweets.csv"
OUTPUT_FILE = "output/processed_tweets.csv"

CHUNK_SIZE = 10000


def process_dataset():

    first_chunk = True
    total_rows = 0

    print("Starting data processing...\n")

    for chunk in pd.read_csv(
        INPUT_FILE,
        encoding="latin-1",
        chunksize=CHUNK_SIZE
    ):

        processed_chunk = create_features(chunk)

        processed_chunk.to_csv(
            OUTPUT_FILE,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False
        )

        total_rows += len(processed_chunk)

        first_chunk = False

        print(f"Processed {total_rows:,} tweets")

    print("\nProcessing completed!")
    print(f"Total tweets processed: {total_rows:,}")


if __name__ == "__main__":
    process_dataset()
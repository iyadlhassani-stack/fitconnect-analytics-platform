from pathlib import Path

RAW_DATA_DIR = Path("data/raw")


def main() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Synthetic data generator will write files to:", RAW_DATA_DIR)


if __name__ == "__main__":
    main()
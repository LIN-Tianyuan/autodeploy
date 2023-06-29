from pathlib import Path
path = Path(__file__)

ROOT_DIR = str(path.parent.parent)

if __name__ == "__main__":
    print(ROOT_DIR)

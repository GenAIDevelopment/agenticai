import os 
from dotenv import load_dotenv


def load_OPEN_API_KEY():
    load_dotenv()
    return os.getenv('OPENAI_API_KEY')


def main():
    openai_api_key = load_OPEN_API_KEY()


if __name__ == "__main__":
    main()

from dotenv import load_dotenv
import os

def main():
    print(os.getenv('LANGSMITH_MYKEY', 'NO KEY FOUND'))
    load_dotenv()
    print(os.getenv('LANGSMITH_MYKEY','NO KEY FOUND'))
    


if __name__ == "__main__":
    main()

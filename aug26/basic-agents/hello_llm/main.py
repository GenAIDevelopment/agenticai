import os
from dotenv import load_dotenv

def main():
    why = os.getenv('HELLO_LLM_WHY')
    print(why)
    load_dotenv()
    why = os.getenv('HELLO_LLM_WHY')
    print(why)
        


if __name__ == "__main__":
    main()

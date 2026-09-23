from dotenv import load_dotenv
import os
import claude
import gpt


def print_api_keys():
    load_dotenv()
    print(os.getenv('ANTHROPIC_API_KEY'))
    print(os.getenv('OPENAI_API_KEY'))



    

if __name__ == "__main__":
    #print_api_keys()
    #claude.interact_with_model()
    gpt.interact_with_model()

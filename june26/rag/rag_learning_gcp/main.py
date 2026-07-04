from utils import get_model_from_gcp

def main():
    llm = get_model_from_gcp(model_name="gemini-2.5-flash-lite")
    result = llm.invoke("What is 2+2?")
    result.pretty_print()
    


if __name__ == "__main__":
    main()

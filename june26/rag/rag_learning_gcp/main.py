from utils import get_model_from_gcp

def main():
    llm = get_model_from_gcp()
    result = llm.invoke("What is 2+2?")
    result.pretty_print()
    


if __name__ == "__main__":
    main()

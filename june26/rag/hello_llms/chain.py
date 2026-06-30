from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.base import Runnable

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

print(f"is llm runnable {isinstance(llm, Runnable)}")

prompt = HumanMessage(content='What is capital of France?')
print(f"Is Prompt runnable {isinstance(prompt, Runnable)}")

parser = StrOutputParser()
print(f"Is parser runnable {isinstance(parser, Runnable)}")

chain =  llm | parser
print(f"is chain runnable {isinstance(chain, Runnable)}")
response = chain.invoke([prompt])
print(response)


otherchain = llm | parser
response = otherchain.invoke([HumanMessage('What is capital of India')])
print(response)

x = chain | otherchain
response = x.invoke([HumanMessage('What is capital of USA')])
print(response)




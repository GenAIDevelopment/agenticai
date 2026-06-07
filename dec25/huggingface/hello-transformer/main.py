from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

# response = classifier("I like Large Language models very much")
# print(response)

response = classifier("I got irritate standing in line at airport")
print(response)
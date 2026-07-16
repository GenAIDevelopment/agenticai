"""In this module lets explore how recursive chunking works
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter


sample_text = """Paragraph one is short

Paragraph two is a bit longer that the first one. This will not fit inside a small chunk size. So the splitter has to recurse further to break it apart into smaller pieces. 

Paragraph three is short too."""


seperators = ["\n\n", ". "]

splitter = RecursiveCharacterTextSplitter(
    separators=seperators,
    chunk_size=50,
    chunk_overlap=10,
    keep_separator=False
)

chunks = splitter.split_text(sample_text)
for index, chunk in enumerate(chunks):
    print(f"Chunk {index}: length {len(chunk)}\n\n{chunk}\n\n\n")
"""
This module contains 
    * code to read all text the pages content (page_n.txt) and combine into a single text
    * Now perform recursive splitting by regex and then by length (1000)
"""
import os
import glob
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def extract_chapter_text(
        chapter_dir: str = "./knowledge/book/extracted/text",
        pattern: str = "*.txt") -> str:
    text = ""
    # Get all the files in the directory with page_*.txt
    files = glob.glob(f"{chapter_dir}/{pattern}")
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            text += f.read() + "\n"
    return text


def split_by_section_with_limits(
        text: str,
        section_pattern: list[str] = [r"\n(?=\d+\.\d+\s)", ". "],
        chunk_size: int = 1000,
        chunk_overlap: int = 150) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        separators=section_pattern,
        is_separator_regex=True,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    # chunks = text_splitter.create_documents([text])
    chunks = text_splitter.split_text(text)
    print(f"total number of chunks = {len(chunks)}")
    return chunks


if __name__ == "__main__":
    chapter1_text = extract_chapter_text(
        "./knowledge/book/extracted/text", "page_*.txt")
    chunks = split_by_section_with_limits(chapter1_text)
    for index, chunk in enumerate(chunks):
        print(f"Chunk {index}: length {len(chunk)}")
        #input("Press Enter to continue and Ctrl + C to quit")

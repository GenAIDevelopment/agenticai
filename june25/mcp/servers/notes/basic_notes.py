from mcp.server.fastmcp import FastMCP
from typing import Literal
import os
import pathlib
mcp = FastMCP("basic-notes")

FILE_LOCATION = r"C:\GenerativeAI\notes\notes.txt"

def ensure_file_exists():
    """checks if the file exists
    if not creates a new file
    """
    if not os.path.exists(FILE_LOCATION):
        with open(FILE_LOCATION, "w"):
            pass


@mcp.tool()
def save_notes(note: str) -> str:
    """This stores notes locally

    Args:
        note (str): note to be stored

    Returns:
        str: 'Saved' if everythings right otherwise 'Not Saved'
    """
    # append to file in FILE_LOCATION
    ensure_file_exists()
    result = "Saved"
    try:
        with open(FILE_LOCATION,mode='a') as notes:
            notes.write(note + "\n")
    except Exception as e:
        result = "Not Saved"
    finally:
        return result



@mcp.tool()
def get_all_notes() -> str:
    """This gets all the notes from local storage

    Returns:
        str: notes
    """
    ensure_file_exists()
    content = ""
    try:
        with open(FILE_LOCATION,mode='r') as notes:
            content = notes.read()
            
    except Exception as e:
        content = ""
    finally:
        return content
    

@mcp.resource(name="latest", uri="resource://latest")
def get_latest_notes() -> str:
    """This function gets the latest notes

    Returns:
        str: latest notes if found else No Notes Yet
    """
    ensure_file_exists()
    lines = []
    try:
        with open(FILE_LOCATION,mode='r') as notes:
            lines = notes.readlines()
    except Exception as e:
        return "No Notes Yet"
    finally:
        return lines[-1]


@mcp.prompt(name="summaryprompt")
def summary_prompt() -> str:
    """This method has a summary prompt

    Returns:
        str: prompt to summarize the notes
    """
    content = get_all_notes()
    return f"Summarize notes: {content}"



if __name__ == '__main__':
    mcp.run(transport='stdio')
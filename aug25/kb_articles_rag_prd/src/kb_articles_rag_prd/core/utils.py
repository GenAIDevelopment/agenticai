"""This module will have reusable functions
"""

import hashlib

def sha1hash_file(path:str) -> str:
    """This method calculates the hash

    Args:
        path (str): Path of the file

    Returns:
        str: sha1_hash
    """
    with open(path, 'rb') as f:
        sha1hash = hashlib.sha1(f.read()).hexdigest()
    return sha1hash
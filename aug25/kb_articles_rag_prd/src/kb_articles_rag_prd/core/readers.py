"""This module will have an implementation to
read the documents from a directory and necessary information to 
metadata
"""

from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader
from kb_articles_rag_prd.core.common import BaseReader
from kb_articles_rag_prd.core.utils import sha1hash_file


class DirectoryReader(BaseReader):
    """This implementation reads the files from directory
    and adds the hash to be metadata
    """

    def read(self, path:str,glob:str) -> list[Document]:
        """This method will read the documents
        """
        directory_loader = DirectoryLoader(
            path=path,
            glob=glob,
            use_multithreading=True)
        docs = directory_loader.load()
        # wrong implmentation
        for doc in docs:
            doc.metadata.update(
                'checksum', sha1hash_file(doc.metadata['source'])
            )
        return docs
    





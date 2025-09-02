"""This will be the base class for reading docs
"""
from abc import ABC, abstractmethod
#langchain_core.documents.base.Document
from langchain_core.documents import Document

class BaseReader(ABC):
    """Base Reader

    Args:
        ABC (_type_): BaseReader
    """

    @abstractmethod
    def read(self, path:str,glob:str) -> list[Document]:
        """This method will read the documents
        """
        pass



from pathlib import Path
import re
from datamodels import Document, Paragraph


# This inheritence might not be a good idea but starting off with it
class DataParser:
    def __init__(self, data_path: str):
        self.data_path = data_path
    
    def parse(self):
        raise NotImplementedError


class TxtDataParser(DataParser):
    def parse(self) -> list[Paragraph]:
        with open(self.data_path, "r") as file:
            txt_data = file.read()
            paragraphs = re.split(r"\n\n+", txt_data)
        return [Paragraph(index, paragraph) for index, paragraph in enumerate(paragraphs)]


def get_data(data_path: str) -> list[Document]:
    files = Path(data_path).glob("*")
    texts = []
    for file in files:
        file_name = file.name.rstrip(file.suffix)
        if file.suffix == ".txt":
            paragraph_list = TxtDataParser(file).parse()
        doc = Document(
            file_name= file.name, 
            title=file_name, 
            type=file.suffix,
            paragraphs=paragraph_list
        )
        texts.append(doc)
    return texts
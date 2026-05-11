import os
import json
import asyncio
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    CSVLoader,
    UnstructuredMarkdownLoader
)

def pdf_loader(filepath: str) -> list[Document]:
    try:
        return PyPDFLoader(filepath).load()
    except:
        return []

def txt_loader(filepath: str) -> list[Document]:
    try:
        return TextLoader(filepath, encoding="utf-8").load()
    except:
        return []

def docx_loader(filepath: str) -> list[Document]:
    try:
        return Docx2txtLoader(filepath).load()
    except:
        return []

def csv_loader(filepath: str) -> list[Document]:
    try:
        return CSVLoader(filepath, encoding="utf-8").load()
    except:
        return []

def json_loader(filepath: str) -> list[Document]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        text = json.dumps(data, ensure_ascii=False, indent=2)
        return [Document(page_content=text)]
    except:
        return []

def md_loader(filepath: str) -> list[Document]:
    try:
        return UnstructuredMarkdownLoader(filepath).load()
    except:
        return []

async def parse_document(file_path: str) -> list[Document]:
    ext = os.path.splitext(file_path)[-1].lower()

    # 同步文件读取 -> 放到线程池执行，不阻塞异步事件循环
    loop = asyncio.get_event_loop()

    if ext == ".pdf":
        return await loop.run_in_executor(None, pdf_loader, file_path)

    elif ext == ".txt":
        return await loop.run_in_executor(None, txt_loader, file_path)

    elif ext == ".docx":
        return await loop.run_in_executor(None, docx_loader, file_path)

    elif ext == ".csv":
        return await loop.run_in_executor(None, csv_loader, file_path)

    elif ext == ".json":
        return await loop.run_in_executor(None, json_loader, file_path)

    elif ext == ".md":
        return await loop.run_in_executor(None, md_loader, file_path)

    return []
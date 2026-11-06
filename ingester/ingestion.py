from pathlib import Path
from uuid import uuid4
from ingester.state import PaperState



def pdf_ingestion(state:PaperState) -> dict:
    """It verfiy the paper """
    pdf_path = Path(state['pdf_path'])

    if not pdf_path.exists():
        return{"ingestion_status":"failed",
               "errors":["pdf file does not exist."]
               }
    if not pdf_path.is_file():
        return {
             "ingestion_status": "failed",
            "errors": ["Provided path is not a file."]
        }
    if pdf_path.suffix.lower()!=".pdf":
        return{
            "ingestion_status":"failed",
            "errors":["ONly Pdf files are supported"]
        }
    if pdf_path.stat().st_size == 0:
        return{
             "ingestion_status": "failed",
            "errors": ["PDF file is empty."]
        }
    with pdf_path.open('rb') as file:
        header= file.read(5)
    if header != b"%PDF-":
        return{
             "ingestion_status": "failed",
            "errors": ["File does not have a valid PDF header."]
        }   

    return {
        "paper_id": str(uuid4()),
        "file_size_bytes": pdf_path.stat().st_size,
        "ingestion_status": "success",
        "errors": []
    } 
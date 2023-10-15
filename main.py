import os
import crud
import models
import parse_to_dicts

from fastapi import FastAPI, Depends, Request, HTTPException, File, UploadFile
from typing import List
from process_pdf import process_pdf_files, unparse_pdf
from database import Session, engine
from validator import validate_m_11


app = FastAPI()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

if 'M-11Pdf' not in os.listdir():
    os.mkdir('M-11Pdf')

@app.post("/forcedoc", status_code=201)
async def upload_pdf_files(db=Depends(get_db), files: List[UploadFile] = File(...)):
    try:
        for file in files:
            file_location = f"M-11Pdf/{file.filename}"
            with open(file_location, "wb") as buffer:
                buffer.write(await file.read())
            output_json_file = await post_push_file(db)

            os.remove(output_json_file)
            os.remove(file_location)
    except:
        print("Произошла ошибка")
    return {"message": "Файлы успешно загружены"}

@app.post("/filechecker", status_code=200)
async def upload_pdf_files(db=Depends(get_db), files: List[UploadFile] = File(...)):
    check_results = {}
    try:
        for file in files:
            file_location = f"M-11Pdf/{file.filename}"
            with open(file_location, "wb") as buffer:
                buffer.write(await file.read())
            output_json_file, errors = await check_docs(db)
            check_results[file.filename] = errors
            os.remove(output_json_file)
            os.remove(file_location)
    except:
        print("Произошла ошибка")
    return check_results

async def post_push_file(db):
    folder_path = 'M-11Pdf'
    coordinates = [(57.5, 8, 70, 10), (25, 12, 65, 14), (18.5, 15.5, 73, 19)]

    results = process_pdf_files(folder_path, coordinates)

    folder_path = 'M-11Pdf'
    output_folder = "11_output"
    output_json_file = unparse_pdf(folder_path, output_folder)
    df_forms, df_table1, df_table2 = parse_to_dicts.create_dataframes(output_json_file)
    crud.add_document(db, results, df_forms, df_table1, df_table2)
    return output_json_file

async def check_docs(db):
    folder_path = 'M-11Pdf'
    coordinates = [(57.5, 8, 70, 10), (25, 12, 65, 14), (18.5, 15.5, 73, 19)]

    results = process_pdf_files(folder_path, coordinates)

    folder_path = 'M-11Pdf'
    output_folder = "11_output"
    output_json_file = unparse_pdf(folder_path, output_folder)
    df_forms, df_table1, df_table2 = parse_to_dicts.create_dataframes(output_json_file)
    val_flag, errors = validate_m_11(db, results, df_forms, df_table1, df_table2)
    return output_json_file, errors

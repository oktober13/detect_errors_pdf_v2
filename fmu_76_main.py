from fastapi import FastAPI, Depends, Request, HTTPException, File, UploadFile
from typing import List
from process_pdf import process_pdf_files, unparse_pdf
from database import Session, engine
import os
from validator import validate_m_11
import crud
import models
import parse_to_dicts

app = FastAPI()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

@app.post("/forcedoc", status_code=201)
async def upload_pdf_files(db=Depends(get_db), files: List[UploadFile] = File(...)):
    try:
        for file in files:
            file_location = f"FMU_76Pdf/{file.filename}"
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
            file_location = f"FMU_76Pdf/{file.filename}"
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
    folder_path = 'FMU_76Pdf'
    coordinates = [(57.5, 8, 70, 10), (25, 12, 65, 14), (18.5, 15.5, 73, 19)]

    results = process_pdf_files(folder_path, coordinates)

    folder_path = 'FMU_76Pdf'
    output_folder = "76_output"
    output_json_file = unparse_pdf(folder_path, output_folder)
    df_forms, df_table1, df_table2 = parse_to_dicts.create_dataframes(output_json_file)
    crud.add_document(db, results, df_forms, df_table1, df_table2)
    return output_json_file

async def check_docs(db):
    folder_path = 'FMU_76Pdf'
    coordinates = [(57.5, 8, 70, 10), (25, 12, 65, 14), (18.5, 15.5, 73, 19)]

    results = process_pdf_files(folder_path, coordinates)

    folder_path = 'FMU_76Pdf'
    output_folder = "76_output"
    output_json_file = unparse_pdf(folder_path, output_folder)
    df_forms, df_table1, df_table2 = parse_to_dicts.create_dataframes(output_json_file)
    val_flag, errors = validate_m_11(db, results, df_forms, df_table1, df_table2)
    return output_json_file, errors

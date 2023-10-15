from fastapi import FastAPI, Depends, Request, HTTPException
from process_pdf import process_pdf_files, unparse_pdf
from database import Session, engine
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
async def post_game_log(db=Depends(get_db)):
    # Папка с документами pdf формы 11
    folder_path = 'M-11Pdf'
    coordinates = [(57.5, 8, 70, 10), (25, 12, 65, 14), (18.5, 15.5, 73, 19)]

    results = process_pdf_files(folder_path, coordinates)

    folder_path = 'M-11Pdf'  # Путь к папке, где находятся PDF-файлы
    output_folder = "11_output"  # Путь к новой папке для сохранения JSON-файлов
    unparse_pdf(folder_path, output_folder)
    df_forms, df_table1, df_table2 = parse_to_dicts.create_dataframes(output_folder + '/М-11 1029 от 27.01.2023.json')
    crud.add_document(db, results, df_forms, df_table1, df_table2)

@app.post("/checkdoc", status_code=200)
async def post_game_log(db=Depends(get_db)):
    # Папка с документами pdf формы 11
    folder_path = 'M-11Pdf'
    coordinates = [(57.5, 8, 70, 10), (25, 12, 65, 14), (18.5, 15.5, 73, 19)]

    results = process_pdf_files(folder_path, coordinates)

    folder_path = 'M-11Pdf'  # Путь к папке, где находятся PDF-файлы
    output_folder = "11_output"  # Путь к новой папке для сохранения JSON-файлов
    output_json_file = unparse_pdf(folder_path, output_folder)
    df_forms, df_table1, df_table2 = parse_to_dicts.create_dataframes(output_json_file)
    val_flag, errors = validate_m_11(db, results, df_forms, df_table1, df_table2)
    if val_flag:
        raise HTTPException(detail='\n'.join(errors))

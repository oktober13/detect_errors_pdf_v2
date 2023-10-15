import fitz
import pdfplumber
import json
import os

def extract_statement_name(file_path, x1, y1, x2, y2):
    doc = fitz.open(file_path)
    page = doc.load_page(0)  # Получаем первую страницу

    # Получаем размеры страницы
    page_width = page.mediabox_size[0]
    page_height = page.mediabox_size[1]

    # Вычисляем координаты в пикселях на основе процентов
    x1_px = int(x1 * page_width / 100)
    y1_px = int(y1 * page_height / 100)
    x2_px = int(x2 * page_width / 100)
    y2_px = int(y2 * page_height / 100)

    # Извлекаем текст из указанного фрагмента страницы
    text = page.get_textbox(fitz.Rect(x1_px, y1_px, x2_px, y2_px))
    statement_name = text.strip()

    doc.close()

    return statement_name


def process_between_tables(file_name):
    keywords = ['Через', 'Разрешил', 'Затребовал']
    width = [500, 300, 300]
    res_dict = {}
    for keyword, wid in zip(keywords, width):
        flag, borders = find_borders(file_name, keyword, wid)
        if flag:
            words = find_text(file_name, borders)
            res_dict[keyword] = ' '.join(process_list(words, keyword))
    return res_dict


def process_list(input_list, keyword):
    result_list = []

    for word in input_list:
        if word == keyword or word == 'кого':
            continue
        elif word.startswith(keyword):
            result_list.append(word[len(keyword):])
        else:
            result_list.append(word)

    return result_list


def find_text(file_name, borders):
    with pdfplumber.open(file_name) as pdf:
        page = pdf.pages[0]
        words = page.extract_words()

        word_found = []
        for d in words:
            if borders[0] <= d['x0'] and d['x1'] <= borders[2] and borders[1] <= d['top'] and d['bottom'] <= borders[3]:
                word_found.append(d['text'])
        return word_found


def find_borders(file_name, keyword, wid):
    with pdfplumber.open(file_name) as pdf:
        page = pdf.pages[0]

        words = page.extract_words()

        word_found = None
        for d in words:
            if d['text'].startswith(keyword):
                word_found = d
                break

        if not (word_found is None):
            x0, y0 = d['x0'], d['top']
            x1, y1 = d['x1'], d['bottom']

            x1_new = x0
            x2_new = x0 + wid  # регулирует ширину бокса

            y1_new = y1 - 3 * (y1 - y0)
            y2_new = y1
            return True, (x1_new, y1_new, x2_new, y2_new)

        return False, ()

def process_pdf_files(folder_path, coordinates):
    result = {}

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(folder_path, file_name)
            statement_names = {}
            i = 1  # Нумеруем ключи в соответствии с Пронумерованным М-11
            for coord in coordinates:
                statement_name = extract_statement_name(file_path, *coord)
                if statement_name:
                    statement_names[i] = statement_name.replace("\n", " ")  # Тут добавим в будущем регулярные выражения
                    i += 1  # Увеличиваем счетчик ключа

            result.update(statement_names)
            result.update(process_between_tables(file_path))

    return result


def unparse_pdf(folder_path, output_folder):
    # Проверяем, существует ли папка "11_output". Если нет, создаем ее.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_file_path = os.path.join(folder_path, filename)
            pdf_file_name = os.path.splitext(filename)[0]
            output_json_file = os.path.join(output_folder, f"{pdf_file_name}.json")
            result = []  # Список для хранения данных

            with pdfplumber.open(pdf_file_path) as pdf:
                for page in pdf.pages:
                    page_data = {"Страница": page.page_number, "Таблицы": []}
                    for table in page.extract_tables():
                        table_data = []
                        cell_number = 1
                        for row in table:
                            row_data = {}
                            for index, cell in enumerate(row):
                                cleaned_cell = cell.replace("\n", " ") if cell else None
                                row_data[f"Ячейка {cell_number}"] = cleaned_cell
                                cell_number += 1
                            table_data.append(row_data)
                        page_data["Таблицы"].append(table_data)
                    result.append(page_data)

            with open(output_json_file, "w", encoding="utf-8") as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=4)

            return output_json_file
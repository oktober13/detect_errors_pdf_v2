# API. Автоматизация обработки бухгалтерских документов

## Описание проекта

Процесс от создания реестра приема-передачи до регистрации документов в бухгалтерском учете может быть долгим и подвержен ошибкам, 
особенно из-за человеческого фактора. Наш проект предоставляет решение для автоматизации этого процесса, 
включая анализ документов на корректность и правильность заполненных данных, 
а также преобразование информации с документов в необходимый формат для дальнейшей работы.

## Состав проекта

`main.py`: Основной файл приложения FastAPI, который предоставляет API для обработки документов.

`models.py`: Описывает модели данных, которые используются для хранения информации о документах и других сущностях.

`crud.py`: Содержит функции для взаимодействия с базой данных, включая добавление документов и выполнение различных запросов.

`database.py`: Инициализирует базу данных, настраивает соединение с ней и предоставляет объект сессии для работы с базой данных.

`parse_to_dicts.py`: Содержит функции для парсинга данных из PDF-файлов и преобразования их в структурированный формат, который будет использоваться для дальнейшей обработки.

`process_pdf.py`: Включает функции для извлечения данных из PDF-файлов, а также для конвертации данных в формат JSON.

`validator.py`: Содержит функции для валидации данных из документов формы M-11 и формы ФМУ-76, проверяя номер документа, наименование организации, ОКПО и другие аспекты.

## Зависимости и установка

```
pip install -r requirements.txt
```

## Инструкции по использованию

Настройка базы данных: Сначала настройте базу данных, указав путь к вашей базе данных SQLite в файле `database.py`.

Запуск приложения: Запустите FastAPI-приложение с помощью команды:
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
### 1. Загрузка PDF-файлов: Положите ваши PDF-файлы в папку `M-11Pdf` или `FMU-76Pdf`.

### 2. Обработка и валидация документов:
Используйте метод `POST /forcedoc`, чтобы обработать и добавить документы в базу данных.
Используйте метод `POST /checkdoc`, чтобы проверить и валидировать документы.
### 3. Получение результатов: Ваши обработанные данные будут храниться в базе данных, 
и вы можете выполнить различные запросы с использованием методов, предоставляемых в файле `crud.py`.

## Лицензия

 Использование данного продукта не треубет лицензии.

## Команда разработки

AI Wizardry.
 
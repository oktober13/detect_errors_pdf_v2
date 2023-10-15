import datetime
from crud import search_okpo, search_structural_division, search_structural_division_be

org_prefix = ['АО', 'ИП', 'ОАО', 'ООО']

def validate_m_11(db, docInfo, df_forms, df_table1, df_table2):
    validation_msg = []
    validation_result = True

    if not(docInfo[1]) or docInfo[1] == '-':
        validation_msg.append('Номер документа не может быть пустым')
        validation_result = False

    if not(docInfo[2].startswith(tuple(org_prefix))):
        validation_msg.append('Наименование организации не начинается на АО, ИП, ОАО, ООО')

    if not(search_okpo(db, df_forms['Форма по ОКПО'].iloc[0])):
        validation_msg.append('Окпо не найден в базе данных')

    if not(docInfo[3]) or docInfo[3] == '-' or not(search_structural_division(db, docInfo[3])):
        validation_msg.append('Структурное подразделение не найдено в базе данных')

    if not(df_forms['БЕ'].iloc[0]) or df_forms['БЕ'].iloc[0] == '-' or not(search_structural_division_be(db, df_forms['БЕ'].iloc[0])):
        validation_msg.append('Структурное подразделение (Код) не найдено в базе данных')

    for row in range(len(df_table1)):
        try:
            _ = datetime.datetime.strptime(df_table1.loc[row, 'Дата составления'], '%d.%m.%Y')
        except ValueError:
            validation_msg.append(f'Строка {df_table1.loc[row, "Дата составления"]} не редставлена в виде dd.mm.yyyy')

    return validation_result, validation_msg

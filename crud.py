from sqlalchemy.orm import Session

import models

def add_document(db: Session, docInfo, df1, df2, df3):
    doc = models.DocumentM_11(documentNumber=docInfo[1],
                               organization=docInfo[2],
                               organizationOKPO=df1['Форма по ОКПО'].iloc[0],
                               structuralDivision=docInfo[3],
                               structuralDivisionBE=df1['БЕ'].iloc[0],
                               requestedPersone=docInfo['Затребовал'],
                               allowedPerson=docInfo['Разрешил'],
                               throughPersone=docInfo['Через'],
                               )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    add_deliveries(db, df2, doc)
    add_dtable_rows(db, df3, doc)
    return doc

def add_deliveries(db: Session, df2, doc):
    for row in range(len(df2)):
        delivery = models.DocumentM_11_Deliveries(dateOfCompilation=df2.loc[row, 'Дата составления'],
                                                  operationTypeCode=df2.loc[row,'Код вида операции'],
                                                  senderStructuralUnit=df2.loc[row,'Отправитель. Структурное подраздение'],
                                                  senderServiceNumber=df2.loc[row,'Отправитель. Табельный номер МОЛ (ЛОС)'],
                                                  recipientStructuralUnit=df2.loc[row,'Получатель. Структурное подразделение'],
                                                  recipientServiceNumber=df2.loc[row,'Получатель. Табельный номер МОЛ (ЛОС)'],
                                                  subAccount=df2.loc[row,'Корреспондирующий счет. Счет, субсчет'],
                                                  analyticalAccountingCode=df2.loc[row,'Корреспондирующий счет. Код аналитического учета'],
                                                  accountingUnitOfOutput=df2.loc[row,'Учетная единица выпуска продукции (работ, услуг)']
                                                  )
        db.add(delivery)
        db.commit()

def add_dtable_rows(db: Session, df3, doc):
    for row in range(len(df3)):
        table_row = models.DocumentM_11_TableRows(correspondingAccount=df3.loc[row, 'Корреспондирующий счет'],
                                                 materialComponents=df3.loc[row, 'Материальные ценности. наименование'],
                                                 materialNumber=df3.loc[row, 'Материальные ценности. номенклатурный номер'],
                                                 characteristicDesc=df3.loc[row, 'Характеристика'],
                                                 factoryNumber=df3.loc[row, 'Заводской номер'],
                                                 inventoryNumber=df3.loc[row, 'Инвентарный номер'],
                                                 networkNumber=df3.loc[row, 'Сетевой номер'],
                                                 measurementCode=df3.loc[row, 'Единица изменения. Код'],
                                                 measurementName=df3.loc[row, 'Единица изменения. Наименование'],
                                                 numberOfRequested=df3.loc[row, 'Количество. Затребовано'],
                                                 numberOfReleased=df3.loc[row, 'Количество. Отпущено'],
                                                 priceInRubles=df3.loc[row, 'Цена'],
                                                 amountWithoutVAT=df3.loc[row, 'Сумма без учета НДС'],
                                                 serialNumberWarehouse=df3.loc[row, 'Порядковый номер по складской картотеке'],
                                                 placeDesc=df3.loc[row, 'Местонахождение'],
                                                 registrationNumber=df3.loc[row, 'Регистрационный номер партии товара, подлежащего прослеживаемости']
                                                 )
        db.add(table_row)
        db.commit()

def add_okpo(db: Session, okpo_given):
    okpo = models.OKPO(okpo=okpo_given)
    db.add(okpo)
    db.commit()

def search_okpo(db: Session, okpo):
    return db.query(models.OKPO).filter(models.OKPO.okpo.in_([okpo])).count() > 0

def search_structural_division(db: Session, structural_division):
    return db.query(models.DocumentM_11).filter(models.DocumentM_11.structuralDivision.in_([structural_division])).count() > 0

def search_structural_division_be(db: Session, structural_division_be):
    return db.query(models.DocumentM_11).filter(models.DocumentM_11.structuralDivisionBE.in_([structural_division_be])).count() > 0



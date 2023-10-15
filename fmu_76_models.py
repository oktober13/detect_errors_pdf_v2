from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, mapped_column

from database import Base

class DocumentM_76(Base):
    __tablename__ = "DocumentM_76"

    docID = Column(Integer, primary_key=True, autoincrement= True)
    documentNumber = Column(String, primary_key=False) #1
    organization = Column(String, primary_key=False) #2а
    organizationOKPO = Column(String, primary_key=False) #2b
    structuralDivision = Column(String, primary_key=False) #3a
    structuralDivisionBE = Column(String, primary_key=False) #3b
    requestedPersone = Column(String, primary_key=False) #11
    allowedPerson = Column(String, primary_key=False) #12
    throughPersone = Column(String, primary_key=False)#13

class DocumentM_11_Deliveries(Base):
    __tablename__ = "DocumentM_76_Deliveries"

    deliveryId = Column(Integer, primary_key=True, autoincrement= True)
    dateOfCompilation = Column(String, primary_key=False) #4
    operationTypeCode = Column(String, primary_key=False) #5
    senderStructuralUnit = Column(String, primary_key=False) #6
    senderServiceNumber = Column(String, primary_key=False) #7
    recipientStructuralUnit = Column(String, primary_key=False) #8
    recipientServiceNumber = Column(String, primary_key=False) #9
    subAccount = Column(String, primary_key=False) #28
    analyticalAccountingCode = Column(String, primary_key=False) #25
    accountingUnitOfOutput = Column(String, primary_key=False) #10

class DocumentM_11_TableRows(Base):
    __tablename__ = "DocumentM_76_TableRows"

    rowId = Column(Integer, primary_key=True, autoincrement= True)
    correspondingAccount = Column(String, primary_key=False) # 29
    materialComponents = Column(String, primary_key=False)  # 14
    materialNumber = Column(String, primary_key=False) # 15
    characteristicDesc = Column(String, primary_key=False)  # 16
    factoryNumber = Column(String, primary_key=False)  # 17
    inventoryNumber = Column(String, primary_key=False)  # 30
    networkNumber = Column(String, primary_key=False)  # 31
    measurementCode = Column(String, primary_key=False)  # 18
    measurementName = Column(String, primary_key=False)  # 19
    numberOfRequested = Column(String, primary_key=False)  # 20
    numberOfReleased = Column(String, primary_key=False)  # 21
    priceInRubles = Column(String, primary_key=False)  # 26
    amountWithoutVAT = Column(String, primary_key=False)  # 27
    serialNumberWarehouse = Column(String, primary_key=False)  # 22
    placeDesc = Column(String, primary_key=False)  # 32
    registrationNumber = Column(String, primary_key=False)  # 33

class OKPO(Base):
    __tablename__ = "OKPO"

    okpoId = Column(Integer, primary_key=True, autoincrement= True)
    okpo = Column(String, primary_key=False)
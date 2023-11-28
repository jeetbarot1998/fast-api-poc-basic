from sqlalchemy.orm import Session


def add_into_table_with_dict(tableObj, dbObj: Session, data:dict):
    new_data = tableObj(**data)
    dbObj.add(new_data)
    dbObj.commit()
    return True

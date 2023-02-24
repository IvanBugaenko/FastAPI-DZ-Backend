from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.operations import Operations
from src.models.tanks import Tanks
from src.models.products import Products
from src.models.schemas.operations.operations_request import OperationsRequest
from datetime import datetime
import csv
from io import StringIO
from typing import BinaryIO


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session


    def all(self) -> List[Operations]:
        operations = (
            self.session
                .query(Operations)
                    .order_by(Operations.id.asc())
                        .all()
        )

        return operations
    

    def get(self, operation_id: int) -> Operations:
        operation = (
            self.session
                .query(Operations)
                    .filter(Operations.id == operation_id)
                        .first()
        )

        return operation


    def add(self, operations_schema: OperationsRequest, creating_id: int) -> Operations:
        operation = Operations(**operations_schema.dict())
        operation.created_by = creating_id
        self.session.add(operation)
        self.session.commit()

        return operation
    

    def update(self, operation_id: int, operations_schema: OperationsRequest, modifying_id: int) -> Operations:
        operation = self.get(operation_id)
        for field, value in operations_schema:
            if value and value != 0:
                setattr(operation, field, value)

        operation.modified_by = modifying_id
        operation.modified_at = datetime.now()
        
        self.session.commit()

        return operation
    

    def delete(self, operation_id: int) -> None:
        operation = self.get(operation_id)
        self.session.delete(operation)
        self.session.commit()


    def find_by_tank(self, tank_id: int) -> List[Operations]:
        operations = (
            self.session
                .query(Operations)
                    .filter(Operations.tank_id == tank_id)
                        .order_by(Operations.id.asc())
                            .all()
        )

        return operations
    

    def download(self, tank_id: int, product_id: int, date_start: datetime, date_end: datetime):
        operations = (
            self.session
                .query(Operations)
                    .filter(Operations.tank_id == tank_id, 
                            Operations.product_id == product_id,
                            Operations.date_start >= date_start,
                            Operations.date_end <= date_end
                    )
                        .order_by(Operations.id.asc())
                            .all()
        )

        columns_name = Operations.__table__.columns.keys()

        list = [dict([(key, row.__dict__[key]) for key in columns_name]) for row in operations]

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=columns_name)
        writer.writeheader()

        for row in list:
            writer.writerow(row)
        output.seek(0)

        return output

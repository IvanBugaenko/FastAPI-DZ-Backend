from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.tanks import Tanks
from src.models.schemas.tanks.tanks_request import TanksRequest
from datetime import datetime


class TanksService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session


    def all(self) -> List[Tanks]:
        tanks = (
            self.session
                .query(Tanks)
                    .order_by(Tanks.id.asc())
                        .all()
        )

        return tanks
    

    def get(self, tank_id: int) -> Tanks:
        tank = (
            self.session
                .query(Tanks)
                    .filter(Tanks.id == tank_id)
                        .first()
        )

        return tank


    def add(self, tanks_schema: TanksRequest, creating_id: int) -> Tanks:
        tank = Tanks(**tanks_schema.dict())
        tank.created_by = creating_id
        self.session.add(tank)
        self.session.commit()

        return tank
    

    def update(self, tank_id: int, tanks_schema: TanksRequest, modifying_id: int) -> Tanks:
        tank = self.get(tank_id)
        for field, value in tanks_schema:
            if value and value != 0:
                setattr(tank, field, value)

        tank.modified_by = modifying_id
        tank.modified_at = datetime.now()

        self.session.commit()

        return tank
    

    def delete(self, tank_id: int) -> None:
        tank = self.get(tank_id)
        self.session.delete(tank)
        self.session.commit()


    def update_current_capacity(self, tank_id: int, new_capacity: float, modifying_id: int) -> Tanks:
        tank = self.get(tank_id)
        tank.current_capacity = new_capacity

        tank.modified_by = modifying_id
        tank.modified_at = datetime.now()

        self.session.commit()

        return tank

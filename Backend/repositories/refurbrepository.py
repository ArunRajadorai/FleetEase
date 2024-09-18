import json
import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from ..models.refurb import Refurbishment
from ..models.vehicle import Vehicle
from ..schemas.refurbschema import RefurbishmentCreate, RefurbishmentCreateResponse


class RefurbRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_refurbishment(self, refurbishment: RefurbishmentCreate):
        try:
            # Create a new Refurbishment record
            db_refurbishment = Refurbishment(
                user_id=refurbishment.user_id,
                vehicle_id=refurbishment.vehicle_id,
                service_description=refurbishment.service_description,
                service_type=refurbishment.service_type,
                status=refurbishment.status,
                created_at=datetime.datetime.now()
            )
            self.db.add(db_refurbishment)

            # Update the status in the Vehicle table
            self.db.query(Vehicle).filter(Vehicle.vehicle_id == refurbishment.vehicle_id).update(
                {Vehicle.status: 'Refurbishment Scheduled'}
            )

            # Commit the changes
            self.db.commit()
            self.db.refresh(db_refurbishment)
            return RefurbishmentCreateResponse(refurbishment_id=db_refurbishment.refurbishment_id)

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error creating refurbishment: {e}")
            return None


    def get_refurbishment(self, refurbishment_id: int):
        return self.db.query(Refurbishment).filter(Refurbishment.refurbishment_id == refurbishment_id).first()

    def get_refurbishments_by_user(self, user_id: int):
        return self.db.query(Refurbishment).filter(Refurbishment.user_id == user_id).all()

    # def update_refurbishment(self, refurbishment_id: int, refurbishment_update: RefurbishmentUpdate):
    #     db_refurbishment = self.get_refurbishment(refurbishment_id)
    #     if not db_refurbishment:
    #         return None
    #
    #     if refurbishment_update.service_type is not None:
    #         db_refurbishment.service_type = refurbishment_update.service_type
    #     if refurbishment_update.spare_parts is not None:
    #         db_refurbishment.spare_parts = refurbishment_update.spare_parts
    #     if refurbishment_update.estimated_cost is not None:
    #         db_refurbishment.estimated_cost = refurbishment_update.estimated_cost
    #     if refurbishment_update.date is not None:
    #         db_refurbishment.date = refurbishment_update.date
    #     if refurbishment_update.time is not None:
    #         db_refurbishment.time = refurbishment_update.time
    #     if refurbishment_update.status is not None:
    #         db_refurbishment.status = refurbishment_update.status
    #
    #     self.db.commit()
    #     self.db.refresh(db_refurbishment)
    #     return db_refurbishment
    #
    # def delete_refurbishment(self, refurbishment_id: int):
    #     db_refurbishment = self.get_refurbishment(refurbishment_id)
    #     if not db_refurbishment:
    #         return None
    #
    #     self.db.delete(db_refurbishment)
    #     self.db.commit()
    #     return db_refurbishment

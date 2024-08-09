from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from ..models.refurb import Refurbishment
from ..schemas.refurbmentschema import RefurbishmentCreate, RefurbishmentUpdate

class RefurbRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_refurbishment(self, refurbishment: RefurbishmentCreate):
        db_refurbishment = Refurbishment(
            user_id=refurbishment.user_id,
            center_id=refurbishment.center_id,
            service_type=refurbishment.service_type,
            spare_parts=refurbishment.spare_parts,
            estimated_cost=refurbishment.estimated_cost,
            date=refurbishment.date,
            time=refurbishment.time,
            status=refurbishment.status
        )
        self.db.add(db_refurbishment)
        self.db.commit()
        self.db.refresh(db_refurbishment)
        return db_refurbishment

    def get_refurbishment(self, refurbishment_id: int):
        return self.db.query(Refurbishment).filter(Refurbishment.refurbishment_id == refurbishment_id).first()

    def get_refurbishments_by_user(self, user_id: int):
        return self.db.query(Refurbishment).filter(Refurbishment.user_id == user_id).all()

    def update_refurbishment(self, refurbishment_id: int, refurbishment_update: RefurbishmentUpdate):
        db_refurbishment = self.get_refurbishment(refurbishment_id)
        if not db_refurbishment:
            return None

        if refurbishment_update.service_type is not None:
            db_refurbishment.service_type = refurbishment_update.service_type
        if refurbishment_update.spare_parts is not None:
            db_refurbishment.spare_parts = refurbishment_update.spare_parts
        if refurbishment_update.estimated_cost is not None:
            db_refurbishment.estimated_cost = refurbishment_update.estimated_cost
        if refurbishment_update.date is not None:
            db_refurbishment.date = refurbishment_update.date
        if refurbishment_update.time is not None:
            db_refurbishment.time = refurbishment_update.time
        if refurbishment_update.status is not None:
            db_refurbishment.status = refurbishment_update.status

        self.db.commit()
        self.db.refresh(db_refurbishment)
        return db_refurbishment

    def delete_refurbishment(self, refurbishment_id: int):
        db_refurbishment = self.get_refurbishment(refurbishment_id)
        if not db_refurbishment:
            return None

        self.db.delete(db_refurbishment)
        self.db.commit()
        return db_refurbishment

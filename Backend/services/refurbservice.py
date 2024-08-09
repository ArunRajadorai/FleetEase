from sqlalchemy.orm import Session
from ..schemas.refurbschema import RefurbishmentCreate, RefurbishmentUpdate
from ..repositories.refurbrepository import RefurbishmentRepository

class RefurbService:
    def __init__(self, refurbishment_repository: RefurbishmentRepository):
        self.refurbishment_repository = refurbishment_repository

    def create_refurbishment(self, refurbishment: RefurbishmentCreate):
        return self.refurbishment_repository.create_refurbishment(refurbishment)

    def get_refurbishment(self, refurbishment_id: int):
        return self.refurbishment_repository.get_refurbishment(refurbishment_id)

    def get_refurbishments_by_user(self, user_id: int):
        return self.refurbishment_repository.get_refurbishments_by_user(user_id)

    def update_refurbishment(self, refurbishment_id: int, refurbishment_update: RefurbishmentUpdate):
        return self.refurbishment_repository.update_refurbishment(refurbishment_id, refurbishment_update)

    def delete_refurbishment(self, refurbishment_id: int):
        return self.refurbishment_repository.delete_refurbishment(refurbishment_id)

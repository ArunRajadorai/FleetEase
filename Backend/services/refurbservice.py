from sqlalchemy.orm import Session
from ..schemas.refurbschema import RefurbishmentCreate
from ..repositories.refurbrepository import RefurbRepository


class RefurbService:
    def __init__(self, refurbishment_repository: RefurbRepository):
        self.refurbishment_repository = refurbishment_repository

    def create_refurbishment(self, refurbishment: RefurbishmentCreate):
        return self.refurbishment_repository.create_refurbishment(refurbishment)

    def get_refurbishment(self, refurbishment_id: int):
        return self.refurbishment_repository.get_refurbishment(refurbishment_id)

    def get_refurbishments_by_user(self, user_id: int):
        return self.refurbishment_repository.get_refurbishments_by_user(user_id)

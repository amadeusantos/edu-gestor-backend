from pydantic import BaseModel, EmailStr
from core.infrastructure.database.tables import RoleEnum, User


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum

    
    def to_row(self) -> User:
        return User(
            email=str(self.email),
            password=self.password,
            role=self.role,
        )

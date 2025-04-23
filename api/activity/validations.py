from api.activity.exceptions import ActivityProfessorIdException
from api.activity.schemas import ActivityCreateSchema
from api.schemas import UserPrincipal
from infrastructure.persistence.enums import RoleEnum


def validate_create_activities(activity: ActivityCreateSchema, user_principal: UserPrincipal):
    if user_principal.role == RoleEnum.COORDINATOR.value or user_principal.role == RoleEnum.ADMIN.value:
        print(user_principal.role)
        if not activity.professor_id:
            raise ActivityProfessorIdException()
        return activity

    activity.professor_id = user_principal.professor_id
    return activity
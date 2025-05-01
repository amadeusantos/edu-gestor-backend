from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.authentication import Authorizations
from api.schemas import UserPrincipal
from api.score.exceptions import ScoreNotFoundException
from api.score.schemas import ScoreUpdateSchema, ScoreSchema
from infrastructure.persistence.db_session import open_db_session
from infrastructure.persistence.enums import RoleEnum
from infrastructure.persistence.models import ScoreModel

router = APIRouter(prefix="/scores", tags=["Score"])

def query_scores(session: Session):
    return session.query(ScoreModel).where(ScoreModel.deleted == False)


def query_first(session: Session, id: UUID):
    query = query_scores(session)
    score = query.where(ScoreModel.id == id).first()

    if not score:
        raise ScoreNotFoundException()

    return score

@router.put("/{id}")
def update_score(id: UUID, dto: ScoreUpdateSchema, session: Session = Depends(open_db_session),
        user_principal: UserPrincipal = Depends(
            Authorizations([RoleEnum.ADMIN, RoleEnum.COORDINATOR, RoleEnum.PROFESSOR])))-> ScoreSchema:
    score = query_first(session, id)
    if dto.is_absent:
        session.query(ScoreModel).where(ScoreModel.id == score.id).update(dto.model_dump())
    else:
        session.query(ScoreModel).where(ScoreModel.id == score.id).update(dto.model_dump())
    session.commit()
    session.refresh(score)
    return score
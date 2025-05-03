import math
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from api.student.schemas import StudentInfoPaginationSchema
from infrastructure.persistence.models import FrequencyModel, DisciplineModel, ScoreModel, ExamModel, StudentModel, \
    ClassroomModel


def get_info(session: Session, student_id: UUID, page: int, size: int) -> StudentInfoPaginationSchema:

    query = session.query(DisciplineModel).where(
        DisciplineModel.deleted == False,
        DisciplineModel.archived == False,
        DisciplineModel.classroom.has(ClassroomModel.students.any(StudentModel.id == student_id))
    ).order_by(DisciplineModel.id)

    total_items = query.count()
    total_pages = math.ceil(total_items / size)
    disciplines = query.offset((page - 1) * size).limit(size).all()

    disciplines_ids = [discipline.id for discipline in disciplines]

    classes = session.query(FrequencyModel.discipline_id, func.count(FrequencyModel.id).label("classes")).where(
        FrequencyModel.deleted == False,
        FrequencyModel.archived == FrequencyModel.archived == False,
        FrequencyModel.discipline_id.in_(disciplines_ids),
    ).group_by(FrequencyModel.discipline_id).order_by(FrequencyModel.discipline_id).all()

    faults = session.query(FrequencyModel.discipline_id, func.count(FrequencyModel.id).label("faults")).where(
        FrequencyModel.deleted == False,
        FrequencyModel.archived == FrequencyModel.archived == False,
        FrequencyModel.discipline_id.in_(disciplines_ids),
        ~FrequencyModel.presents.any(StudentModel.id != student_id)
    ).group_by(FrequencyModel.discipline_id).order_by(FrequencyModel.discipline_id).all()

    results = []
    for index, discipline in enumerate(disciplines):
        count_exams = session.query(ExamModel).where(
            ExamModel.deleted == False,
            ExamModel.archived == False,
            ExamModel.is_finish == True,
            ExamModel.discipline_id == discipline.id
        ).count()

        scores = session.query(ScoreModel).join(ExamModel).where(
            ScoreModel.deleted == False,
            ScoreModel.archived == False,
            ExamModel.is_finish == True,
            ExamModel.discipline_id == discipline.id,
            ScoreModel.student_id == student_id,
        ).all()

        results.append(
            dict(
                discipline_id=discipline.id,
                discipline_name=discipline.name,
                professor_name=discipline.professor.fullname,
                faults=next((fault[1] for fault in faults if fault[0] == discipline.id), 0),
                classes=next((classe[1] for classe in classes if classe[0] == discipline.id), 0),
                average_grade=round(sum(map(lambda x: x.value, scores), 0) / count_exams if count_exams != 0 else 0, 2)
            )
        )


    return {"total_items":total_items, "total_pages": total_pages, "page": page, "size": size, "results": results}

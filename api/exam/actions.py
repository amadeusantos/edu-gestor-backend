from sqlalchemy.orm import Session

from infrastructure.persistence.models import ExamModel, StudentModel, ScoreModel, ActivityModel


def sync_students(session: Session, exam_create: ExamModel):
    students = session.query(StudentModel).where(StudentModel.classroom_id == exam_create.discipline.classroom_id).all()
    students_ids = [student.id for student in students]
    exam_students_ids = [score.student_id for score in exam_create.scores]
    new_students = [id for id in students_ids if not id in exam_students_ids]
    scores = [session.add(ScoreModel(student_id=student, value=0, exam_id=exam_create.id)) for student in new_students]
    session.flush()


def create_activity(session: Session, exam: ExamModel):
    activity = ActivityModel(title=exam.title, description=f"Prova de {exam.discipline.name}", is_exam=True,
                             date=exam.date, disciplines=[exam.discipline], professor_id=exam.discipline.professor_id)
    session.add(activity)
    exam.activity = activity
    session.flush()


def update_activity(session: Session, exam: ExamModel):
    session.query(ActivityModel).where(ActivityModel.id == exam.activity_id).update(
        {"title": exam.title, "date": exam.date,
         "professor_id": exam.discipline.professor_id})
    session.flush()

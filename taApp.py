from app import app
from app.models import Professor, Student, Course

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Professor': Professor, 'Student': Student, 'Course': Course}
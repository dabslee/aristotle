from ..models import Course
import datetime

# utility functions
def dateConvert(date_in):
    try:
        date_processing = date_in.replace('T', '-').replace(':', '-').split('-')
        date_processing = [int(v) for v in date_processing]
        return datetime.datetime(*date_processing)
    except ValueError:
        return None

def alwaysContext(request):
    return {
        "username": request.user.username,
        "selected_course": Course.objects.filter(id=request.session.get('selected_course_id')).first()
    }
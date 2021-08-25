# Run in Django shell `python manage.py shell`

from forum.models import Assignment, Submission

for assn in Assignment.objects.all():
    try:
        print(assn.description.html)
    except:
        oldstr = assn.description.json_string
        oldstr = oldstr.replace("\n","<br>")
        assn.description.json_string = "{\"delta\":\"\",\"html\":\"" + oldstr + "\"}"
        assn.save()

for sub in Submission.objects.all():
    try:
        print(sub.details.html)
    except:
        oldstr = sub.details.json_string
        oldstr = oldstr.replace("\n","<br>")
        sub.details.json_string = "{\"delta\":\"\",\"html\":\"" + oldstr + "\"}"
        sub.save()

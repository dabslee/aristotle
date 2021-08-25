# Run in Django shell `python manage.py shell`

from forum.models import Assignment

for assn in Assignment.objects.all():
    try:
        print(assn.description.html)
    except:
        oldstr = assn.description.json_string
        oldstr = oldstr.replace("\n","<br>")
        assn.description.json_string = "{\"delta\":\"\",\"html\":\"" + oldstr + "\"}"
        assn.save()
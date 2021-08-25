# Run in Django shell `python manage.py shell`

from forum.models import Assignment, Submission
import django_quill

for assn in Assignment.objects.all():
    try:
        oldstr = assn.description.html
        newstr = ""
        for line in oldstr.split("   |\r\n"):
            newstr += f"<p>{line}</p>"
        newstr.replace("\r\n", "")
        assn.description.json_string = "{\"delta\":\"\",\"html\":\"" + newstr + "\"}"
        assn.save()
    except:
        try:
            oldstr = assn.description.json_string
            oldstr = oldstr.replace("   ","<br>")
            assn.description.json_string = "{\"delta\":\"\",\"html\":\"" + oldstr + "\"}"
            assn.save()
        except django_quill.quill.QuillParseError as e:
            print(e)

for sub in Submission.objects.all():
    try:
        print(sub.details.html)
    except:
        oldstr = sub.details.json_string
        oldstr = oldstr.replace("\n","<br>")
        sub.details.json_string = "{\"delta\":\"\",\"html\":\"" + oldstr + "\"}"
        sub.save()

for assn in Assignment.objects.all():
    print(assn.id)
    try:
        oldstr = assn.description.html
    except:
        oldstr = assn.description.json_string
    newstr = ""
    for line in oldstr.replace("\r","").replace("\n","   ").split("   "):
        if not "<p>" in newstr:
            newstr += f"<p>{line}</p>"
        else:
            newstr += {line}
    newstr = newstr.replace("\"","\'")
    thestr = "{\"delta\":\"\",\"html\":\"" + newstr + "\"}"
    assn.description.json_string = thestr
    print(thestr)
    assn.save()
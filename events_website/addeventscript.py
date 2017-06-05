from events.models import *
from login.views import *

VALID_KEY_CHARS = string.ascii_lowercase

def addevent(number,startnumber=0, date='2017-06-02'):
    for i in range(startnumber, number):
        name = "Event %s" % i
        location = get_random_string(10, VALID_KEY_CHARS)
        description = get_random_string(50, VALID_KEY_CHARS)
        instance = event(name=name, location=location, date=date, description=description)
        instance.save()

#sometest
from .util import get_groups
import datetime

today = datetime.date.today()


def groups_processor(request):
    return {'GROUPS': get_groups(request)}


def year(request):
    return {'YEAR': today.strftime("%Y")}

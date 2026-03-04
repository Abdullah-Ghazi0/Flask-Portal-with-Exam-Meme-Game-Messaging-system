from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

def date_formater(og_date):
    og_date = og_date.replace(tzinfo=timezone.utc)
    local_date = og_date.astimezone()
    td = datetime.today().astimezone()

    date_diff = td.date() - local_date.date()
    
    if date_diff.days == 0:
        date = "Today"

    elif date_diff.days == 1:
        date = "Yesterday"

    elif date_diff < timedelta(days=7):
        date = local_date.strftime("%A")
    
    else:
        date = local_date.strftime("%#d %B %Y")
    
    return date

def time_formater(og_time):
    og_time = og_time.replace(tzinfo=timezone.utc)
    local_time = og_time.astimezone()
    formated_time = local_time.strftime("%I:%M %p").lower()
    return formated_time

def chat_time(msg_time=None):
    msg_time = msg_time.replace(tzinfo=timezone.utc)
    localtime_of_msg = msg_time.astimezone()
    td = datetime.today().astimezone()
    
    date_diff = td.date() - localtime_of_msg.date()
    if date_diff.days == 0:
        time = localtime_of_msg.strftime("%I:%M %p").lower()

    elif date_diff.days == 1:
        time = "Yesterday"

    elif date_diff < timedelta(days=7):
        time = localtime_of_msg.strftime("%A")
        
    else:
        time = localtime_of_msg.strftime("%d/%m/%Y")


    return time


def msg_date(all_msgs):
    last_msg_date  = None
    for msg in all_msgs:
        if msg.time.date() == last_msg_date:
            msg.datetime = [time_formater(msg.time)]
        else:
            msg.datetime = [time_formater(msg.time), date_formater(msg.time)]
            last_msg_date = msg.time.date()

    return all_msgs
import datetime

def get_current_time() -> str:
    return datetime.datetime.now().strftime("%I:%M %p")

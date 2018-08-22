import re
from datetime import datetime

LOG_FILE_PATH = '/Projects/Log Beautifier/src/log.txt'
timestamp_rgx = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}'
log_level_rgx = r'INFO|ERROR|WARN|TRACE|DEBUG|FATAL'
thread_rgx = r'\[.+?(?= :)'
message_rgx = r'(?<=: ).*$'


class Log:
    def __init__(self, timestamp, log_level, thread, message):
        self.timestamp = timestamp
        self.log_level = log_level
        self.thread = thread
        self.message = message


def read_file(path):

    fd = open(path, 'r')
    content = fd.read()
    fd.close()
    return content


def extract_fields():

    events = []
    content = read_file(LOG_FILE_PATH)
    log_events = content.split('\n')
    for i, event in enumerate(log_events):
        event = re.sub(r'\s\s+', ' ', event)
        timestamp = datetime.strptime(str(re.search(timestamp_rgx, event).group(0)), '%Y-%m-%d %H:%M:%S.%f')
        log_level = re.search(log_level_rgx, event).group(0)
        thread = re.search(thread_rgx, event).group(0)
        message = re.search(message_rgx, event).group(0)
        log = Log(timestamp, str(log_level), str(thread), str(message))
        events.append(log)
        print(f'LOG #{i}: {events[i].timestamp}, {events[i].log_level}, {events[i].thread}, {events[i].message}')
    return events


def filter(log, start_time=None, end_time=None, level=None, thread_name=None):

    if start_time is not None and end_time is not None:
        print(f'Found between {start_time} and {end_time}')
        for event in log:
            if end_time > event.timestamp > start_time:
                print(f'{event.timestamp}, {event.log_level}, {event.thread}, {event.message}')

    if level is not None:
        print(f'Found {level}')
        for event in log:
            if event.log_level == level:
                print(f'{event.timestamp}: {event.log_level}, {event.thread}, {event.message}')

    if thread_name is not None:
        print(f'Found in {thread_name}')
        for event in log:
            if thread_name in event.thread:
                print(f'{event.timestamp}: {event.log_level}, {event.thread}, {event.message}')

    return None
import re
import logging
from datetime import datetime

LOG_FILE_PATH = '/Projects/Log Beautifier/libs/log.txt'
timestamp_rgx = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}'
log_level_rgx = r'INFO|ERROR|WARN|TRACE|DEBUG|FATAL'
thread_rgx = r'\[.+?(?= :)'
message_rgx = r'(?<=: ).*(?=\n)'
stack_trace_rgx = r'(?<=\n\s).*'


class Log:
    def __init__(self, timestamp, log_level, thread, message, stack_trace=None):
        self.timestamp = timestamp
        self.log_level = log_level
        self.thread = thread
        self.message = message
        self.stack_trace = stack_trace


class Filter:
    def __init__(self, start_time, end_time, log_level=None, thread=None):
        self.start_time = start_time
        self.end_time = end_time
        self.log_level = log_level
        self.thread = thread


def read_file(path):

    fd = open(path, 'r')
    content = fd.read()
    fd.close()
    return content


def extract_fields(show_warnings=False):

    events = []
    content = read_file(LOG_FILE_PATH)
    event_log = re.split(r'(?=\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3})', content)
    for log_line in event_log:
        event = re.sub(r'  +', ' ', log_line)
        try:
            timestamp = datetime.strptime(str(re.search(timestamp_rgx, event).group(0)), '%Y-%m-%d %H:%M:%S.%f')
            log_level = re.search(log_level_rgx, event).group(0)
            thread = re.search(thread_rgx, event).group(0)
            message = re.search(message_rgx, event).group(0)
            try:
                stack_trace = re.search(stack_trace_rgx, event, re.DOTALL).group(0)
                log = Log(timestamp, str(log_level), str(thread), str(message), str(stack_trace))
            except AttributeError:
                log = Log(timestamp, str(log_level), str(thread), str(message))
            events.append(log)
        except AttributeError:
            if show_warnings:
                logging.warning(f'Skipped line: "{log_line}" because it does not fit the log event mask')
    return events


def request_filtering_attributes():

    print(u'Press enter on input if you don\'t need the filter')
    start_time_input = input('Enter time frame using format dd-MM-yyyy HH:mm.ss\nFrom: ')
    end_time_input = input('To: ')
    try:
        if start_time_input != '':
            start_time = datetime.strptime(start_time_input, '%d-%m-%Y %H:%M.%S')
        else:
            start_time = datetime(2000, 1, 1, 1, 0) # TODO remove this shitty hardcoded const :^)
        if end_time_input != '':
            end_time = datetime.strptime(end_time_input, '%d-%m-%Y %H:%M.%S')
        else:
            end_time = datetime.now()
    except ValueError:
        print(u'Wrong end time data format')

    log_level = input('Enter log level (INFO/ERROR/WARN/TRACE/DEBUG/FATAL): ').upper()
    if log_level == '':
        log_level = None

    thread = input('Enter a part of the thread name: ')
    if thread == '':
        thread = None

    filtering_attributes = Filter(start_time, end_time, log_level, thread)
    return filtering_attributes


def _filter_by_time(event, start_time, end_time):

    if end_time > event.timestamp > start_time:
        return True
    else:
        return False


def _filter_by_level(event, level):

    if event.log_level == level:
        return True
    else:
        return False


def _filter_by_thread(event, thread_name):

    if thread_name in event.thread:
        return True
    else:
        return False


def filter_events(log):

    attributes = request_filtering_attributes()
    if attributes.log_level is None and attributes.thread is None:
        print('No filter chosen')
        return None
    filtered_list = []
    for event in log:
        time_ok = _filter_by_time(event, attributes.start_time, attributes.end_time)
        if attributes.log_level is not None:
            level_ok = _filter_by_level(event, attributes.log_level)
        else:
            level_ok = True
        if attributes.thread is not None:
            thread_ok = _filter_by_thread(event, attributes.thread)
        else:
            thread_ok = True
        if time_ok and level_ok and thread_ok:
            filtered_list.append(event)
    if filtered_list.__len__() == 0:
        return None
    # add try-except
    return filtered_list

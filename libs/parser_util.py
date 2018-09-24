import re
import logging
from datetime import datetime
import time

content_splitter_rgx = r'(?<=\n)(?=\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3})'
timestamp_rgx = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}'
log_level_rgx = r'INFO|ERROR|WARN|TRACE|DEBUG|FATAL'
instance_rgx = r'\[.+?(?= :)'
message_rgx = r'(?<=:\s).*'
str_to_timestamp_converter_pattern = '%Y-%m-%d %H:%M:%S.%f'
extra_spaces_cleanup_rgx = r'  +'


class Log:
    def __init__(self, event_id, timestamp, log_level, instance, message, stack_trace=None):
        self.event_id = event_id
        self.timestamp = timestamp
        self.log_level = log_level
        self.instance = instance
        self.message = message
        self.stack_trace = stack_trace


class Filter:
    def __init__(self, start_time, end_time, log_level=None, instance=None):
        self.start_time = start_time
        self.end_time = end_time
        self.log_level = log_level
        self.instance = instance


def _try_read_file(path):

    try:
        fd = open(path, 'r', encoding='utf8')
        content = fd.read()
        fd.close()
        return content
    except:
        print(f'Error reading {path}')
        return None

def _try_split(content):
    try:
        event_log = re.split(content_splitter_rgx, content)
        return event_log
    except:
        print(f'Cannot detect log events')
        return None

def _try_extract_events(event_log):
    events = []
    event_id = 0
    for log_line in event_log:
        event = re.sub(extra_spaces_cleanup_rgx, ' ', log_line)
        try:
            timestamp = datetime.strptime(str(re.search(timestamp_rgx, event).group(0)),
                                          str_to_timestamp_converter_pattern)
            log_level = re.search(log_level_rgx, event).group(0)
            instance = re.search(instance_rgx, event).group(0)
            message = re.search(message_rgx, event, re.DOTALL).group(0)
            log = Log(event_id, timestamp, str(log_level), str(instance), str(message))
            events.append(log)
            event_id += 1
        except AttributeError:
            logging.warning(f'Skipped line: "{log_line}" because it does not fit the log event mask')
    if events.__len__() == 0:
        print("Looks like it's not a log file")
        return None
    else:
        return events


def parse_log_file(path):

    # TODO change to try-except
    content = _try_read_file(path)
    if content is not None:
        event_log = _try_split(content)
        if event_log is not None:
            events = _try_extract_events(event_log)
            if events is not None:
                return events
    return None


def _filter_by_time(event, start_time, end_time):

    if end_time > event.timestamp > start_time:
        return True
    else:
        return False


def _filter_by_level(event, log_level):

    for level in log_level:
        if event.log_level == level:
            return True
    return False


# TODO rewrite instance filtration algorithm
def filter_by_instances(results, instances):
    for instance in instances:
        if instance in results:
            return True
        else:
            return False


def filter_events(log, attributes):

    filtered_list = []
    for event in log:
        time_ok = _filter_by_time(event, attributes.start_time, attributes.end_time)
        if attributes.log_level is not None:
            level_ok = _filter_by_level(event, attributes.log_level)
        else:
            level_ok = True
        if time_ok and level_ok:
            filtered_list.append(event)
    if filtered_list.__len__() == 0:
        return None
    # add try-except
    return filtered_list

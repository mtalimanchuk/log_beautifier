import libs.utilities as util
import datetime
import libs.gui_graphics as gui
# import wx


def make_alias_name(url):
    if 'http://' in url:
        alias = url.replace('http://', '')
        return alias
    return ''


def try_parse_log_file(path):
    log = util.parse_log_file(path)
    return log


def create_filters(wx_start_date, wx_start_time, wx_end_date, wx_end_time, log_level):

    if wx_start_date.IsValid() and wx_start_time.IsValid() and wx_end_date.IsValid() and wx_end_time.IsValid():
        dt_start = datetime.datetime(wx_start_date.year, int(wx_start_date.month) + 1, wx_start_date.day,
                                     wx_start_time.hour, wx_start_time.minute, wx_start_time.second)
        dt_end = datetime.datetime(wx_end_date.year, int(wx_end_date.month) + 1, wx_end_date.day,
                                   wx_end_time.hour, wx_end_time.minute, wx_end_time.second)
        print(f'FILTERS:\nTIME: from {dt_start} to {dt_end}\n')
    else:
        print(u'Invalid DateTime value(s)')

    if len(log_level) == 0:
        print(f'Error: choose at least one log level filter')
        return None
    else:
        print(f'LOG LEVEL: {log_level}')

    filter_attributes = util.Filter(dt_start, dt_end, log_level)
    return filter_attributes



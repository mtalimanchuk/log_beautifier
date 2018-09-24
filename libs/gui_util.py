import libs.parser_util as util
import datetime
import libs.gui as gui
import wx
import wx.richtext


def set_config():
    config = wx.Config("Log Beautifier")
    return config

def load_recent_files_list(filehistory, config):

    recent_files = []
    filehistory.Load(config)
    for index in range(filehistory.GetCount()):
        recent_files.append(filehistory.GetHistoryFile(index))
    return recent_files

def save_config(config):
    sp = wx.StandardPaths.Get()
    cp = sp.GetConfigDir()
    config.Write('option_1', 'path')
    print(config.Read('option_1'))
    None

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


def fill_richText_control(frame, results_to_show):
    for line in results_to_show:
        frame.results_richText.BeginBold()

        frame.results_richText.BeginTextColour((0, 0, 0))
        frame.results_richText.WriteText(f'{str(line.timestamp)} ')
        frame.results_richText.EndTextColour()

        if line.log_level in ('ERROR', 'FATAL'):    colour = wx.Colour(255, 0, 0)
        elif line.log_level == 'WARN':              colour = wx.Colour(255, 153, 0)
        elif line.log_level in ('TRACE', 'DEBUG'):  colour = wx.Colour(64, 64, 64)
        elif line.log_level == 'INFO':              colour = wx.Colour(0, 153, 0)
        frame.results_richText.BeginTextColour(colour)
        frame.results_richText.WriteText(f'{line.log_level} ')
        frame.results_richText.EndTextColour()

        frame.results_richText.BeginTextColour((38, 77, 115))
        frame.results_richText.WriteText(f'{line.instance} ')
        frame.results_richText.EndTextColour()

        frame.results_richText.EndBold()

        # if '\n' is in log line msg more than twice, hide the message
        # Add this to a new container and operate accordingly
        frame.results_richText.BeginFontSize(8)
        message_short_end = line.message.find('\n')
        frame.results_richText.WriteText(f'{line.message[:message_short_end]}  ')
        if line.message.count('\n') > 1:
            frame.results_richText.BeginURL(line.message[message_short_end:])
            frame.results_richText.BeginUnderline()
            frame.results_richText.WriteText(f'[+] Show full message')
            frame.results_richText.EndUnderline()
            frame.results_richText.EndURL()
        frame.results_richText.EndFontSize()
        frame.results_richText.WriteText(f' \n')

        frame.results_richText.Bind(wx.EVT_TEXT_URL, frame.OnShowFullMessage)

def get_instance_list(results_to_show):
    instance_list = []
    for log_line in results_to_show:
        if not instance_list.__contains__(log_line.instance): instance_list.append(log_line.instance)
    return instance_list
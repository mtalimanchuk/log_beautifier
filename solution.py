import sys
import os
import libs.utilities as util
import libs.gui_util as ui
from fake_useragent import UserAgent

ui.run()
'''
# This works but testing out main menu
results = util.filter_events(log)
if results is not None:
    for event in results:
        print(f'Found {event.timestamp}, {event.log_level}, {event.instance}, {event.message}, {event.stack_trace}')
else:
    print(u'No results found')
input('Press any key')
'''
# TODO add fake useragent utility
'''
from fake_useragent import UserAgent
import requests


ua = UserAgent()
print(ua.chrome)
header = {'User-Agent':str(ua.chrome)}
print(header)
url = "https://www.hybrid-analysis.com/recent-submissions?filter=file&sort=^timestamp"
htmlContent = requests.get(url, headers=header)
print(htmlContent)
'''
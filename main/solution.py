import services.utilities as util
import datetime as dt

events_log = util.extract_fields()

start_time = dt.datetime(2018, 8, 21, 18, 29)
end_time = dt.datetime(2018, 8, 21, 18, 30)
util.filter(events_log, start_time, end_time)
util.filter(events_log, thread_name='deprecation')


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
from datetime import datetime as Datetime
import datetime

class UtilityService:
    def unix_time_to_datetime(self, unix_time):
        return Datetime.fromtimestamp(unix_time, datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y/%m/%d %H:%M:%S')
    
    
from datetime import tzinfo, timedelta, datetime
import time as _time

class LocalTimezone(tzinfo):
    def __init__(self):
        self.ZERO = timedelta(0)
        self.HOUR = timedelta(hours=1)
        self.STDOFFSET = timedelta(seconds = -_time.timezone)

        if _time.daylight:
            self.DSTOFFSET = timedelta(seconds = -_time.altzone)
        else:
            self.DSTOFFSET = self.STDOFFSET

        self.DSTDIFF = self.DSTOFFSET - self.STDOFFSET

    def utcoffset(self, dt):
        if self._isdst(dt):
            return self.DSTOFFSET
        else:
            return self.STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return self.DSTDIFF
        else:
            return self.ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0

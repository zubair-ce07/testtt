import six


class WeatherException(Exception):
    """Base Weather Exception.
    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = "An unknown exception occurred."

    def __init__(self, **kwargs):
        try:
            super(WeatherException, self).__init__(self.message % kwargs)
            self.msg = "Weather Exception: " + (self.message % kwargs)
        except Exception:
            super(WeatherException, self).__init__()

    if six.PY2:
        def __unicode__(self):
            return unicode(self.msg)

    def __str__(self):
        return self.msg


class InvalidMonthFormat(WeatherException):
    message = "(%(month)s) Invalid month format. Please follow: YYYY/MM"


class InvalidMonthRange(WeatherException):
    message = "(%(month)s) Month out of valid range: [1, 12]"


class InvalidYearInput(WeatherException):
    message = "(%(year)d) Invalid year input."

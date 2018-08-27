"""Start of the application"""

import sys
from weatherman_application import WeathermanApplication


app = WeathermanApplication(sys.argv[1])
app.do_the_dew(sys.argv)

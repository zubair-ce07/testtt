class DayInfo:
    def __init__(self, info):
        self.pkt = info[0] if info[0] != '' else None
        self.max_temp = int(info[1]) if info[1] != '' else None
        self.mean_temp = int(info[2]) if info[2] != '' else None
        self.min_temp = int(info[3]) if info[3] != '' else None
        self.mean_humidity = int(info[8]) if info[8] != '' else None

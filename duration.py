class Duration:
    def __init__(self, duration_time):
        raw_duration = duration_time.split(':')
        self.hour = int(raw_duration[0])
        self.minute = int(raw_duration[1])

if __name__ in '__main__':
    test1 = Duration("24:20")
    print(test1.hour, test1.minute)
class Start:
    def __init__(self, start_time, start_day=None):
        raw_list = start_time.split(' ')
        time = raw_list[0].split(':')
        self.hour = int(time[0])
        self.minute = int(time[1])
        self.meridiem = raw_list[1]
        self.day = start_day

if __name__ == '__main__':
    test1 = Start("11:43 PM", "tueSday")
    test2 = Start("11:43 PM")
    tests = [test1, test2]
    for test in tests:
        print(test.hour, test.minute, test.meridiem, test.day)

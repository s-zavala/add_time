from start import Start
from duration import Duration


def add_time(start, duration, start_day=None):
    """
    Adds a period of time to a starting time.

    Args:
    start -- Start time as a str, in format "hour:minute AM" or "hour:minute PM", eg. "12:00 AM"
    duration -- Period of time as a str, in format "hour:minute", eg. "24:10:
    start_day -- Start day as a str, eg. "Monday", "monday", "monDay". Optional. Case insensitive.
    Returns:
    The sum of the starting time plus the duration time. eg. "11:20 AM, Thursday (n days later)"
    """
    
        # List of days AM and PM to walk through to find final day.
    D = ["Monday AM", "Monday PM", "Tuesday AM", "Tuesday PM",
        "Wednesday AM", "Wednesday PM", "Thursday AM", "Thursday PM",
        "Friday AM", "Friday PM", "Saturday AM", "Saturday PM",
        "Sunday AM", "Sunday PM"]

    def make_instance(start, duration, start_day):
        """
        Return two class instances: start from Start and duration from Duration.
        """
        start = Start(start, start_day)
        duration = Duration(duration)
        return start, duration


    def sum_min(start_min, duration_min):
        """
        Add up start minutes with duration minutes.

        Returns:
        add_hour -- if the minute sum > 60 minutes, keep track of hours
        end_min -- the final minute for display
        """
        # Sum total minutes.
        sum_min = start_min + duration_min
        # Floor div catches if sum_min exceeds 60 min.
        add_hour = sum_min // 60
        # Remainder mod gets final min.
        end_min = sum_min % 60
        return add_hour, end_min


    def sum_hour(add_hour, start_hour, duration_hour):
        """
        Add up start hours, duration hours, and any hours accrued from the sum of minutes.

        Returns:
        add_meridiem -- if total hour exceed 12 hour periods, keep track of them
        add_day -- if total hour exceeds 24 hour period, record these
        end_hour -- the final hour to display
        """
        # Sum total hours, 12-hour periods (here called meridiem) elapsed and days elapsed.
        sum_hour = add_hour + start_hour + duration_hour
        # Floor div catches number of 12 hour cycles.
        add_meridiem = sum_hour // 12
        # Calc total days elapsed.
        add_day = add_meridiem//2
        # Mod gets 12-hour periods elapsed.
        add_meridiem %= 2
        # Calc end hour. Test for zero hour.
        end_hour = sum_hour % 12
        if end_hour == 0:
            end_hour = 12
        return add_meridiem, add_day, end_hour


    def find_start(D, start_day):
        """
        In dict D of days by AM and PM, find the offset of the start day.

        Return:
        start_offset -- an int of the start day offset, eg. 0, 1, 14
        """
        # Find start day offset searching dict of days by first two letters.
        d = [x[:2].lower() for x in D]
        day = start_day[:2].lower()
        start_offset = d.index(day)
        # Check if starting time is PM.
        if D[start_offset + 1][-2:] == start.meridiem:
            start_offset += 1
        return start_offset

    
    def find_end(start_offset, add_day, add_meridiem):
        """
        Add the start offset to any extra meridiem (12-hr periods).
        Return:
        end_offset -- the offset in D of the final day to display
        """
        # Add meridiem_count to start_offset to get end_offset.
        end_offset = start_offset + 2 * add_day + add_meridiem
        end_offset %= 14
        return end_offset

    
    def end_day(end_offset):
        """
        Returns the str of end day and end meridiem.
        """
        end_day = D[end_offset]
        end_day_list = end_day.split(' ')
        end_meridiem = end_day_list[1]
        end_day = end_day_list[0]
        return end_day, end_meridiem
    

    def form_end_time(end_hr, end_min, end_mer):
        """
        Returns a str for the end time. HR:MIN AM/PM.
        """
        end_str = ""
        hr = str(end_hr)
        min = str(end_min)
        if len(min) == 1:
            min = '0' + min
        end_str += hr + ':' + min + ' ' + end_mer
        return end_str
    

    def days_later(add_day, add_mer, end_mer):
        if end_mer == start.meridiem and add_day == 0:
            end = ''
        if start.meridiem == 'AM' and end_mer == 'PM' and add_day == 0:
            end = ''
        next = ((start.meridiem == 'PM' and end_mer == 'AM' and add_day == 0), 
            (add_day == 1 and add_mer == 0),
            (start.meridiem == 'AM' and end_mer == 'PM' and add_day == 1 and add_mer == 1))
        for test in next:
            if test:
                end = ' (next day)'
        if start.meridiem == 'PM' and end_mer == 'AM' and add_day == 1 and add_mer == 1:
            end = ' (' + str(add_day + 1) + ' days later)'
        if add_day > 1:
            if end_mer == start.meridiem or (start.meridiem == 'AM' and end_mer == 'PM'):
                end = ' (' + str(add_day) + ' days later)'
            if start.meridiem == 'PM' and end_mer == 'AM' and add_mer == 1:
                end = ' (' + str(add_day + 1) + ' days later)'
        return end

    instances = make_instance(start, duration, start_day)
    # print('Instances: ', instances)
    start, duration = instances
    minutes = sum_min(start.minute, duration.minute)
    add_hr = minutes[0]
    end_min = minutes[1]
    # print('Additional hours: ', add_hr)
    # print('Final minute: ', end_min)
    hours = sum_hour(add_hr, start.hour, duration.hour)
    add_mer = hours[0]
    add_day = hours[1]
    end_hr = hours[2]
    # print('Add meridiems: ', add_mer)
    # print('Add days: ', add_day)
    # print('Final hour: ', end_hr)
    if start.day:
        # print('Given start day: ', start.day)
        start_offset = find_start(D, start.day)
        # print('Found st offset: ', start_offset)
    elif start.meridiem == 'AM':
        start_offset = 0
        # print('Given st is AM.')
    elif start.meridiem == 'PM':
        start_offset = 1
        # print('Given st is PM.')
    end_offset = find_end(start_offset, add_day, add_mer)
    # print('Found end offset: ', end_offset)
    day = end_day(end_offset)
    end_day = day[0]
    end_mer = day[1]
    # print('Final day: ', end_day)
    # print('Final AM/PM: ', end_mer)
    if start.day:
        total = (form_end_time(end_hr, end_min, end_mer) + ', ' + end_day + days_later(add_day, add_mer, end_mer))
    else:
        total = form_end_time(end_hr, end_min, end_mer) + days_later(add_day, add_mer, end_mer)
    return total


if __name__ == '__main__':
    test = [["3:00 PM", "3:10"], ["11:43 AM", "00:20"], ["10:10 PM", "3:30"],
            ["11:43 PM", "24:20", "tueSday"], ["6:30 PM", "205:12"]]
    [print(add_time(*t)) for t in test]

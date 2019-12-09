import datetime

class Resident(object):
    def __init__(self, first_name, last_name, level, program, division, start_date, end_date):
        self.first_name          = first_name
        self.last_name           = last_name
        self.level               = level
        self.program             = program
        self.devision            = division
        self.start_date          = start_date
        self.end_date            = end_date
        self.time_off            = []
        self.remaining_num_calls = self.get_max_num_calls

    def add_time_off(self, year, month, days):
        for day in days:
            self.time_off.append(datetime.date(year, month, day))

    def get_full_name(self):
        return self.first_name + r' ' + self.last_name

    def get_max_num_calls(self):
        num_on_service_days = (self.end_date - self.start_date).days - len(self.time_off) + 1
        return num_on_service_days

    def log(self):
        print( r'first name : ' + self.first_name )
        print( r'last name  : ' + self.last_name  )
        print( r'level      : ' + self.level      )
        print( r'program    : ' + self.program    )
        print( r'division   : ' + self.devision   )
        print( r'start date : ' + self.start_date.strftime(r'%Y-%m-%d') )
        print( r'end date   : ' + self.end_date.strftime(  r'%Y-%m-%d') )


        label  = r'timeoff    :'
        indent = r' ' * len(label)
        tmp = r'['
        for index, i in enumerate(self.time_off):
            is_first = index == 0
            is_last  = index == len(self.time_off) - 1
            tmp += indent + r'  ' if not is_first else r' '
            tmp += i.strftime(r'%Y-%m-%d')
            tmp += '\n'   if not is_last else r' '
        tmp += r']'

        print( label + tmp)


class SeniorResident(Resident):
    def __init__(self, first_name, last_name, level, program, division, start_date, end_date):
        Resident.__init__(self, first_name, last_name, level, program, division, start_date, end_date)

        assert level in [r'PGY-4', r'PGY-5', r'PGY-6']


class JuniorResident(Resident):
    def __init__(self, first_name, last_name, level, program, division, start_date, end_date):
        Resident.__init__(self, first_name, last_name, level, program, division, start_date, end_date)

        assert level in [r'PGY-1', r'PGY-2', r'PGY-3']

if __name__ == r'__main__':
    main()

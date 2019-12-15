import datetime
import uuid

class Resident(object):
    def __init__(self, first_name, last_name, level, program, division, start_date, end_date):
        self.id                  = uuid.uuid1()
        self.first_name          = first_name
        self.last_name           = last_name
        self.level               = level
        self.program             = program
        self.devision            = division
        self.start_date          = start_date
        self.end_date            = end_date
        self.time_off            = []
        self.no_call             = []
        self.remaining_num_calls = self.get_max_num_calls

    def add_time_off(self, year, month, days):
        for day in days:
            self.time_off.append(datetime.date(year, month, day))

    def add_no_call(self, year, month, days):
        for day in days:
            self.no_call.append(datetime.date(year, month, day))

    def get_full_name(self):
        return self.first_name + r' ' + self.last_name

    def get_max_num_calls(self):
        # Call maximums are based on total days ON service (vacation and other time away are
        # deducted from total days on service before calculating maximum call)

        # If rotation is >1 month, in-house call maximum can be averaged over the
        # length of the rotation (maximum averaging length is 3 months) with a
        # maximum of 9 calls in any given month

        num_on_service_days = (self.end_date - self.start_date).days + 1 - len(self.time_off) - len(self.no_call)

        num_months_during_service = num_on_service_days / 30
        num_remaining_days        = num_on_service_days % 30

        if num_remaining_days < 19:
            return num_months_during_service * 9 + num_remaining_days / 4
        if num_remaining_days < 23:
            return num_months_during_service * 9 + 5
        if num_remaining_days < 27:
            return num_months_during_service * 9 + 6
        if num_remaining_days < 30:
            return num_months_during_service * 9 + 7

    def get_no_post_calls(self):
        return self.time_off

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

        print(label + tmp)

        label  = r'no call    :'
        indent = r' ' * len(label)
        tmp = r'['
        for index, i in enumerate(self.no_call):
            is_first = index == 0
            is_last  = index == len(self.time_off) - 1
            tmp += indent + r'  ' if not is_first else r' '
            tmp += i.strftime(r'%Y-%m-%d')
            tmp += '\n'   if not is_last else r' '
        tmp += r']'

        print(label + tmp)


class SeniorResident(Resident):
    def __init__(self, first_name, last_name, level, program, division, start_date, end_date):
        Resident.__init__(self, first_name, last_name, level, program, division, start_date, end_date)

        assert level in [r'PGY-3', r'PGY-4', r'PGY-5']


class JuniorResident(Resident):
    def __init__(self, first_name, last_name, level, program, division, start_date, end_date):
        Resident.__init__(self, first_name, last_name, level, program, division, start_date, end_date)

        assert level in [r'PGY-1', r'PGY-2']

if __name__ == r'__main__':
    main()

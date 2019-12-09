import datetime

from tree import *
from resident import *

from anytree import RenderTree
from anytree.exporter import DotExporter

class ScheduleBlock:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date   = end_date
        self.residents  = []

    def set_residents(self, residents):
        self.residents = residents

    def get_senior_residents(self):
        return list(filter(lambda resident : isinstance(resident, SeniorResident), self.residents))

    def get_junior_residents(self):
        return list(filter(lambda resident : isinstance(resident, JuniorResident), self.residents))

    # TODO(FG): define
    #def get_solo_capable_residents(self):

    def create(self):
        ret = {}
        for date in set([self.start_date + datetime.timedelta(days = x) for x in range(0, (self.end_date - self.start_date).days)]):
            ret[date] = []
            for senior_resident in self.get_senior_residents():
                if date not in senior_resident.time_off:
                    for junior_resident in self.get_junior_residents():
                        if date not in junior_resident.time_off:
                            ret[date].append(NodeSub(date, senior_resident, junior_resident))

        keys = list(sorted(ret.keys()))
        for index in range(0, len(keys)):
            if index > 0:
                for parent in ret[keys[index - 1]]:
                    #for node in ret[keys[index]]:
                    parent.add_children(ret[keys[index]])

        root = NodeRoot(children = ret[keys[0]])
        print(RenderTree(root))

        #udo = Node("Udo")
        #marc = Node("Marc")
        #lian = Node("Lian", parent=marc)

        #print(RenderTree(udo))
        #print(RenderTree(marc))

        #for key in sorted(ret.keys()):
        #    print(key)
        #    print(r'********')
        #    for node in ret[key]:
        #        node.log()
        #return ret


    def log(self):
        for resident in self.residents:
            resident.log()


def schedule():
    paranthaman_pranavan = JuniorResident(r'Parantheman', r'Pranavan',      r'PGY-1', r'Fam Med',   r'Gen Surg' , datetime.date(2019, 7, 1), datetime.date(2019,  7, 28))
    preet_brar           = JuniorResident(r'Preet',       r'Brar',          r'PGY-2', r'Gen Surg',  r'Gen Surg' , datetime.date(2019, 7, 1), datetime.date(2019,  9, 22))
    marcus_oosenburgh    = JuniorResident(r'Marcus',      r'Oosenburgh',    r'PGY-2', r'Gen Surg',  r'Endoscopy', datetime.date(2019, 7, 1), datetime.date(2019,  8, 25))
    megan_melland_smith  = JuniorResident(r'Megan',       r'Melland-Smith', r'PGY-3', r'Gen Surg',  r'Gen Surg' , datetime.date(2019, 7, 1), datetime.date(2019,  8, 31))
    lior_flor            = SeniorResident(r'Lior',        r'Flor',          r'PGY-4', r'Gen Surg',  r'Gen Surg' , datetime.date(2019, 7, 1), datetime.date(2019, 10, 31))
    aleem_visram         = SeniorResident(r'Aleem',       r'Visram',        r'PGY-4', r'Gen Surg',  r'Gen Surg' , datetime.date(2019, 7, 1), datetime.date(2019, 10, 31))
    david_parente        = SeniorResident(r'Devid',       r'Parente',       r'PGY-6', r'Thor Surg', r'Thoracic' , datetime.date(2019, 7, 1), datetime.date(2019, 10, 31))


    megan_melland_smith.add_time_off( 2019, 7, range(1, 2))
    paranthaman_pranavan.add_time_off(2019, 7, range(1, 6))

    print(paranthaman_pranavan.get_max_num_calls())

    schedule_block = ScheduleBlock( datetime.date(2019, 7, 1), datetime.date(2019, 7, 31))
    residents = [
        preet_brar,
        lior_flor,
        megan_melland_smith,
        marcus_oosenburgh,
        david_parente,
        aleem_visram,
        paranthaman_pranavan
    ]
    schedule_block.set_residents(residents)

    schedule_block.create()


    # - Each resident is entitled to 2 complete weekends off (which includes Friday night)
    #   for each 28 day time period. In addition, for home call services, residents cannot
    #   be scheduled for two weekends in a row

    # - Unless otherwise agreed to by the affected resident, PARO and the Program Director,
    #   residents should not be scheduled for consecutive periods of call. This provision
    #   applies to both in-house and home call.

    # - Call maximums are based on total days ON service (vacation and other time away are
    #   deducted from total days on service before calculating maximum call)

    # - Juniors are PGY1-2 and seniors are PGY3-5

    # - Exclude PGY6-7 or thoracic fellow 

    # - Consider personal no call request

    # - resident cannot be on call the first day after vacation

    # - Friday and sundays are handled by the same pair

    # - Family medicine resodents regardless of level never do solo calls

    # - Non family medicine PGY-2 resident do solo call

if __name__ == "__main__":
    schedule()

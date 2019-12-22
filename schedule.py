import datetime

from tree import *
from resident import *

from anytree import RenderTree
from anytree.exporter import DotExporter

import copy

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
        block = sorted(set([self.start_date + datetime.timedelta(days = x) for x in range(0, (self.end_date - self.start_date).days + 1)]))
        for date in block:
            ret[date] = []
            for junior_resident in self.get_junior_residents():
                if date >= junior_resident.start_date and date <= junior_resident.end_date:
                    # - resident cannot be post call the first day of vacation
                    post_call_date = date + datetime.timedelta(days = 1)
                    if date not in junior_resident.time_off and post_call_date not in junior_resident.get_no_post_calls():
                        if junior_resident.allowed_solo_call:
                            ret[date].append(NodeSub(date, None, junior_resident))

                        for senior_resident in self.get_senior_residents():
                            if date >= senior_resident.start_date and date <= senior_resident.end_date:
                                if date not in senior_resident.time_off and post_call_date not in senior_resident.get_no_post_calls():
                                    ret[date].append(NodeSub(date, senior_resident, junior_resident))

        keys = list(sorted(ret.keys()))
        root = NodeRoot()
        root.add_children(ret[keys[0]])

        for key in keys:
            print(r'key: {} - num_values:{}'.format(key, len(ret[key])))

        for index in range(0, len(keys) - 1):
            print(keys[index])
            print(r'  num parent nodes: {}'.format(len(ret[keys[index]])))
            print(r'  num child candidates: {}'.format(len(ret[keys[index+1]])))
            tmp = []
            child_key = keys[index + 1]
            children  = ret[child_key]
            for parent in ret[keys[index]]:
                children_copy = []

                # - Friday and sundays are handled by the same pair
                if child_key.weekday() == 6:
                    gp_senior_id = parent.parent.get_senior_resident_id()
                    gp_junior_id = parent.parent.get_junior_resident_id()

                    f = filter(
                        lambda node: node.get_senior_resident_id() == gp_senior_id and node.get_junior_resident_id() == gp_junior_id,
                        children
                    )
                    found_child = next(f)
                    if found_child:
                        children_copy.append(copy.deepcopy(found_child))
                else:
                    children_copy = copy.deepcopy(children)

                added_children = parent.add_children(children_copy)
                if len(added_children) > 0:
                    tmp.extend(added_children)

            ret[keys[index + 1]] = tmp
            print(r'  num leaf nodes: {}'.format(len(ret[keys[index+1]])))

        print(RenderTree(root))

    def log(self):
        for resident in self.redents:
            resident.log()


def schedule():
    katie_hicks       = JuniorResident(r'Katie',     r'Hicks',      r'PGY-1', r'Plas Surg', r'Gen Surg', datetime.date(2020, 1,  1), datetime.date(2020, 1, 12))
    teagan_telesnicki = JuniorResident(r'Teagan',    r'Telesnicki', r'PGY-1', r'Gen Surg',  r'Thoracic', datetime.date(2020, 1,  1), datetime.date(2020, 1, 12))
    paul_savage       = JuniorResident(r'Paul',      r'Savage',     r'PGY-1', r'Gen Surg',  r'Thoracic', datetime.date(2020, 1, 13), datetime.date(2020, 1, 31))
    katherine_yang    = JuniorResident(r'Katherine', r'Yang',       r'PGY-1', r'Gen Surg',  r'Gen Surg', datetime.date(2020, 1,  6), datetime.date(2020, 1, 31))
    shaerine_ensan    = JuniorResident(r'Shaerine',  r'Ensan',      r'PGY-1', r'Fam Med',   r'Gen Surg', datetime.date(2020, 1,  2), datetime.date(2020, 1,  3))
    sarah_cho         = JuniorResident(r'Sarah',     r'Cho',        r'PGY-1', r'Fam Med',   r'Gen Surg', datetime.date(2020, 1,  4), datetime.date(2020, 1,  5))
    mohammed_firdouse = JuniorResident(r'Mohammed',  r'Firdouse',   r'PGY-2', r'Vas Surg',  r'Gen Surg', datetime.date(2020, 1, 13), datetime.date(2020, 1, 31))
    rashed_alaamer    = JuniorResident(r'Rashed',    r'Alaamer',    r'PGY-2', r'Gen Surg',  r'Gen Surg', datetime.date(2020, 1,  1), datetime.date(2020, 1, 12))
    bethany_so        = JuniorResident(r'Bethany',   r'So',         r'PGY-2', r'Fam Med',   r'Gen Surg', datetime.date(2020, 1,  6), datetime.date(2020, 1, 12))

    dhruvin_hirpara   = SeniorResident(r'Dhruvin',   r'Hirpara',    r'PGY-3', r'Gen Surg',  r'Thoracic', datetime.date(2020, 1,  2), datetime.date(2020, 1, 31))
    sergio_acuna      = SeniorResident(r'Sergio',    r'Acuna',      r'PGY-3', r'Gen Surg',  r'Gen Surg', datetime.date(2020, 1,  2), datetime.date(2020, 1, 31))
    carolina_jimenez  = SeniorResident(r'Carolina',  r'Jimenez',    r'PGY-4', r'Gen Surg',  r'Gen Surg', datetime.date(2020, 1,  1), datetime.date(2020, 1, 31))


    rashed_alaamer.add_time_off(   2020, 1, range( 1,  6))
    teagan_telesnicki.add_time_off(2020, 1, range( 1,  5))
    katherine_yang.add_time_off(   2020, 1, range(11, 20))

    dhruvin_hirpara.add_no_call(   2020, 1, range(17, 21))
    dhruvin_hirpara.add_no_call(   2020, 1, range(28, 29))

    katie_hicks.allow_solo_call()

    schedule_block = ScheduleBlock(
        datetime.date(2020, 1,  1),
        datetime.date(2020, 1,  31)
    )
    residents = [
        katie_hicks,
        teagan_telesnicki,
        paul_savage,
        katherine_yang,
        shaerine_ensan,
        sarah_cho,
        mohammed_firdouse,
        rashed_alaamer,
        bethany_so,
        dhruvin_hirpara,
        sergio_acuna,
        carolina_jimenez
    ]
    schedule_block.set_residents(residents)

    schedule_block.create()

    # - Family medicine residents regardless of level never do solo calls

    # - Non family medicine PGY-2 resident do solo call


if __name__ == "__main__":
    schedule()

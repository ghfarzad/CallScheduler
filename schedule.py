import datetime

from tree import *
from resident import *

from anytree import RenderTree
from anytree.exporter import DotExporter

import concurrent.futures
import copy
import math
import threading

class ScheduleBlock:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date   = end_date
        self.residents  = []
        self.root       = NodeRoot()
        self.lock       = threading.Lock()
        self.ret        = {}
        self.ret_copy   = {}

    def set_residents(self, residents):
        self.residents = residents

    def get_senior_residents(self):
        return list(filter(lambda resident : isinstance(resident, SeniorResident), self.residents))

    def get_junior_residents(self):
        return list(filter(lambda resident : isinstance(resident, JuniorResident), self.residents))

    def append(self, thread_number, parents_chunk, children, date):
        for parent in parents_chunk:
            children_copy = copy.deepcopy(children)
            # - Friday and sundays are handled by the same pair
            if date.weekday() == 6:
                gp_senior_id = parent.parent.get_senior_resident_id()
                gp_junior_id = parent.parent.get_junior_resident_id()

                f = filter(
                    lambda node: node.get_senior_resident_id() == gp_senior_id and node.get_junior_resident_id() == gp_junior_id,
                    children_copy
                )
                found_child = next(f)
                if found_child:
                    parent.add_children([found_child])
            else:
                parent.add_children(children_copy)

            if len(parent.children) > 0:
                self.ret_copy[date].extend(parent.children)


    def create(self):
        block = sorted(set([self.start_date + datetime.timedelta(days = x) for x in range(0, (self.end_date - self.start_date).days + 1)]))
        for date in block:
            self.ret_copy[date] = []
            self.ret[date] = []
            for junior_resident in self.get_junior_residents():
                if date >= junior_resident.start_date and date <= junior_resident.end_date:
                    # - resident cannot be post call the first day of vacation
                    post_call_date = date + datetime.timedelta(days = 1)
                    if date not in junior_resident.time_off and post_call_date not in junior_resident.get_no_post_calls():
                        if junior_resident.allowed_solo_call:
                            self.ret[date].append(NodeSub(date, None, junior_resident))

                        for senior_resident in self.get_senior_residents():
                            if date >= senior_resident.start_date and date <= senior_resident.end_date:
                                if date not in senior_resident.time_off and post_call_date not in senior_resident.get_no_post_calls():
                                    self.ret[date].append(NodeSub(date, senior_resident, junior_resident))

        keys = list(sorted(self.ret.keys()))
        self.root.add_children(self.ret[keys[0]])

        self.ret_copy[keys[0]].extend(self.ret[keys[0]])

        max_num_workers = 500
        for index in range(0, len(keys) - 1):
            tmp = []
            parent_key   = keys[index]
            child_key    = keys[index + 1]
            parents      = self.ret_copy[parent_key]
            num_parents  = len(parents)

            print(child_key)

            worker_count = num_parents if num_parents <= max_num_workers else max_num_workers
            chunk_length = math.ceil(num_parents / worker_count)
            chunks = [parents[i:i+chunk_length] for i in range(0, len(parents), chunk_length)]
            with concurrent.futures.ThreadPoolExecutor(max_workers = len(chunks)) as executor:
                for thread_number in range(len(chunks)):
                    executor.submit(
                        self.append,
                        thread_number,
                        chunks[thread_number],
                        copy.deepcopy(self.ret[child_key]),
                        child_key
                    )

        print(RenderTree(self.root))

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
        datetime.date(2020, 1, 5)
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

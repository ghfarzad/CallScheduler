from anytree import NodeMixin

import copy
import sys

class NodeBase(object):
    def __init__(self, date, senior_resident, junior_resident = None):
        self.date            = date
        self.senior_resident = senior_resident
        self.junior_resident = junior_resident
        self.meta            = {}

    def get_senior_resident_id(self):
        return self.senior_resident.id if self.senior_resident else None

    def get_junior_resident_id(self):
        return self.junior_resident.id if self.junior_resident else None

    def get_num_calls(self, senior_id, junior_id):
        meta_has_senior = senior_id in self.meta.keys()
        meta_has_junior = junior_id in self.meta.keys()
        return {
            r'senior':         self.meta[senior_id][r'num_calls']         if meta_has_senior else 0,
            r'junior':         self.meta[junior_id][r'num_calls']         if meta_has_junior else 0,
            r'senior_weekend': self.meta[senior_id][r'num_weekend_calls'] if meta_has_senior else 0,
            r'junior_weekend': self.meta[junior_id][r'num_weekend_calls'] if meta_has_junior else 0
        }

    def add_meta(self, meta):
        self.meta  = meta if meta else {}
        senior_id  = self.get_senior_resident_id()
        junior_id  = self.get_junior_resident_id()
        is_weekend = self.date.weekday() > 3
        if not senior_id in self.meta.keys():
            self.meta[senior_id] = {
                r'num_calls': 0,
                r'num_weekend_calls': 0
            }

        self.meta[senior_id][r'num_calls'] += 1
        if is_weekend:
            self.meta[senior_id][r'num_weekend_calls'] += 1

        if not junior_id in self.meta.keys():
            self.meta[junior_id] = {
                r'num_calls': 0,
                r'num_weekend_calls': 0
            }

        self.meta[junior_id][r'num_calls'] += 1
        if is_weekend:
            self.meta[junior_id][r'num_weekend_calls'] += 1


    def log(self):
        self.senior_resident.log()

        if self.junior_resident:
            self.junior_resident.log()


class NodeSub(NodeBase, NodeMixin):
    def __init__(self, date, senior_resident, junior_resident = None, parent = None, children = None):
        super(NodeSub, self).__init__(date, senior_resident, junior_resident)
        self.name   = self.to_string()
        self.parent = parent
        if children:
            self.children = children

    def add_child(self, child):
        # - Unless otherwise agreed to by the affected resident, PARO and the Program Director,
        #   residents should not be scheduled for consecutive periods of call. This provision
        #   applies to both in-house and home call.
        parent_senior_id = self.get_senior_resident_id()
        parent_junior_id = self.get_junior_resident_id()
        child_senior_id  = child.get_senior_resident_id()
        child_junior_id  = child.get_junior_resident_id()
        if (parent_senior_id and parent_senior_id == child_senior_id) or parent_junior_id == child_junior_id:
            return False

        # - Each resident is entitled to 2 complete weekends off (which includes Friday night)
        #   for each 28 day time period.

        # TODO(FG)
        # - For home call services, residents cannot be scheduled for 2 weekends in a row.

        senior_max_num_calls = child.senior_resident.get_max_num_calls() if child.senior_resident else sys.maxsize
        junior_max_num_calls = child.junior_resident.get_max_num_calls()

        num_calls = self.get_num_calls(child_senior_id, child_junior_id)
        if num_calls[r'senior'] < senior_max_num_calls and num_calls[r'junior'] < junior_max_num_calls:
            if child.date.weekday() > 3:
                if num_calls[r'senior_weekend'] >= 2 or num_calls[r'junior_weekend'] >= 2:
                    return False

            child.add_meta(copy.deepcopy(self.meta))

            children = list(self.children)
            children.append(child)
            self.children = children
            return True
        else:
            return False


    def add_children(self, children):
        ret = []
        for child in children:
            if self.add_child(child):
                ret.append(child)
        return ret

    def to_string(self):
        num_calls = self.get_num_calls(self.get_senior_resident_id(), self.get_junior_resident_id())
        ret = r'{} {} - sen: {} #calls:{} #wd calls:{} - jun: {} #calls:{} #wd calls:{}'
        weekdays = [r'Monday', r'Tuesday', r'Wednesday', r'Thursday', r'Friday', r'Saturday', r'Sunday']
        return ret.format(
            weekdays[self.date.weekday()],
            self.date.strftime(r'%Y-%m-%d'),
            self.senior_resident.get_full_name() if self.senior_resident else r'None',
            num_calls[r'senior'],
            num_calls[r'senior_weekend'],
            self.junior_resident.get_full_name(),
            num_calls[r'junior'],
            num_calls[r'junior_weekend']
        )

    def __repr__(self):
        return self.to_string()

class NodeRoot(NodeSub):
    def __init__(self, date = None, senior_resident = None, junior_resident = None, parent = None, children = None):
        super(NodeSub, self).__init__(date, senior_resident, junior_resident)
        self.name     = r'root'
        self.parent = parent
        if children:
            self.children = children

    def to_string(self):
        return self.name


if __name__ == r'__main__':
    main()

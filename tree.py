from anytree import NodeMixin

class NodeBase(object):
    def __init__(self, date, senior_resident, junior_resident = None):
        self.date            = date
        self.senior_resident = senior_resident
        self.junior_resident = junior_resident

    def get_senior_resident_id(self):
        return self.senior_resident.id

    def get_junior_resident_id(self):
        return self.junior_resident.id

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
        print(r'add_child({}, {})'.format(self.to_string(), child.to_string()))

        # - Unless otherwise agreed to by the affected resident, PARO and the Program Director,
        #   residents should not be scheduled for consecutive periods of call. This provision
        #   applies to both in-house and home call.
        parent_senior_id = self.get_senior_resident_id()
        parent_junior_id = self.get_junior_resident_id()
        child_senior_id  = child.get_senior_resident_id()
        child_junior_id  = child.get_junior_resident_id()
        if parent_senior_id == child_senior_id or parent_junior_id == child_junior_id:
            return

        senior_num_calls = 0
        junior_num_calls = 0

        parent = self
        while parent:
            senior_num_calls += 1 if parent_senior_id == child_senior_id else 0
            junior_num_calls += 1 if parent_junior_id == child_junior_id else 0
            parent = parent.parent

        print(r'    senior_num_calls: {}'.format(senior_num_calls))
        print(r'    junior_num_calls: {}'.format(junior_num_calls))

        senior_max_num_calls = child.senior_resident.get_max_num_calls()
        junior_max_num_calls = child.junior_resident.get_max_num_calls()
        if senior_num_calls <= senior_max_num_calls and junior_num_calls <= junior_max_num_calls:
            children = list(self.children)
            children.append(child)
            self.children = children

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def to_string(self):
        ret = r'date: {} - senior: {} - junior: {}'
        return ret.format(
            self.date.strftime(r'%Y-%m-%d'),
            self.senior_resident.get_full_name(),
            self.junior_resident.get_full_name()
        )

    def __repr__(self):
        return self.to_string()

class NodeRoot(NodeSub):
    def __init__(self, children = None):
        self.name     = r'root'
        self.parent   = None
        if children:
            self.children = children

    def to_string(self):
        return self.name


if __name__ == r'__main__':
    main()

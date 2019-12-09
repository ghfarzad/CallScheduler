from anytree import NodeMixin

class NodeBase(object):
    def __init__(self, date, senior_resident, junior_resident = None):
        self.date            = date
        self.senior_resident = senior_resident
        self.junior_resident = junior_resident

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
        children = list(self.children)
        children.append(child)
        self.children = children

    def add_children(self, childs):
        children = list(self.children)
        children.extend(childs)
        self.children = children

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

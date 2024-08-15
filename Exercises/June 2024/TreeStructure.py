class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def name_split(self):
        self.data = self.data.split()[0]
        if self.children:
            for child in self.children:
                child.name_split()

    def designation_split(self):
        self.data = self.data.split('(')[1].split(')')[0]
        if self.children:
            for child in self.children:
                child.designation_split()

    def print_tree(self, level):
        if self.get_level() > level:
            return
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + self.data)
        if self.children:
            for child in self.children:
                child.print_tree(level)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

def build_product_tree(format = 'both'):
    if format.lower() not in ['name', 'designation', 'both']:
        raise ValueError('Invalid Parameter')

    ceo = TreeNode('Nilpul (CEO)')

    cto = TreeNode('Chinmay (CTO)')
    hr_head = TreeNode('Gels (HR Head)')

    ceo.add_child(cto)
    ceo.add_child(hr_head)

    infra_head = TreeNode('Vishwa (Infrastructure Head)')

    cto.add_child(infra_head)
    infra_head.add_child(TreeNode('Dhaval (Cloud Manager)'))
    infra_head.add_child(TreeNode('Abhijit (App Manager)'))
    hr_head.add_child(TreeNode('Peter (Recruitment Manager)'))
    hr_head.add_child(TreeNode('Waqas (Policy Manager)'))

    if format.lower() == 'name':
        ceo.name_split()
    elif format.lower() == 'designation': 
        ceo.designation_split()
    
    return ceo

root = build_product_tree()

root.print_tree(2)
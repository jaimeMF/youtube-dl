import ast

with open('__init__.py.bak') as f:
    code = f.read()
tree = ast.parse(code)

class Extractor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.res = []
    def ex(self, node):
        self.visit(node)
        return self.res
    #def generic_visit(self, node):
    #    print(node)
    def visit_Module(self, node):
        for s in node.body:
            self.visit(s)
    def visit_ImportFrom(self, node):
        if node.level < 1:
            return
        ies = []
        for alias in node.names:
            ies.append(alias.name)
        self.res.append((node.module, ies))

e = Extractor()
res = e.ex(tree)

indent = '    '

print('_ie_list = [')
for it in res:
    msg = indent  + '(' + repr(it[0]) + ', ['
    if len(it[1]) > 1:
        msg += '\n' + ',\n'.join(2*indent + repr(ie) for ie in it[1]) + ',\n' + indent
    else:
        msg += repr(it[1][0])
    msg += ']),'
    print(msg)
print(']')

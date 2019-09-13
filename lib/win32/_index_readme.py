import ast
import os


def _is_dunder(name):
    """Returns True if a __dunder__ name, False otherwise."""
    return (len(name) > 4 and
            name[:2] == name[-2:] == '__' and
            name[2] != '_' and
            name[-3] != '_')


def _is_sunder(name):
    """Returns True if a _sunder_ name, False otherwise."""
    return (len(name) > 2 and
            name[0] == name[-1] == '_' and
            name[1:2] != '_' and
            name[-2:-1] != '_')


flags = []
for flag_file in os.listdir('flags'):
    pass

funcs = []
for func_file in os.listdir('func'):
    if _is_dunder(func_file):
        continue
    func_file = open(os.path.join('func', func_file))
    node = ast.parse(func_file.read())
    for child_node in ast.iter_child_nodes(node):
        if isinstance(child_node, ast.FunctionDef):
            doc_string: str = ast.get_docstring(child_node)

            for i in range(10):
                try:
                    # get first sentance
                    end = doc_string.index(".")
                    description = doc_string[:end + 1]

                    end = description.index('_')
                    func_name = ''
                    for letter in reversed(description[:end]):
                        if letter == ' ':
                            break
                        func_name = letter + func_name

                    print(doc_string, func_name)
                except ValueError:
                    break

structs = []
for struct_file in os.listdir('structs'):
    pass


class node:
    def __init__(self, val) -> None:
        self.left = self.right = None
        self.val = val


def get_smallest(dict: dict):
    smallest = min(dict.items(), key=lambda data: data[1])
    dict.pop(smallest[0])
    return smallest


def create_tree(values: dict):
    stored = []

    x = get_smallest(values)

    if (values):
        y = get_smallest(values)
        new_node = node(x[1] + y[1])
        new_node.left = node(x[0])
        new_node.right = node(y[0])
        stored.append([new_node, new_node.val])
        result = create_tree_util(values, stored)
        root = result[0][0]
        result = dfs(root)
        return result
    else:
        return 0


def create_tree_util(values, stored: list):
    stored.sort(key=lambda data: data[1])
    candidate1 = stored[0]
    stored.pop(0)

    if (stored):

        candidate_sp = stored.pop(0)

        if (values):
            candidate2 = get_smallest(values)

            if (candidate_sp[1] <= candidate2[1]):
                new_node = node(candidate1[1] + candidate_sp[1])
                new_node.left = candidate1[0]
                new_node.right = candidate_sp[0]
                values[candidate2[0]] = candidate2[1]  #
                stored.append([new_node, new_node.val])
                create_tree_util(values, stored)

            elif (values):
                stored.append(candidate_sp)
                candidate3 = get_smallest(values)
                if (candidate1[1] <= candidate3[1]):
                    new_node = node(candidate1[1] + candidate2[1])
                    new_node.left = candidate1[0]
                    new_node.right = node(candidate2[0])
                    stored.append([new_node, new_node.val])
                    values[candidate3[0]] = candidate3[1]
                    create_tree_util(values, stored)
                else:
                    new_node = node(candidate2[1] + candidate3[1])
                    new_node.left = node(candidate2[0])
                    new_node.right = node(candidate3[0])
                    stored.append(candidate1)
                    stored.append([new_node, new_node.val])
                    create_tree_util(values, stored)
            else:
                new_node = node(candidate1[1] + candidate2[1])
                new_node.left = candidate1[0]
                new_node.right = node(candidate2[0])
                stored.append(candidate_sp)
                stored.append([new_node, new_node.val])
                create_tree_util(values, stored)
        else:
            new_node = node(candidate1[1] + candidate_sp[1])
            new_node.left = candidate1[0]
            new_node.right = candidate_sp[0]
            stored.append([new_node, new_node.val])
            create_tree_util(values, stored)
    else:
        if (values):
            candidate2 = get_smallest(values)

            if (candidate1[1] <= candidate2[1]):
                new_node = node(candidate1[1] + candidate2[1])
                new_node.left = candidate1[0]
                new_node.right = node(candidate2[0])
                stored.append([new_node, new_node.val])
                create_tree_util(values, stored)
            else:
                if (values):
                    candidate3 = get_smallest(values)
                    if (candidate1[1] <= candidate3[1]):
                        new_node = node(candidate1[1] + candidate2[1])
                        new_node.left = candidate1[0]
                        new_node.right = node(candidate2[0])
                        stored.append([new_node, new_node.val])
                        values[candidate3[0]] = candidate3[1]
                        create_tree_util(values, stored)
                    else:
                        new_node = node(candidate2[1] + candidate3[1])
                        new_node.left = node(candidate2[0])
                        new_node.right = node(candidate3[0])
                        stored.append(candidate1)
                        stored.append([new_node, new_node.val])
                        create_tree_util(values, stored)
        else:
            stored.append(candidate1)

    return stored


def dfs(root: node):
    code_dict = {}
    reverse_code_dict = {}
    code = ''
    dfs_util(root, code_dict, reverse_code_dict, code)
    # print(code_dict)
    return code_dict, reverse_code_dict


def dfs_util(root: node, code_dict, reverse_code_dict, code):
    if root is None:
        return
    if (root.left == None) and (root.right == None):
        reverse_code_dict[code] = root.val
        code_dict[root.val] = code

    dfs_util(root.left, code_dict, reverse_code_dict, (code + '0'))
    dfs_util(root.right, code_dict, reverse_code_dict, (code + '1'))

# values = {"A":1,"B":2,"C":3,"D":0}
# {'e': '00', 'f': '01', 'a': '100', 'b': '101', 'c': '110', 'd': '111'}
# values = {"a":1,"b":1,"c":1,"d":1,"e":1,"f":1}
# x = create_tree(values)
# print(x)



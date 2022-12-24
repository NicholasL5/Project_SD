class Node:
    def __init__(self, freq, char=None):
        self.freq = freq
        self.left = None
        self.right = None
        self.char = char
        self.next = None


class Tree:
    def __init__(self):
        self.code_dict = {}
        self.reverse_code = {}

    def buat_code(self, queue):
        code = ""
        node = queue.dequeue()
        self.buat_code_util(node, code)
        print(self.code_dict)

    def buat_code_util(self, node, code):
        if node is None:
            return
        if node.char is not None:
            self.code_dict[node.char] = code
            self.reverse_code[code] = node.char

        self.buat_code_util(node.left, (code + "0"))
        self.buat_code_util(node.right, (code + "1"))


class Queue:
    def __init__(self):
        self.front = self.rear = None
        self.size = 0

    def isEmpty(self):
        return self.front is None

    def enqueue(self, other, char=None):
        self.size += 1
        if not isinstance(other, Node):
            new_node = Node(other, char)
        else:
            new_node = other
        if self.isEmpty():
            self.front = self.rear = new_node
            return
        itr = self.front
        prev = itr
        while itr is not None:
            if itr.freq > new_node.freq:
                if itr == self.front:
                    new_node.next = itr
                    self.front = new_node
                    return
                new_node.next = itr
                prev.next = new_node
                return
            prev = itr
            itr = itr.next

        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        self.size -= 1
        if self.isEmpty():
            print("kosong")
            return
        temp = self.front
        self.front = temp.next
        return temp

    def peek(self):
        return self.front.data

    def printQ(self):
        itr = self.front
        while itr:
            if itr is self.rear:
                break
            print(itr.freq, end=" -> ")
            itr = itr.next
        print(itr.freq)


def priority(queue: Queue):
    node1 = queue.dequeue()
    node2 = queue.dequeue()
    new_node = Node(node1.freq + node2.freq)
    new_node.left = node1
    new_node.right = node2
    queue.enqueue(new_node)


values = {"a":1,"b":1,"c":1,"d":1,"e":1,"f":1}
queue = Queue()
for i in values:
    queue.enqueue(values[i], i)
queue.printQ()
while queue.size != 1:
    priority(queue)

tree = Tree()
tree.buat_code(queue)

class Node:
    def __init__(self, data, index):
        self.data = data
        self.next = None
        self.index = index
        self.prev = None
        self.original_path = data
        self.decompressed = None
        self.compressed = None


class Queue:
    def __init__(self):
        self.counter = 0
        self.front = self.rear = None
        self.pointer = self.front

    def isEmpty(self):
        return self.front is None

    def enqueue(self, new_data):
        if not self.check_que(new_data):
            self.counter += 1
            new_node = Node(new_data, self.counter)
            if self.isEmpty():
                self.front = new_node
                self.front.next = self.front
                self.front.prev = self.front
                self.rear = self.front.prev

                return True

            new_node.next = self.front
            new_node.prev = self.rear
            self.front.prev = new_node
            self.rear.next = new_node
            self.rear = new_node
            return True

    def get_all_index(self):
        all = []
        itr = self.front
        while itr:

            all.append(int(itr.index)-1)
            if itr == self.rear:
                break
            itr = itr.next
        return all

    def get_all_data(self):
        all = []
        itr = self.front
        while itr:
            all.append(int(itr.data) - 1)
            if itr == self.rear:
                break
            itr = itr.next
        return all

    def delete_compress(self, tup):
        for i in tup:
            itr = self.front
            while itr is not None:
                if itr.index == int(i)+1:
                    itr.compressed = None
                    itr.data = itr.original_path
                    break
                itr = itr.next

    def delete_decompress(self, tup):
        for i in tup:
            itr = self.front
            while itr is not None:
                if itr.index == int(i)+1:
                    itr.decompressed = None
                    if itr.compressed:
                        itr.data = itr.compressed
                    else:
                        itr.data = itr.original_path
                    break
                itr = itr.next

    def check_que(self, data):
        """return true kalau ada duplikat"""
        if not self.isEmpty():
            itr = self.front
            while itr:
                if itr.original_path == data:
                    return True
                if itr == self.rear:
                    if itr.original_path == data:
                        return True
                    else:
                        break
                itr = itr.next

    def insert_compressed(self, index, path):
        itr = self.front
        while itr:
            if itr.index == int(index):
                itr.compressed = path
                itr.data = path
                return
            itr = itr.next

    def insert_decompressed(self, index, path):
        itr = self.front
        while itr:
            if itr.index == int(index):
                itr.decompressed = path
                itr.data = path
                return
            itr = itr.next

    def dequeue_index(self, index):
        if self.isEmpty():
            return
        itr = self.front
        if itr.index == index:
            if self.front.next == self.front:
                self.front = None
                self.rear = None

                return
            self.front = itr.next
            self.front.prev = self.rear
            self.rear.next = self.front
            return
        while itr.next is not None:
            if itr.next.index == index:
                if itr.next == self.rear:
                    self.rear = itr
                    self.rear.next = self.front
                    self.front.prev = self.rear
                    return
                itr.next = itr.next.next
                itr.next.next.prev = itr
                return
            itr = itr.next


    def peek_index(self, index):
        if self.isEmpty():
            return None
        itr = self.front
        while itr is not None:
            if itr.index == int(index):
                return itr
            itr = itr.next

    def subque(self, tup):
        subque = Queue()
        for i in tup:
            itr = self.front
            while itr is not None:
                if itr.index == int(i)+1:
                    temp = self.peek_index(itr.index)
                    subque.enqueue(temp.data)
                    break
                itr = itr.next
        return subque

    def dequeue(self):
        if self.isEmpty():
            print("dequeue kosong")
            return
        if self.front.next == self.front:
            temp = self.front
            self.front = None
            self.rear = None
            return temp
        temp = self.front
        self.front = temp.next
        self.front.prev = self.rear
        self.rear.next = self.front
        return temp

    def get_ori(self, ind):
        itr = self.front
        while itr is not self.rear:
            if itr.index == int(ind):
                return itr.original_path
            itr = itr.next
        if itr.index == int(ind):
            return itr.original_path

    def get_compressed(self, ind):
        itr = self.front
        while itr is not self.rear:
            if itr.index == int(ind):
                if itr.compressed is None:
                    return itr.original_path
                return itr.compressed
            itr = itr.next
        if itr.index == int(ind):
            if itr.compressed is None:
                return itr.original_path
            return itr.compressed

    def to_list(self):
        data = []
        if not self.isEmpty():
            itr = self.front
            while itr:
                data.append(itr.data)
                if itr == self.rear:
                    break
                itr = itr.next

        return data

    def prev(self):
        if self.pointer is not None:
            self.pointer = self.pointer.prev
        return self.get_data()

    def get_data(self):
        if self.pointer is not None:
            var = [f"original: {self.pointer.original_path}",
                   f"compressed: {str(self.pointer.compressed)}",
                   f"decompressed: {str(self.pointer.decompressed)}",
                   f"data now: {str(self.pointer.data)}"]
            return var
        else:
            return None


    def next(self):
        if self.pointer is not None:
            self.pointer = self.pointer.next
        return self.get_data()

    def peek(self):
        self.pointer = self.front
        if self.pointer:
            var = [f"original: {self.front.original_path}",
                   f"compressed: {str(self.front.compressed)}",
                   f"decompressed: {str(self.front.decompressed)}",
                   f"data now: {str(self.front.data)}"]
        else:
            var = [f"original: None",
                   f"compressed: None",
                   f"decompressed: None",
                   f"data now: None"]
        return var

    def printQ(self):
        if self.isEmpty():
            return print("kosong")
        itr = self.front
        while itr:
            if itr is self.rear:
                break
            print(itr.data,",index=", itr.index, end=" -> ")
            itr = itr.next
        print(itr.data,",index=", itr.index)

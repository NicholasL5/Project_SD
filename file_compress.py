import heapq
import os
import ast
import huffman_tree as h_tree
import copy


class Node:
    def __init__(self, char, count):
        self.char = char
        self.count = count
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.count < other.count

    def __eq__(self, other):
        if other is None:
            return False
        elif not isinstance(other, Node):
            return False
        else:
            return True if self.count == other.count else False


class FileCompress:
    def __init__(self):
        self.char_dict = {}
        self.heap = []
        self.code_dict = {}
        self.reverse_code = {}

    def buat_tree(self):
        node1 = heapq.heappop(self.heap)
        node2 = heapq.heappop(self.heap)
        parent_node = Node(None, node1.count + node2.count)
        parent_node.left = node1
        parent_node.right = node2
        heapq.heappush(self.heap, parent_node)

    def buat_heap(self, val):
        for i in val:
            heapq.heappush(self.heap, Node(i, int(val[i])))
        return self.heap

    def map_char(self, string):
        count = {}
        for char in string:
            if char not in count:
                count[char] = 1
            else:
                count[char] += 1

        return count

    def buat_code_util(self, node: Node, code):
        if node is None:
            return
        if node.char is not None:
            self.code_dict[node.char] = code
            self.reverse_code[code] = node.char

        self.buat_code_util(node.left, (code + "0"))
        self.buat_code_util(node.right, (code + "1"))

    def ganti_text(self, text):

        text_code = ""

        for char in text:
            text_code += self.code_dict[char]

        # untuk tambah supaya text jadi kelipatan 8
        pad = 8 - len(text_code) % 8
        # print(pad)
        for i in range(pad):
            text_code += "0"

        # menyimpan informasi kita menambahkan berapa kali padding
        # informasi diubah jadi bentuk binary juga
        padded_info = "{0:08b}".format(pad)
        # print(padded_info)
        text_code = padded_info + text_code
        return text_code

    def to_binary(self, text_code):
        b = bytearray()
        for i in range(0, len(text_code), 8):
            byte = text_code[i:i + 8]
            b.append(int(byte, 2))
        return b

    def buat_code(self):
        root = heapq.heappop(self.heap)
        code = ""
        self.buat_code_util(root, code)

    def compress(self, file):
        if "\\" in file:
            file = file.replace("\\", "/")

        parent_dir = ""
        file_dir, file_extension = os.path.splitext(file)
        # search / terakhir
        if "/" in file_dir:
            index = file_dir.rfind("/")
            parent_dir = file_dir[0:(index + 1)]
            file_name = file_dir[index+1:]
        else:
            file_name = file_dir
        # if "-" in file_name:
        #     ind1 = file_name.rfind("/")
        #     ind = file_name.rfind("-")
        #     check = file_name[ind] + "-compressed"
        # else:
        #     check = file_name + "-compressed"
        if "compressed" in file_dir:
            return True
        # buat folder compressed
        compressed_dir = parent_dir + "compressed/" + file_name + "-compressed/"
        if not os.path.exists(compressed_dir):
            os.makedirs(compressed_dir)
        # output = compressed + nama file + extension .bin
        output_path = compressed_dir + file_name + ".bin"
        # buat simpan data tabel code
        data_path = compressed_dir + "data.txt"

        with open(file, "r") as f:
            print('1')
            data = f.read()
            print('2')
            mapped = self.map_char(data)
            print('3')            
            code,r_code = h_tree.create_tree(mapped)
            print('4')            
            # print(mapped)
            # self.buat_heap(mapped)
            # while len(self.heap) != 1:
            #     self.buat_tree()
            # self.buat_code()
            # print(self.code_dict)
            self.code_dict = copy.deepcopy(code)
            self.reverse_code = copy.deepcopy(r_code)
            print('5')
            text_code = self.ganti_text(data)
            print('6')
            output = self.to_binary(text_code)
            print('7')
            tabel_code = str(self.reverse_code)
            print('8')

        with open(data_path, "w") as out:
            out.write(tabel_code)

        with open(output_path, "wb") as out:
            out.write(bytes(output))

        return output_path

    # ===============================================================

    def remove_padding(self, str_bits):
        padding_info = str_bits[:8]
        extra_padding = int(padding_info, 2)

        str_bits = str_bits[8:]

        encoded_text = str_bits[:(len(str_bits) - extra_padding) + 1]
        return encoded_text

    def decode(self, text):
        code = ''
        decoded = ''
        # print('reverse map', self.reverse_code)
        for bit in text:
            code += bit
            if code in self.reverse_code:
                character = self.reverse_code[code]
                decoded += character
                code = ''
        return decoded

    def decompress(self, file):
        if "\\" in file:
            file = file.replace("\\", "/")
        filename, extension = os.path.splitext(file)
        index = filename.rfind("/")
        data_path = filename[0:(index+1)] + "data.txt"
        with open(data_path, 'r') as code:
            file_data = code.read()
        # ubah string dictionary jadi dictionary
        self.reverse_code = ast.literal_eval(file_data)
        # output file
        output_path = filename + "-decompressed.txt"


        with open(file, 'rb') as f, open(output_path, 'w') as output:
            string_of_bits = ''

            byte = f.read(1)

            while len(byte) > 0:
                # print(byte)
                byte = ord(byte)
                # print(byte)
                # print(bin(byte))
                bits = bin(byte)[2:].rjust(8, '0')
                # print(bits)
                string_of_bits += bits
                byte = f.read(1)

            encoded = self.remove_padding(string_of_bits)
            decoded = self.decode(encoded)
            output.write(decoded)

        # print('decompressed')
        return output_path

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Que import Queue
import file_compress



def get_filename():
    global path_queue
    temp_q = Queue()

    file = filedialog.askopenfilenames(initialdir="D:\\projects\\python_projects",
                                       title="Select A File",
                                       filetypes=(("txt files", "*.txt"), ("all files", "*.*")))

    file = list(file)
    for i in range(len(file)):
        if not path_queue.enqueue(file[i]):
            file[i] = None

    update()

    path_queue.printQ()
    for i in file:
        if i is not None:
            temp_q.enqueue(i)
        else:
            print("item sudah ada")

    to_table(temp_q)



def to_table(queue: Queue):
    global counter
    for i in queue.to_list():
        index = i.rfind("/")
        mytree.insert(parent='', index='end', iid=str(counter), text="", values=(counter + 1, i[index + 1:len(i)]))
        counter += 1


def remove_all():
    global path_queue
    print(mytree.get_children())
    for i in mytree.get_children():
        mytree.delete(i)
        path_queue.dequeue_index((int(i)+1))
    update()



def compress():
    global path_queue
    test = file_compress.FileCompress()
    x = mytree.selection()

    if x:
        sub_que = path_queue.subque(x)
    else:
        x = path_queue.get_all_index()
        print(x)
        sub_que = path_queue.subque(x)
    print(x)
    print("subque", end=" ")
    sub_que.printQ()
    for i in range(len(x)):
        path = sub_que.dequeue()
        index = path.data.rfind(".")
        if path.data[index:] == ".bin":
            print("bukan text file")
        else:
            compressed_path = test.compress(path.data)
            if compressed_path == True:
                print("sudah pernah dicompress")
            else:
                path_queue.insert_compressed((int(x[i])+1), compressed_path)
                index = compressed_path.rfind("/")
                filename = compressed_path[index+1:]
                value = mytree.item(x[i], 'values')
                mytree.item(x[i], text="", values=(value[0], filename))
                print("updated: ", end="")
                path_queue.printQ()
    update()

def delete_compress():
    global path_queue
    x = mytree.selection()
    if x:
        path_queue.delete_compress(x)
    else:
        x = path_queue.get_all_index()
        path_queue.delete_compress(x)

    for i in range(len(x)):
        value = mytree.item(x[i], 'values')
        filename = path_queue.get_ori((int(x[i]) + 1))
        index = filename.rfind("/")
        filename = filename[index + 1:]
        mytree.item(x[i], text="", values=(value[0], filename))
    update()

def delete_decompress():
    global path_queue
    x = mytree.selection()
    if x:
        path_queue.delete_decompress(x)
    else:
        x = path_queue.get_all_index()
        path_queue.delete_decompress(x)

    for i in range(len(x)):
        value = mytree.item(x[i], 'values')
        filename = path_queue.get_compressed((int(x[i]) + 1))
        index = filename.rfind("/")
        filename = filename[index + 1:]
        mytree.item(x[i], text="", values=(value[0], filename))
    update()



def decompress():
    global path_queue
    test = file_compress.FileCompress()
    x = mytree.selection()

    if x:
        sub_que = path_queue.subque(x)
    else:
        x = path_queue.get_all_index()
        print(x)
        sub_que = path_queue.subque(x)
    print(x)
    print("subque", end=" ")
    sub_que.printQ()
    for i in range(len(x)):
        path = sub_que.dequeue()
        index = path.data.rfind(".")
        if path.data[index:] == ".txt":
            print("bukan binary file")
        else:
            decompressed_path = test.decompress(path.data)
            path_queue.insert_decompressed((int(x[i]) + 1), decompressed_path)
            index = decompressed_path.rfind("/")
            filename = decompressed_path[index + 1:]
            value = mytree.item(x[i], 'values')
            mytree.item(x[i], text="", values=(value[0], filename))
            print("updated: ", end="")
            path_queue.printQ()
    update()


def update():
    global path_queue
    text = path_queue.peek()
    label_ori.config(text=text[0])
    label_com.config(text=text[1])
    label_decom.config(text=text[2])
    label_data_now.config(text=text[3])


def next_node():
    global path_queue
    text = path_queue.next()
    label_ori.config(text=text[0])
    label_com.config(text=text[1])
    label_decom.config(text=text[2])
    label_data_now.config(text=text[3])


def prev_node():
    global path_queue
    text = path_queue.prev()
    label_ori.config(text=text[0])
    label_com.config(text=text[1])
    label_decom.config(text=text[2])
    label_data_now.config(text=text[3])


def remove_selection():
    global path_queue
    x = mytree.selection()
    for i in x:
        print(i)
        path_queue.dequeue_index(int(i)+1)
        path_queue.printQ()
        mytree.delete(i)
    update()


counter = 0
root = Tk()

add_frame = Frame(root)
add_frame.pack(pady=5)

Label(add_frame, text="Insert a File").grid(row=0, column=0)

path_queue = Queue()
root.geometry("700x700")
Button(root, text="Select Directory/Files", command=get_filename).pack()

mytree = ttk.Treeview(root)

# kolom
mytree['col'] = ("No.", "File")

# format kolom
mytree.column("#0", width=25, stretch=NO)
mytree.column("No.", anchor=W, width=50, minwidth=50)
mytree.column("File", anchor=CENTER, width=200)

mytree.heading("#0", text="", anchor=W)
mytree.heading("No.", text="No", anchor=W)
mytree.heading("File", text="Directory/Files", anchor=CENTER)

mytree.pack(pady=10)

# remove
remove_frame = Frame(root)
remove_frame.pack(pady=10)
Button(remove_frame, text="Remove All", width=15, command=remove_all).grid(row=0, column=0, padx=2)
Button(remove_frame, text="Remove Select", width=15, command=remove_selection).grid(row=0, column=1, padx=2)

# compress and decompress
compress_frame = Frame(root)
compress_frame.pack(pady=10)
# compress
Button(compress_frame, text="Compress", width=15, command=lambda: compress()).grid(row=0, column=0, padx=2)
# decompress
Button(compress_frame, text="Decompress", width=15, command=lambda: decompress()).grid(row=0, column=1, padx=2)

# next and prev
preview_frame = Frame(root)
preview_frame.pack(pady=10)
Button(preview_frame, text="Next", width=15, command=lambda: next_node()).grid(row=0, column=0, padx=2)
Button(preview_frame, text="Prev", width=15, command=lambda: prev_node()).grid(row=0, column=1, padx=2)

# compress and decompress delete
delete_frame = Frame(root)
delete_frame.pack(pady=10)
# compress
Button(delete_frame, text="Delete Compress", width=15, command=lambda: delete_compress()).grid(row=0, column=0, padx=2)
# decompress
Button(delete_frame, text="Delete Decompress", width=15, command=lambda: delete_decompress()).grid(row=0, column=1, padx=2)

label_ori = Label(root, text="")
label_com = Label(root, text="")
label_decom = Label(root, text="")
label_data_now = Label(root, text="")
label_ori.pack()
label_com.pack()
label_decom.pack()
label_data_now.pack()

root.mainloop()
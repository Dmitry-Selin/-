from tkinter.filedialog import *
from tkinter.messagebox import askyesnocancel
import pickle


class Widget:
    def __init__(self, menu):
        self.var = IntVar()
        self.__frame_n = Frame(menu, width=800, height=30, bg="PaleGreen", bd=4)
        self.__label_n = Label(self.__frame_n, text='№', font=14, bg='PaleGreen')
        self.__entry_n = Entry(self.__frame_n, width=77, font='Cambria 12', bd=2)
        self.__checkbutton_n = Checkbutton(self.__frame_n, variable=self.var, onvalue=1, offvalue=0, bg="PaleGreen")

        self.__frame_n.pack(fill=X, padx=5, pady=3)
        self.__label_n.pack(side='left')
        self.__entry_n.pack(side='left')
        self.__checkbutton_n.deselect()
        self.__checkbutton_n.pack()

    def set_label(self, text):
        self.__label_n['text'] = ('№' + str(text))

    def set_flag(self, value):
        if value:
            self.__checkbutton_n.select()
        else:
            self.__checkbutton_n.deselect()

    def set_entry(self, text):
        self.__entry_n.delete(0, END)
        self.__entry_n.insert(0, text)

    def answer(self):
        txt = self.__entry_n.get()
        return txt

    def flag(self):
        flag_n = self.var.get()
        return flag_n


def open_as():
    with open('text.pkl', 'rb') as my_file:
        content = pickle.load(my_file)
        i = 0
        while content:
            widget = list_of_widget[i]
            key_value = content.popitem()
            widget.set_entry(key_value[0])
            widget.set_flag(key_value[1])
            i += 1
        del i


def save():
    with open('text.pkl', 'wb') as my_file:
        for widget in list_of_widget:
            if not widget.answer():
                continue
            else:
                var = widget.flag()
                content_of_entry[widget.answer()] = var
        pickle.dump(content_of_entry, my_file)
        del var
        my_file.close()


def clear_all():
    for widget in list_of_widget:
        widget.set_entry('')
        widget.set_flag(0)


def see_of_change():
    content_of_entry_2 = dict()
    with open('text.pkl', 'rb') as my_file:
        for widget in list_of_widget:
            if not widget.answer():
                continue
            else:
                var = widget.flag()
                content_of_entry_2[widget.answer()] = var
        if (content_of_entry_2 != {}) and (content_of_entry_2 != pickle.load(my_file)):
            return True
        else:
            return False
    del content_of_entry_2
    my_file.close()


def exit_app():
    if see_of_change():
        result = askyesnocancel('To-do list', 'To save the changes?')
        if result is True:
            save()
            root.destroy()
        elif result is False:
            root.destroy()
        elif result is None:
            pass
    else:
        root.destroy()

root = Tk()
root.configure(background='PaleGreen')
root.geometry('800x425')
root.resizable(width=False, height=False)
root.title("To-do list")
# создание меню
str_menu = Menu()
root.config(menu=str_menu)

first_menu = Menu(str_menu, tearoff=0)
str_menu.add_cascade(label="File", menu=first_menu)

# меню
first_menu.add_command(label='Open', command=open_as)
first_menu.add_command(label='Save', command=save)
first_menu.add_separator()
first_menu.add_command(label='Exit', command=exit_app)

# заголовок таблицы
frame_1 = Frame(root, width=800, height=30, bg='PaleGreen')
lab = Label(frame_1, text="PLANED ACTIVITIES", font="Cambria 14", bg='PaleGreen')
frame_1.pack(fill=X, padx=5, pady=3)
lab.pack()

# панель инструментов
frame_2 = Frame(root, width=800, height=30, bg='PaleGreen')
save_button = Button(frame_2, text='Save', font="Cambria 11",
                     height=1, width=5, bg='MediumSpringGreen', command=save)
open_button = Button(frame_2, text='Open', font="Cambria 11",
                     height=1, width=5, bg='MediumSpringGreen', command=open_as)
clear_button = Button(frame_2, text='Clear', font="Cambria 11",
                      height=1, width=5, bg='MediumSpringGreen', command=clear_all)
save_button.pack(side=LEFT)
open_button.pack(side=LEFT)
clear_button.pack(side=LEFT)
frame_2.pack(side=BOTTOM)

# словарь {'значение' : flag}
content_of_entry = dict()
# список экземпляров класса Widget
list_of_widget = list()

for x in range(0, 9):
    list_of_widget.append(Widget(root))
for x in range(0, 9):
    list_of_widget[x].set_label(x + 1)

root.mainloop()

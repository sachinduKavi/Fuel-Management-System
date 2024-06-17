from tkinter import *


def sys_log(master):
    global canvas
    if __name__ == '__main__':
        sys_win = Tk()
    else:
        sys_win = Toplevel(master)
        sys_win.geometry(f'+{master.winfo_rootx()+100}+{master.winfo_rooty()-50}')
    sys_win.geometry('500x600')
    sys_win.resizable(width=True, height=False)
    sys_win.title('System log')
    sys_win.iconbitmap('img/setting.ico')

    # Heading
    Label(sys_win, text='System Log', font=('Arial', 20, 'bold'), fg='#636363').pack(pady=10)

    # Main frame
    main_frame = Frame(sys_win)
    main_frame.pack()

    # pack canvas
    canvas = Canvas(main_frame, width=480, height=520)
    canvas.pack(side=LEFT)
    # scroll
    scroll = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scroll.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scroll.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    # Content frame
    con_frame = Frame(canvas)
    canvas.create_window((0, 0), window=con_frame, anchor=NW)

    # Reading file sys_log
    sys_log_file = open('sys_log.txt', 'r')
    sys_file = sys_log_file.readlines()
    sys_log_file.close()
    log_list = []
    for record in sys_file:
        log_list.append(record[:-1])
    log_list.reverse()

    for record in log_list:
        Label(con_frame, text=record, font=('Arial', 12, 'bold')).pack(pady=5, padx=2, anchor=W)

    sys_win.mainloop()


def on_mousewheel(event):
    canvas.yview_scroll(int(-1*event.delta/120), 'units')


if __name__ == '__main__':
    sys_log(None)

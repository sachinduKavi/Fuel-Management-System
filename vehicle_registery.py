from tkinter import *
from database_connection import db_connection
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
from datetime import date


def register_start(master, syatem_name, user):
    global reg_win, sys_name, user_name
    sys_name = syatem_name

    if __name__ == "__main__":
        reg_win = Tk()
    else:
        reg_win = Toplevel(master)
        reg_win.geometry(f"+{master.winfo_rootx()}+{master.winfo_rooty()}")
        master.grab_set()
    reg_win.title(f"Registry - {sys_name.replace('_', ' ')}")
    reg_win.geometry("700x500")
    reg_win.iconbitmap("img/setting.ico")
    reg_win.resizable(width=False, height=False)
    reg_win.protocol("WM_DELETE_WINDOW", on_closing)

    # Heading
    heading_frame = Frame(reg_win)
    heading_frame.pack(anchor=W, fill=X)

    Label(heading_frame, text="Vehicle Registry", font=("Arial", 20, "bold"), fg='#7D7D7D').pack(anchor=W, padx=10,
                                                                                                 pady=10, side=LEFT)
    list_img = ImageTk.PhotoImage(Image.open('img/list.jpg').resize((30, 30), Image.Resampling.LANCZOS))
    Button(heading_frame, image=list_img, borderwidth=0, command=file_read).pack(side=RIGHT, padx=30)

    # windows menus
    main_menu = Menu(reg_win)
    option_menu = Menu(main_menu, tearoff=0)
    option_menu.add_command(label='Refresh', command=refresh_main_frame)
    option_menu.add_command(label='Delete All', command=delete_all)
    main_menu.add_cascade(label='Options', menu=option_menu)

    reg_win.config(menu=main_menu)

    registry_main()
    reg_win.mainloop()


def on_closing():
    reg_win.quit()
    reg_win.destroy()
    canvas.destroy()


def delete_all():
    ans = messagebox.askyesno("Confirm", 'Are you sure you want to delete all registered vehicles ?', parent=reg_win)
    if ans:
        log_file = open('sys_log.txt', 'a')
        log_file.write(f'{date.today()} >> Vehicle register has been deleted by {user_name}\n')
        log_file.close()
        database, cursor = db_connection(sys_name)
        cursor.execute("DELETE FROM vehicle_register")
        database.commit()
        refresh_main_frame()


def file_read():
    try:
        file_location = filedialog.askopenfilename(parent=reg_win)
        file_data = open(file_location, 'r', encoding='utf8').readlines()
        database, cursor = db_connection(sys_name)
        for row in file_data:
            reg_num, veh_name, pg_num, fuel = row.rstrip('\n').split('#')
            reg_num = reg_num.upper()
            cursor.execute(f"INSERT INTO vehicle_register VALUES('{reg_num}', '{veh_name}', '{pg_num}', '{fuel}')")
        database.commit()
        print("Vehicle registration successful")
        refresh_main_frame()
    except:
        messagebox.showerror("Error", "Incorrect file type or duplicates exists", parent=reg_win)


def registry_main():
    global main_frame, canvas
    # Connecting database
    data_base, cursor = db_connection(sys_name)
    main_frame = Frame(reg_win)
    main_frame.pack(fill=X)

    # Canvas
    canvas = Canvas(main_frame, width=670, height=430)
    canvas.pack(fill=X, padx=5, side=LEFT)
    # Scroll bar
    scroll = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scroll.pack(side=RIGHT, fil=Y)
    canvas.configure(yscrollcommand=scroll.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # Frame for tables
    table_frame = Frame(canvas)
    canvas.create_window((0, 0), window=table_frame, anchor=NW)

    # Headings of the tables
    border_frame = Frame(table_frame)
    border_frame.grid(row=0, column=0, pady=5, sticky=EW)
    Label(border_frame, text='Registration\nNumber', font=("Arial", 10, "bold"), bg='#2D7070', fg='white', height=2,
          borderwidth=3, padx=3, width=20).pack(pady=5, padx=5)
    border_frame = Frame(table_frame)
    border_frame.grid(row=0, column=1, pady=5, sticky=EW)
    Label(border_frame, text='Vehicle type', font=("Arial", 10, "bold"), bg='#2D7070', fg='white', height=2, padx=3,
          width=32).pack(pady=5, padx=5, fill=X)
    border_frame = Frame(table_frame)
    border_frame.grid(row=0, column=2, pady=5, sticky=EW)
    Label(border_frame, text='Page No', font=("Arial", 10, "bold"), bg='#2D7070', fg='white', height=2, padx=3).pack(
        pady=5, padx=5)
    border_frame = Frame(table_frame)
    border_frame.grid(row=0, column=3, pady=5, sticky=EW)
    Label(border_frame, text='Fuel type', font=("Arial", 10, "bold"), bg='#2D7070', fg='white', height=2, padx=3).pack(
        pady=5, padx=5)
    border_frame = Frame(table_frame)
    border_frame.grid(row=0, column=4, pady=5, sticky=EW)
    Label(border_frame, text='Delete', font=("Arial", 10, "bold"), bg='#2D7070', fg='white', height=2, padx=3).pack(
        pady=5, padx=5)

    # Extracting registry from database
    cursor.execute("SELECT * FROM vehicle_register ORDER BY reg_num ASC")
    vehicle_reg = cursor.fetchall()
    print(vehicle_reg)
    row = 1
    del_btn_img = ImageTk.PhotoImage(Image.open("img/del.png").resize((20, 20), Image.Resampling.LANCZOS))
    for record in vehicle_reg:
        column = 0
        count = 0
        for data in record:
            if column == 0:
                reg = data
            if count == 1:
                font_t = "Iskoola Pota"
            else:
                font_t = "Arial"
            Label(table_frame, text=data, font=(font_t, 12, "bold"), fg='#4F4B4B').grid(row=row, column=column, pady=2,
                                                                                        sticky=W, padx=13)
            column += 1
            count += 1
        Button(table_frame, image=del_btn_img, command=lambda value=reg: delete_rec(value), borderwidth=0).grid(row=row, column=column)
        row += 1

    mainloop()


def on_mousewheel(event):
    canvas.yview_scroll(int(-1*event.delta/120), 'units')


# Deleting record from database
def delete_rec(reg_no):
    ans = messagebox.askyesno("Delete confirm", "I understand that deleting registration will affect to whole database\n Click YSE to confirm delete", parent=reg_win)
    if ans:
        log_file = open('sys_log.txt', 'a')
        log_file.write(f'{date.today()} >> Register record {reg_no} is deleted\n')
        log_file.close()
        data_base, cursor = db_connection(sys_name)
        cursor.execute(f"DELETE FROM vehicle_register WHERE reg_num='{reg_no}'")
        data_base.commit()
        refresh_main_frame()


def refresh_main_frame():
    main_frame.forget()
    for child in main_frame.winfo_children():
        child.destroy()
    registry_main()


if __name__ == '__main__':
    register_start(None, "OR_SYSTEM_2022")

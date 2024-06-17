from tkinter import *
from PIL import ImageTk, Image
from database_connection import db_connection
from tkinter import messagebox
from datetime import date

times = True
number_str = ''


def delete_update_start(master, system_name, user):
    global delete_win, sys_name, result_frame, month_list, box_frame, user_name
    user_name = user
    sys_name = system_name
    database, cursor = db_connection(sys_name)
    if __name__ == '__main__':
        delete_win = Tk()
    else:
        delete_win = Toplevel(master)
        delete_win.geometry(f"+{master.winfo_rootx() + 30}+{master.winfo_rooty() + 30}")
    delete_win.geometry("600x430")
    delete_win.title("Update records")
    delete_win.iconbitmap('img/setting.ico')
    delete_win.resizable(width=False, height=False)

    # Heading
    Label(delete_win, text='Delete / Update', font=('Arial', 20, 'bold'), fg='#99A1A0').pack(anchor=W, padx=10, pady=10)

    # Search frame & search button and entry
    search_frame = Frame(delete_win)
    search_frame.pack(anchor=W, padx=30)
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
    # OR number
    Label(search_frame, text="OR Number :  OR", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=E)
    or_num = Entry(search_frame, font=('Arial', 12, 'bold'), width=4)
    or_num.grid(row=0, column=1, padx=10, sticky=W)
    search_img = ImageTk.PhotoImage(Image.open("img/search.png").resize((70, 30), Image.Resampling.LANCZOS))
    serach_btn = Button(search_frame, image=search_img, borderwidth=0, command=lambda: results(or_num))
    serach_btn.grid(row=0, column=2)

    big_border = Frame(delete_win, bg='#D1CDCD')
    big_border.pack(fill=BOTH, expand=True, pady=3, padx=20)
    box_frame = Frame(big_border, bg='#E8E8E8')
    box_frame.pack(pady=3, padx=3)

    delete_win.mainloop()


def refresh_results():
    hide_box()
    box_frame.pack()


def hide_box():
    global number_str
    for child in box_frame.winfo_children():
        child.destroy()
    box_frame.forget()
    number_str = ''


def results(or_num):
    database, cursor = db_connection(sys_name)
    # Check whether reg_num is registered in the database
    global c_month, month_label, c_num, pg_number, liters_e, calculation_label, result_frame, times, or_number, pre_page_num, liters_e, unit_price, number_str
    or_number = or_num.get()
    print(or_number)
    or_num.delete(0, END)
    cursor.execute(f"SELECT * FROM oil_records WHERE or_num='{or_number}'")
    result = cursor.fetchall()
    cursor.execute(f"SELECT * FROM vehicle_register WHERE reg_num='{result[0][3]}'")
    vehicle_info = cursor.fetchall()[0]
    if not times:
        refresh_results()
    times = False
    result_frame = Frame(box_frame)
    result_frame.pack(pady=10)
    if len(result) == 1:
        global unit
        result = result[0]
        # Result frame
        c_month = result[2]
        c_num = month_list.index(c_month)
        # Arrow images
        left_img = ImageTk.PhotoImage(Image.open("img/left.png").resize((40, 40), Image.Resampling.LANCZOS))
        right_img = ImageTk.PhotoImage(Image.open("img/right.png").resize((40, 40), Image.Resampling.LANCZOS))

        month_frame = Frame(result_frame)
        month_frame.pack()

        Button(month_frame, image=right_img, borderwidth=0, command=lambda: change_month('-')).pack(side=LEFT)
        middle_frame = Frame(month_frame, width=200, height=50)
        middle_frame.pack(side=LEFT, expand=True)
        month_label = Label(middle_frame, text=c_month, font=('Arial', 12, 'bold'), width=200)
        month_label.pack(side=LEFT)
        middle_frame.pack_propagate(0)
        Button(month_frame, image=left_img, borderwidth=0, command=lambda: change_month('+')).pack(side=RIGHT)

        border_frame = Frame(result_frame, bg='#B80000')
        border_frame.pack(padx=10, pady=20)
        reg_frame = Frame(border_frame)
        reg_frame.pack(padx=3, pady=3)
        Label(reg_frame, text='OR' + str(or_number), font=('Arial', 12, 'bold')).pack(side=LEFT)
        Label(reg_frame, text='Registration : ' + str(result[3]), font=('Arial', 12, 'bold')).pack(side=LEFT, padx=10)
        Label(reg_frame, text='Vehicle type : ' + str(vehicle_info[1]), font=('Iskoola Pota', 12, 'bold')).pack(side=LEFT, padx=10)

        # Page number
        page_frame = Frame(result_frame)
        page_frame.pack(pady=5)
        Label(page_frame, text='Page No : ', font=('Arial', 12, 'bold')).pack(side=LEFT)
        Button(page_frame, text="<<", font=('Arial', 12, 'bold'), borderwidth=0, command=lambda: change_page('-')).pack(side=LEFT)
        mini_frame = Frame(page_frame, width=50, height=30)
        mini_frame.pack(side=LEFT, padx=5)
        mini_frame.pack_propagate(0)
        pg_number = Entry(mini_frame, font=('Arial', 12, 'bold'), justify=CENTER)
        pg_number.pack()
        pre_page_num = result[4]
        pg_number.insert(END, pre_page_num)
        Button(page_frame, text=">>", font=('Arial', 12, 'bold'), borderwidth=0, command=lambda: change_page('+')).pack(side=RIGHT)

        # Fuel calculation
        fuel_frame = Frame(result_frame)
        fuel_frame.pack()
        Label(fuel_frame, text=f'Fuel Type : ', font=('Arial', 12, 'bold')).grid(row=0, column=0)
        Label(fuel_frame, text=f'{vehicle_info[3]}', font=('Arial', 12, 'bold')).grid(row=0, column=1)
        Label(fuel_frame, text='Liters : ', font=('Arial', 12, 'bold')).grid(row=1, column=0)
        liters_e = Entry(fuel_frame, font=('Arial', 12, 'bold'), width=7, justify=RIGHT)
        liters_e.grid(row=1, column=1, padx=5, sticky=W)
        liters_e.insert(END, result[6])
        unit = result[5]
        liters_e.bind("<KeyRelease>", calculation)
        unit_price = float(result[5])
        calculation_label = Label(fuel_frame, text=f"{result[6]} x {unit_price} = Rs. {result[7]:.2f}", font=('Arial', 12, 'bold'))
        calculation_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Update delete button
        update_img = ImageTk.PhotoImage(Image.open("img/update.png").resize((90, 50), Image.Resampling.LANCZOS))
        del_img = ImageTk.PhotoImage(Image.open("img/del.png").resize((40, 40), Image.Resampling.LANCZOS))
        cancel_img = ImageTk.PhotoImage(Image.open("img/cancel.png").resize((85, 36), Image.Resampling.LANCZOS))

        btn_frame = Frame(result_frame)
        btn_frame.pack(pady=(5, 0))

        Button(btn_frame, image=update_img, borderwidth=0, command=lambda: update_data(or_number)).pack(side=LEFT, padx=10)
        Button(btn_frame, image=cancel_img, borderwidth=0, command=hide_box).pack(side=LEFT, padx=10)
        Button(btn_frame, image=del_img, borderwidth=0, command=lambda: delete_rec(or_number)).pack(side=LEFT, padx=10)
    else:
        messagebox.showerror("Error", "No results found please try again", parent=delete_win)

    mainloop()


def delete_rec(or_num):
    ans = messagebox.askyesno("Confirmation", "Confirm YES to continue delete", parent=delete_win)
    if ans:
        log_file = open('sys_log.txt', 'a')
        log_file.write(f'{date.today()} >> Oil record {or_num} is deleted by {user_name}\n')
        log_file.close()
        data_base, cursor = db_connection(sys_name)
        cursor.execute(f"DELETE FROM oil_records WHERE or_num='{or_num}'")
        hide_box()
        data_base.commit()


def update_data(or_numb):
    database, cursor = db_connection(sys_name)
    # Check whether page number is changed
    page_number = pg_number.get()
    liters = float(liters_e.get())
    row_price = liters * unit_price
    # Updating the database
    cursor.execute(f"UPDATE oil_records SET month='{c_month}', pg_num='{page_number}', fuel_l='{liters}', r_price='{row_price}' WHERE or_num='{or_numb}'")
    database.commit()
    hide_box()
    messagebox.showinfo("Successful", "Record updated successfully", parent=delete_win)
    log_file = open('sys_log.txt', 'a')
    log_file.write(f'{date.today()} >> Record {or_numb} is updated by {user_name}\n')
    log_file.close()


def calculation(event):
    print(event)
    global number_str, ans_e
    try:
        float(event.keysym)
        number_str += event.keysym
    except ValueError:
        if event.keysym == 'BackSpace' and len(number_str) > 0:
            number_str = number_str[:-1]
        elif event.keysym == 'period':
            number_str += "."

    liters_e.delete(0, END)
    liters_e.insert(END, number_str)
    # Updating the answer
    final_ans = unit * float(number_str)
    calculation_label.config(text=f"{unit} X {number_str}  = Rs.{final_ans:.2f}")


def change_page(sign):
    pg_num = int(pg_number.get())
    if sign == '+':
        pg_num += 1
    elif sign == '-':
        pg_num -= 1
    pg_number.delete(0, END)
    pg_number.insert(END, pg_num)


def change_month(sign):
    global c_month, c_num
    if sign == '+' and c_num < 11:
        c_num += 1
    elif sign == '-' and c_num > 0:
        c_num -= 1
    c_month = month_list[c_num]
    month_label.config(text=c_month)


if __name__ == '__main__':
    delete_update_start(None, 'OR_SYSTEM_2022')
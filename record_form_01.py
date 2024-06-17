import datetime
from tkinter import *
from database_connection import db_connection
from datetime import date
from PIL import ImageTk, Image
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from vehicle_registery import register_start

new_re_state = False
mini_f = True


def new_record_start(master, sys_name, petrol_p, diesel_p, user):
    global new_re_state, user_name
    user_name = user
    new_re_state = True
    global rec_win
    if __name__ == '__main__':
        rec_win = Tk()
    else:
        rec_win = Toplevel(master)
        rec_win.geometry(f"+{master.winfo_rootx()+50}+{master.winfo_rooty()+-10}")
    rec_win.geometry('420x500')
    rec_win.iconbitmap("img/setting.ico")
    rec_win.title(f'New Record - {sys_name.upper()} - User : {user}')
    rec_win.protocol("WM_DELETE_WINDOW", on_closing)
    rec_win.resizable(width=False, height=False)
    new_record(master, sys_name, petrol_p, diesel_p)


def on_closing():
    global mini_f
    mini_f = True
    rec_win.quit()
    rec_win.destroy()


def new_record(master, sys_name, petrol_p, diesel_p):
    global month_value, month_list, month_num, month_label, rec_win, main_frame
    # Database initialize
    data_base, cursor = db_connection(sys_name)

    main_frame = Frame(rec_win)
    main_frame.pack(fill=BOTH, expand=True)
    # New record label
    Label(main_frame, text='New Record', font=('Arial', 20, 'bold'), fg='#707070').pack(anchor=W, padx=10, pady=(5, 3))

    # Month Frame
    month_frame = Frame(main_frame, bg='#068A9C', height=40)
    month_frame.pack(fill=X)
    # Extracting month
    month_num = int(str(date.today())[5:7])
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_value = month_list[month_num-1]

    # Button Image
    left_img = ImageTk.PhotoImage(Image.open("img/left.png").resize((40, 40), Image.Resampling.LANCZOS))
    right_img = ImageTk.PhotoImage(Image.open("img/right.png").resize((40, 40), Image.Resampling.LANCZOS))

    # Month label and its frame
    Button(month_frame, image=right_img, borderwidth=0, bg='#068A9C', command=lambda: change_month("-"), activebackground='#068A9C').pack(side=LEFT, padx=(70, 0))
    middle_frame = Frame(month_frame, bg='#068A9C')
    middle_frame.pack(side=LEFT, expand=True)
    month_label = Label(middle_frame, text=month_value, font=('Arial', 20, 'bold'), fg='white', bg='#068A9C')
    month_label.pack()
    Button(month_frame, image=left_img, borderwidth=0, bg='#068A9C', command=lambda: change_month("+"), activebackground='#068A9C').pack(side=RIGHT, padx=(0, 70))

    # Add vehicle or machine button and view records buttons
    add_img = ImageTk.PhotoImage(Image.open("img/add.png").resize((60, 25)))
    details_img = ImageTk.PhotoImage(Image.open("img/details.jpg").resize((25, 25)))

    view_button_frame = Frame(main_frame)
    view_button_frame.pack(padx=20, anchor=W, fill=X, pady=(10, 0))
    # add vehicle button
    Button(view_button_frame, image=details_img, borderwidth=0, command=lambda :register_start(rec_win, sys_name)).pack(side=LEFT)
    # Vehicle registration command
    Button(view_button_frame, image=add_img, borderwidth=0, command=lambda: vehicle_reg(rec_win, sys_name)).pack(side=RIGHT)

    # Registration label and entry box frame
    reg_frame = Frame(main_frame)
    reg_frame.pack(pady=(10, 5))
    # Fetching registration numbers from vehicle_register for list name reg_list
    cursor.execute("SELECT reg_num FROM vehicle_register")
    register = cursor.fetchall()
    reg_list = []
    for reg_numb in register:
        reg_list.append(reg_numb[0])

    Label(reg_frame, text=' Registration No :  ', font=('Arial', 10, 'bold')).pack(side=LEFT)
    reg_num = AutocompleteCombobox(reg_frame, completevalues=reg_list, font=('Arial', 10, 'bold'), width=10)
    reg_num.pack(side=LEFT)
    # Search button
    search_img = ImageTk.PhotoImage(Image.open("img/search.png").resize((70, 30), Image.Resampling.LANCZOS))
    Button(reg_frame, image=search_img, borderwidth=0, command=lambda: new_record_searched(reg_num, data_base, cursor)).pack(side=LEFT, padx=10)

    # Extracted data frame
    global ext_frame
    ext_frame = Frame(main_frame, bg='#DBDBDB', height=230)
    ext_frame.pack(fill=X, padx=5)
    ext_frame.propagate(0)

    # Submit button to data submission
    global sub_btn
    sub_img = ImageTk.PhotoImage(Image.open("img/submit.png").resize((100, 50), Image.Resampling.LANCZOS))
    sub_btn = Button(main_frame, image=sub_img, borderwidth=0, state=DISABLED, command=lambda: record_submission(sys_name))
    sub_btn.pack(pady=15)

    # Menu in rec_win
    action_menu = Menu(rec_win)
    action_menu.add_command(label='Reload', command=lambda: refresh_new_rec(master, sys_name, petrol_p, diesel_p))
    rec_win.config(menu=action_menu)

    mainloop()


# Mini box appears after clicked search
def new_record_searched(reg_num, data_base, cursor):
    global mini_frame, mini_f, veh_typo_final, pg_num_final, fuel_typo, unit_e, regis_num, dep_var
    forget_min_frame()
    mini_f = False
    mini_frame = Frame(ext_frame, bg='#DBDBDB')
    mini_frame.pack(pady=20)
    regis_num = reg_num.get()
    reg_num.delete(0, END)
    cursor.execute(f"SELECT * FROM vehicle_register WHERE reg_num='{regis_num}'")
    result = cursor.fetchall()
    print(result)
    if len(result) == 1:
        # Registration number
        Label(mini_frame, text=f'Registration No : {result[0][0]}', font=('Arial', 14, 'bold'), bg='#DBDBDB', fg='red').grid(row=0, column=0, pady=5, columnspan=2)

        # Vehicle Type
        Label(mini_frame, text='Vehicle Type : ', font=('Arial', 10, 'bold'), bg='#DBDBDB').grid(row=1, column=0, pady=5)
        veh_typo_final = Entry(mini_frame, font=("Iskoola Pota", 12, 'bold'), width=25)
        veh_typo_final.grid(row=1, column=1)
        veh_typo_final.insert(END, result[0][1])

        # Page Number
        Label(mini_frame, text="Page No : ", font=('Arial', 10, 'bold'), bg='#DBDBDB').grid(row=2, column=0, pady=5, sticky=E)
        btn_frame = Frame(mini_frame)
        btn_frame.grid(row=2, column=1)
        Button(btn_frame, text="<<", font=('Arial', 10, 'bold'), borderwidth=0, bg='#DBDBDB', command=lambda: page_num_increment("-")).pack(side=LEFT)
        pg_num_final = Entry(btn_frame, font=('Arial', 10, 'bold'), width=4, justify=CENTER)
        pg_num_final.pack(side=LEFT)
        pg_num_final.insert(END, result[0][2])
        Button(btn_frame, text=">>", font=('Arial', 10, 'bold'), borderwidth=0, bg='#DBDBDB', command=lambda: page_num_increment("+")).pack(side=LEFT)

        # Fuel Type
        Label(mini_frame, text='Fuel Type : ', font=('Arial', 10, 'bold'), bg='#DBDBDB').grid(row=3, column=0, pady=5, sticky=E)
        fuel_typo = Entry(mini_frame, font=('Arial', 10, 'bold'), width=8)
        fuel_typo.grid(row=3, column=1)
        fuel_typo.insert(END, result[0][3])
        # Unit price
        global unit
        if result[0][3] == "Petrol":
            cursor.execute("SELECT petrol_u FROM sys_info")
            unit = cursor.fetchall()[0][0]
        elif result[0][3] == "Diesel":
            cursor.execute("SELECT diesel_u FROM sys_info")
            unit = cursor.fetchall()[0][0]
        else:
            unit = "Error"

        unit_e = Entry(mini_frame, font=('Arial', 10, 'bold'), width=6)
        unit_e.grid(row=3, column=2)
        unit_e.insert(END, unit)
        unit_e.config(stat=DISABLED)
        Label(mini_frame, text='unit price', font=('Arial', 8, 'bold')).grid(row=3, column=3, padx=5)

        # Liters calculator
        global liter_e, result_l, ans_e
        liter_frame = Frame(mini_frame, pady=20, bg='#DBDBDB')
        liter_frame.grid(row=4, column=0, columnspan=4)
        Label(liter_frame, text="Liters : ", font=('Arial', 13, 'bold'), bg='#DBDBDB').pack(side=LEFT)
        liter_e = Entry(liter_frame, font=('Arial', 13, 'bold'), width=5, justify=RIGHT)
        liter_e.bind("<KeyRelease>", liter_cal)
        liter_e.pack(side=LEFT)
        # Calculated result
        result_l = Label(liter_frame, text="???", font=('Arial', 13, 'bold'), bg='#DBDBDB')
        result_l.pack(side=LEFT, padx=10)
        ans_e = Entry(liter_frame, font=('Arial', 13, 'bold'), width=10)
        ans_e.pack(side=LEFT)


number_str = ""


def liter_cal(event):
    global number_str, ans_e
    sub_btn.config(state=NORMAL)
    try:
        float(event.keysym)
        number_str += event.keysym
    except ValueError:
        if event.keysym == 'BackSpace' and len(number_str) > 0:
            number_str = number_str[:-1]
        elif event.keysym == 'period':
            number_str += "."

    liter_e.delete(0, END)
    liter_e.insert(END, number_str)
    # Updating the answer
    if not unit == "Error":
        final_ans = unit*float(number_str)
        result_l.config(text=f"{unit} X {number_str}  = ")
        ans_e.delete(0, END)
        ans_e.insert(END, final_ans)
    else:
        ans_e.delete(0, END)


def record_submission(sys_name):
    global number_str
    cur_date = datetime.date.today()
    data_base, cursor = db_connection(sys_name)
    # veh_typo_final, pg_num_final, fuel_typo, unit
    # Database check with values for any changes
    cursor.execute(f"SELECT * FROM vehicle_register WHERE reg_num='{regis_num}'")
    validate_results = cursor.fetchall()
    print("validate results", validate_results)
    if len(validate_results) == 1:
        if not(validate_results[0][1] == veh_typo_final.get() and validate_results[0][3] == fuel_typo.get()):
            answer = messagebox.showerror("Error", "Values in the register has been changed do you want to continue with new values", parent=rec_win)
        else:
            answer = True
        if answer:
            cursor.execute(f"UPDATE vehicle_register SET type='{veh_typo_final.get()}', current_page='{pg_num_final.get()}', fuel_type='{fuel_typo.get()}' WHERE reg_num='{regis_num}'")
            # inserting new records into oil records
            cursor.execute(f"INSERT INTO oil_records(dte, month, vehicle_reg, pg_num, fuel_price, fuel_l, r_price) VALUES("
                           f"'{cur_date}',"
                           f"'{month_value}',"
                           f"'{regis_num}',"
                           f"'{pg_num_final.get()}',"
                           f"'{unit}',"
                           f"'{number_str}',"
                           f"'{ans_e.get()}')")
            data_base.commit()
            log_file = open('sys_log.txt', 'a')
            log_file.write(f'{date.today()} >> New record inserted by {user_name}\n')
            log_file.close()
            messagebox.showinfo("Successful", "Record created successfully", parent=rec_win)
            forget_min_frame()
            number_str = ""


# Incrementing page number
def page_num_increment(sign):
    value = int(pg_num_final.get())
    if sign == "+":
        value += 1
    else:
        value -= 1
    pg_num_final.delete(0, END)
    pg_num_final.insert(END, str(value))


def forget_min_frame():
    global mini_f
    if not mini_f:
        for child in mini_frame.winfo_children():
            child.destroy()
        mini_frame.forget()
        sub_btn.config(state=DISABLED)


# Reloading new record window
def refresh_new_rec(master, sys_name, petrol_p, diesel_p):
    global mini_f
    mini_f = True
    main_frame.forget()
    for child in main_frame.winfo_children():
        child.destroy()
    new_record(master, sys_name, petrol_p, diesel_p)


# Changing month from button click
def change_month(sign):
    global month_num, month_value
    if sign == "+" and month_num < 12:
        month_num += 1
    elif sign == "-" and month_num > 1:
        month_num -= 1
    month_value = month_list[month_num-1]
    month_label.config(text=month_value)


# To enter new vehicle or machine to the database
def vehicle_reg(master, sys_name):
    global vehicle_win
    vehicle_win = Toplevel(master)
    vehicle_win.geometry('500x300')
    vehicle_win.title(f"Vehicle Register - {sys_name.upper()}")
    vehicle_win.protocol('WM_DELETE_WINDOW', closing_vehicle_win)

    # Vehicle Register label
    Label(vehicle_win, text='Vehicle Register', font=('Arial', 20, 'bold'), fg='#707070').pack(pady=5)

    # Details about de vehicle
    detail_frame = Frame(vehicle_win)
    detail_frame.pack()
    # Registration number
    Label(detail_frame, text='Registration No', font=("Arial", 15, 'bold'), fg='#707070').grid(row=0, column=0, sticky=E)
    Label(detail_frame, text=' : ', font=("Arial", 15, 'bold'), fg='#707070').grid(row=0, column=1)
    reg_num = Entry(detail_frame, font=("Arial", 15, 'bold'), width=12)
    reg_num.grid(row=0, column=2, sticky=W, pady=5)
    # Vehicle or machine type
    Label(detail_frame, fg='#707070', font=("Arial", 15, 'bold'), text='Vehicle Type (S)').grid(row=1, column=0, sticky=E)
    Label(detail_frame, text=' : ', font=("Arial", 15, 'bold'), fg='#707070').grid(row=1, column=1)
    vehicle_typo = Entry(detail_frame, font=("Arial", 15, 'bold'), width=18)
    vehicle_typo.grid(row=1, column=2, sticky=W, pady=5)
    # Current page number of the oli book
    Label(detail_frame, text="Current Page", fg='#707070', font=("Arial", 15, 'bold')).grid(row=2, column=0, sticky=E)
    Label(detail_frame, text=' : ', font=("Arial", 15, 'bold'), fg='#707070').grid(row=2, column=1)
    current_page = Entry(detail_frame, font=("Arial", 15, 'bold'), width=4)
    current_page.grid(row=2, column=2, sticky=W, pady=5)
    # Fuel type
    fuel_var = StringVar()
    fuel_var.set("Petrol")

    Label(detail_frame, text='Fuel Type', fg='#707070', font=("Arial", 15, 'bold')).grid(row=3, column=0, sticky=E)
    # Radio frame for radio buttons
    radio_frame = Frame(detail_frame, pady=5)
    radio_frame.grid(row=3, column=2, columnspan=2, sticky=SW)
    Radiobutton(radio_frame, text="Petrol", variable=fuel_var, value='Petrol', font=("Arial", 10, 'bold')).pack(side=LEFT, padx=3)
    Radiobutton(radio_frame, text="Diesel", variable=fuel_var, value='Diesel', font=("Arial", 10, 'bold')).pack(side=LEFT, padx=3)

    # Submit Image
    sub_img = ImageTk.PhotoImage(Image.open("img/submit.png").resize((100, 50), Image.Resampling.LANCZOS))
    Button(vehicle_win, image=sub_img, borderwidth=0, command=lambda: vehicle_reg_sub(reg_num, vehicle_typo, current_page, fuel_var, sys_name)).pack(pady=10)

    mainloop()


# Inserting values to database
def vehicle_reg_sub(reg_num, vehicle_typo, current_page, fuel_var, sys_name):
    reg_number = reg_num.get().upper()
    if len(current_page.get()) == 0:
        messagebox.showinfo("Error", "Page number cannot be Empty", parent=vehicle_win)
    else:
        data_base, cursor = db_connection(sys_name)
        # Check for duplicates from the database
        cursor.execute(F"SELECT * FROM vehicle_register WHERE reg_num='{reg_number}'")
        count = cursor.fetchall()
        print(count)
        if len(count) == 0:
            cursor.execute(f"INSERT INTO vehicle_register VALUES('{reg_number}', '{vehicle_typo.get()}', '{current_page.get()}', '{fuel_var.get()}')")
            messagebox.showinfo("Successful", "Vehicle Registration Successful", parent=vehicle_win)
            # Clear data from entry boxes
            reg_num.delete(0, END)
            vehicle_typo.delete(0, END)
            current_page.delete(0, END)
            fuel_var.set("Petrol")
            data_base.commit()
        else:
            messagebox.showerror("Data Error", f"Duplicate found in your database in register number {reg_number}", parent=vehicle_win)


def closing_vehicle_win():
    global new_re_state
    if new_re_state:
        messagebox.showinfo("Closing", "Reload the new record window to update", parent=vehicle_win)
    vehicle_win.destroy()


if __name__ == '__main__':
    new_record_start(None, 'or_system_2022', 420, 400)

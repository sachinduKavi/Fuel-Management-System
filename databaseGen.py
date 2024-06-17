from tkinter import *
from PIL import ImageTk, Image
import mysql.connector
from tkinter import messagebox
from datetime import date

# To generate new databases for mysql this file uses database year from user


def data_entry(year):
    # Connecting database
    data_base = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root'
    )
    # Initiate cursor
    cursor = data_base.cursor()

    year = str(year.get())
    dte = date.today()

    # Check database name in valid range
    if len(year) == 4:
        try:
            year = "OR_SYSTEM_" + year
            print('database name', year)
            cursor.execute(f'CREATE DATABASE {year}')
            # ReConnecting database
            data_base = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database=year
            )
            # ReInitiate cursor
            cursor = data_base.cursor()

            # Creating vehicle register table
            cursor.execute("CREATE TABLE vehicle_register("
                           "reg_num VARCHAR(255) PRIMARY KEY,"
                           "type NVARCHAR(255),"
                           "current_page INT,"
                           "fuel_type NVARCHAR(255))")

            # Creating oil records table
            cursor.execute("CREATE TABLE oil_records("
                           "dte VARCHAR(255),"
                           "or_num INT AUTO_INCREMENT PRIMARY KEY,"
                           "month VARCHAR(255),"
                           "vehicle_reg VARCHAR(255),"
                           "pg_num INT,"
                           "fuel_price FLOAT,"
                           "fuel_l FLOAT,"
                           "r_price FLOAT)")
            messagebox.showinfo("Database created", "Database created successfully")
            # Creating new text file for database name
            database_name = open('database_name.txt', 'w')
            database_name.write(year)
            database_name.close()
            # Updating system created date on sys_info table
            cursor.execute("CREATE TABLE sys_info("
                           "dte VARCHAR(255),"
                           "diesel_u FLOAT,"
                           "petrol_u FLOAT,"
                           "pws VARCHAR(255))")
            cursor.execute(F"INSERT INTO sys_info VALUES('{str(dte)}', '{diesel_p.get()}', '{petrol_p.get()}', 'nmceng@2022')")
            data_base.commit()
            new_data_win.quit()
            new_data_win.destroy()
        except():
            messagebox.showerror("Error", "Database name already exists")
    else:
        messagebox.showerror("Invalid data", "Year entered is invalid or out of range")


def new_database(master):
    global new_data_win, diesel_p, petrol_p
    if __name__ == '__main__':
        new_data_win = Tk()
    else:
        new_data_win = Toplevel(master)

    new_data_win.geometry('400x250')
    new_data_win.title('New database')
    new_data_win.iconbitmap('img/dataicon.ico')
    new_data_win.resizable(width=False, height=False)
    # Heading
    Label(new_data_win, text='Create New Database', font=('Arial', 23, 'bold'), fg='#595C5B').pack(pady=10, padx=5, anchor=W)

    # Frame for database name and entry box
    data_name_f = Frame(new_data_win)
    data_name_f.pack()

    Label(data_name_f, text='OR_SYSTEM_', font=('Arial', 20, 'bold'), fg='#8C8C8C').pack(side=LEFT, pady=10)
    year_e = Entry(data_name_f, width=5, font=('Arial', 20, 'bold'))
    year_e.pack(side=LEFT)

    price_f = Frame(new_data_win)
    price_f.pack()
    Label(price_f, text='Petrol price :', font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=W)
    Label(price_f, text='Diesel price :', font=('Arial', 12, 'bold')).grid(row=0, column=1, sticky=W, padx=10)

    petrol_p = Entry(price_f, font=('Arial', 12, 'bold'), width=6)
    petrol_p.grid(row=1, column=0, sticky=W, padx=5)
    diesel_p = Entry(price_f, font=('Arial', 12, 'bold'), width=6)
    diesel_p.grid(row=1, column=1, sticky=W, padx=20)


    button_img = ImageTk.PhotoImage(Image.open('img/signin.png').resize((100, 40), Image.Resampling.LANCZOS))
    Button(new_data_win, image=button_img, borderwidth=0, command=lambda: data_entry(year_e)).pack(pady=20)


    mainloop()


if __name__ == '__main__':
    new_database(None)
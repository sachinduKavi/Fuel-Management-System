from tkinter import *
import mysql.connector
from PIL import ImageTk, Image
from databaseGen import new_database
from record_form_01 import new_record_start
from vehicle_registery import register_start
from change_fuel import change_fuel_start
import webbrowser
from delete_update import delete_update_start
from graphView import graph_view
from dataImportExport import *
from adminprivilage import admin_pass
from changePsw import current_psw
from userAccount import user_module


class ORSys:
    def main_screen(self):
        self.data_base.commit()
        # Main menu frame
        self.main_frame = Frame(self.root)
        self.main_frame.pack(expand=True, fill=BOTH)

        # Top main bar
        bar_f = Frame(self.main_frame, height=140, bg='#1DBCA5')
        bar_f.pack(fill=X)

        # NMC image
        self.nmc_img = ImageTk.PhotoImage(Image.open("img/nmcLogo.png").resize((140, 140), Image.Resampling.LANCZOS))
        Label(bar_f, image=self.nmc_img, bg='#1DBCA5').pack(side=LEFT, padx=(20, 0))

        # Name frame and system name
        name_frame = Frame(bar_f, bg='#1DBCA5')
        name_frame.pack(side=LEFT, padx=(8, 0))
        Label(name_frame, text='NMC\nNEGOMBO MUNICIPAL COUNCIL', font=('Arial', 17, 'bold'), justify=LEFT, fg='white', bg='#1DBCA5').pack(pady=(10, 0))
        Label(name_frame, text=self.system_name.replace("_", " "), font=('Arial', 15, 'bold'), justify=LEFT, fg='white', bg='#1DBCA5').pack(anchor=W, pady=8)

        # Created date label
        Label(bar_f, text=f'Created on :\n            {self.dte}', font=('Arial', 12, 'bold'), fg='white', bg='#045648', padx=10, borderwidth=2, relief=SOLID).pack(side=RIGHT, anchor=SE, padx=20, pady=10)

        # Content frame for data and data manipulation
        content_f = Frame(self.main_frame)
        content_f.pack(fill=BOTH, expand=True)

        # For database current state and other stuff
        overView_frame = Frame(content_f, width=500, bg='#E0E0E0', relief=RAISED, borderwidth=1)
        overView_frame.pack(side=LEFT, padx=10, fill=Y, pady=10)
        # Overview heading
        over_head = Frame(overView_frame, bg='#004946', width=500, height=50)
        over_head.pack()
        Label(over_head, text='Overview', font=('Arial', 23, 'bold'), fg='white', bg='#004946').place(x=10, y=5)

        # Extracting diesel and petrol prices from database
        self.cursor.execute("SELECT diesel_u, petrol_u FROM sys_info")
        self.diesel_p, self.petrol_p = self.cursor.fetchall()[0]
        Label(overView_frame, text=f'Petrol unit Price : Rs. {self.petrol_p:.2f}', font=('Arial', 20, 'bold'), fg='white', bg='#4E594E').pack(pady=(10, 0), anchor=W, padx=10, fill=X)
        Label(overView_frame, text=f'Diesel unit Price : Rs. {self.diesel_p:.2f}', font=('Arial', 20, 'bold'), fg='white', bg='#4E594E').pack(pady=(10, 0), anchor=W, padx=10, fill=X)

        # Month frame
        month_frame = Frame(overView_frame, bg='#E0E0E0')
        month_frame.pack(fill=X, pady=5)
        # Button Image
        left_img = ImageTk.PhotoImage(Image.open("img/left.png").resize((30, 30), Image.Resampling.LANCZOS))
        right_img = ImageTk.PhotoImage(Image.open("img/right.png").resize((30, 30), Image.Resampling.LANCZOS))
        # Fetching system date month
        self.c_month_num = int(str(date.today())[5:7])-1
        self.c_month = self.month_list[self.c_month_num]

        Button(month_frame, image=right_img, borderwidth=0, command=lambda: self.change_month('-'), bg='#E0E0E0', activebackground='#E0E0E0').pack(side=LEFT, padx=(100, 0))
        middle_frame = Frame(month_frame, bg='#E0E0E0')
        middle_frame.pack(side=LEFT, expand=True, fill=X)
        self.month_label = Label(middle_frame, text=self.c_month, font=('Arial', 15, 'bold'), bg='#E0E0E0')
        self.month_label.pack()
        Button(month_frame, image=left_img, borderwidth=0, command=lambda: self.change_month('+'), bg='#E0E0E0', activebackground='#E0E0E0').pack(side=RIGHT, padx=(0, 100))

        # Extract total number of petrol and diesel from the database
        used_fuel_frame = Frame(overView_frame, bg='#E0E0E0')
        used_fuel_frame.pack(fill=X, pady=5)

        self.fuel_frame = Frame(used_fuel_frame, height=10, bg='#E0E0E0')
        self.fuel_frame.pack()

        self.fuel_update()

        # Change fuel price jump link
        Button(overView_frame, text='Change Fuel Prices', font=('Arial', 12, 'bold'), fg='red', command=lambda: self.call_back_refresh('change_fuel_start')).pack(pady=10, anchor=E, padx=10)

        # For data manipulation and apply changes to the database
        manu_frame = Frame(content_f, bg='#E0E0E0', relief=RAISED, borderwidth=1)
        manu_frame.pack(side=RIGHT, padx=(0, 10), fill=Y, pady=10, expand=True)

        # Heading frame in manipulation frame
        menu_head_f = Frame(manu_frame, bg='#004946', width=370, height=50)
        menu_head_f.pack()
        Label(menu_head_f, text='Manipulation', font=('Arial', 23, 'bold'), fg='white', bg='#004946').place(x=10, y=5)
        # Jump links frames
        jump_frame = Frame(manu_frame, bg='#E0E0E0')
        jump_frame.pack(pady=5)
        # Jump buttons
        Button(jump_frame, text='Add Records', font=('Ariaal', 12, 'bold'), bg='#039191', fg='white', width=25, command=lambda: self.call_back_refresh("add_record")).pack(pady=4)
        Button(jump_frame, text='Display Records', font=('Ariaal', 12, 'bold'), bg='#039191', fg='white', width=25,  command=lambda: self.display_or(self.system_name)).pack(pady=4)
        Button(jump_frame, text='Delete / Update', font=('Ariaal', 12, 'bold'), bg='#039191', fg='white', width=25, command=lambda: admin_pass(self.system_name, self.root, 'Delete Update')).pack(pady=4)
        Button(jump_frame, text='Vehicle Registry', font=('Ariaal', 12, 'bold'), bg='#039191', fg='white', width=25, command=lambda: register_start(self.root, self.system_name, self.user)).pack(pady=4)
        Button(jump_frame, text='Summary Sheet', font=('Ariaal', 12, 'bold'), bg='#039191', fg='white', width=25,  command=lambda: self.summary(self.system_name)).pack(pady=4)
        Button(jump_frame, text='Graph View', font=('Ariaal', 12, 'bold'), bg='#039191', fg='white', width=25,  command=lambda: graph_view(self.system_name)).pack(pady=4)

        mainloop()

    def fuel_update(self):
        # Removing previous content from the frame
        self.fuel_frame.forget()
        for child in self.fuel_frame.winfo_children():
            child.destroy()
        self.fuel_frame.pack()

        # Fetching petrol values from database
        self.cursor.execute(f"SELECT reg_num  FROM vehicle_register WHERE fuel_type='Petrol'")
        petrol_veh = self.cursor.fetchall()
        total_petrol = 0
        for reg_num in petrol_veh:
            reg_num = reg_num[0]
            self.cursor.execute(f"SELECT fuel_l FROM oil_records WHERE vehicle_reg='{reg_num}' AND month='{self.c_month}'")
            liters = self.cursor.fetchall()
            for value in liters:
                total_petrol += value[0]

        # Fetching diesel values from database
        self.cursor.execute("SELECT reg_num FROM vehicle_register WHERE fuel_type='Diesel'")
        diesel_veh = self.cursor.fetchall()
        total_diesel = 0
        for reg_num in diesel_veh:
            reg_num = reg_num[0]
            self.cursor.execute(F"SELECT fuel_l FROM oil_records WHERE vehicle_reg='{reg_num}' AND month='{self.c_month}'")
            liters = self.cursor.fetchall()
            for value in liters:
                total_diesel += value[0]

        # Creating petrol and diesel labels
        petrol_frame = Frame(self.fuel_frame, width=100, bg='#03827A', height=100)
        petrol_frame.pack(side=LEFT, padx=10)
        Label(petrol_frame, text='Petrol :', font=('Arial', 10, 'bold'), bg='#03827A', fg='white').pack(anchor=W, padx=5)
        Label(petrol_frame, text=f"{total_petrol:.1f}", font=('Arial', 18, 'bold'), bg='#03827A', fg='white', width=6).pack(padx=8)

        diesel_frame = Frame(self.fuel_frame, width=100, bg='#03827A', height=100)
        diesel_frame.pack(side=RIGHT, padx=10)
        Label(diesel_frame, text='Diesel :', font=('Arial', 10, 'bold'), bg='#03827A', fg='white').pack(anchor=W, padx=5)
        Label(diesel_frame, text=f"{total_diesel:.1f}", font=('Arial', 18, 'bold'), bg='#03827A', fg='white', width=6).pack(padx=8)

    def change_month(self, sign):
        if sign == '+' and self.c_month_num < 11:
            self.c_month_num += 1
        elif sign == '-' and self.c_month_num > 0:
            self.c_month_num -= 1
        self.c_month = self.month_list[self.c_month_num]
        self.month_label.config(text=self.c_month)
        self.fuel_update()

    def database_change(self):
        try:
            system_name = open('database_name.txt', 'r').readlines()[0]
        except FileNotFoundError:
            messagebox.showerror("File Error", "No database found\n Please create new database to continue")
            new_database(self.root)
            system_name = str(open('database_name.txt', 'r').readlines()[0])
        print('Database name', system_name)
        # Database initialize
        self.data_base = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database=system_name
        )
        self.cursor = self.data_base.cursor()
        self.cursor.execute("SELECT dte FROM sys_info")
        dte = self.cursor.fetchall()[0][0]
        print(dte)
        return system_name, dte

    def __init__(self, user):
        self.month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.root = Tk()
        self.root.geometry('900x500')
        self.root.title(f'OR_System - User : {user}')
        self.root.iconbitmap('img/fuel2.ico')
        self.root.resizable(width=False, height=False)
        self.user = user
        # Database init
        self.system_name, self.dte = self.database_change()

        # Main menus
        self.main_menu = Menu(self.root)

        # Action sub menu
        self.action = Menu(self.main_menu, tearoff=0)
        self.action.add_command(label='New Database', command=lambda: new_database(self.root))

        self.main_menu.add_cascade(label='Action', menu=self.action)

        # Fetching database names from mysql database
        self.cursor.execute("SHOW DATABASES")
        all_databases = self.cursor.fetchall()
        or_database = []
        for database in all_databases:
            if database[0][:-4] == 'or_system_':
                or_database.append(database[0])
        print("Or databases", or_database)

        # sub menu in change database
        change_db_menu = Menu(self.action, tearoff=0)
        for value in or_database:
            value = value.upper()
            change_db_menu.add_command(label=value.upper(), command=lambda s=value: self.database_shift(s))
        self.action.add_cascade(label='Change Database', menu=change_db_menu)
        # Refresh command
        self.action.add_command(label="Refresh", command=self.refresh_main_screen)

        self.privilege = Menu(self.main_menu, tearoff=0)
        # Import Export menus
        self.privilege.add_command(label="Import", command=lambda: self.call_back_refresh("data_import"))
        self.privilege.add_command(label="Export", command=lambda: data_export(self.system_name, self.user))
        self.privilege.add_command(label="System Log", command=lambda: admin_pass(self.system_name, self.root, 'Sys_log'))
        self.privilege.add_command(label='Change Password', command=lambda: current_psw(self.system_name, self.root))

        self.main_menu.add_cascade(label='Admin', menu=self.privilege)

        self.root.config(menu=self.main_menu)

        # Main screen
        self.main_screen()

        self.root.mainloop()

    def refresh_main_screen(self):
        self.main_frame.forget()
        for child in self.main_frame.winfo_children():
            child.destroy()
        self.main_screen()

    # Auto refresh main screen after call back
    def call_back_refresh(self, function_name):
        if function_name == 'change_fuel_start':
            change_fuel_start(self.root, self.system_name, self.user)
        elif function_name == 'add_record':
            new_record_start(self.root, self.system_name, self.petrol_p, self.diesel_p, self.user)
        elif function_name == 'data_import':
            data_import(self.system_name, self.user)

        self.refresh_main_screen()

    def summary(self, sys_name):
        sys_year = sys_name[-4:]
        try:
            os.startfile(f"Summary Sheet-{sys_year}")
        except FileNotFoundError:
            messagebox.showerror("Missing File", f"Change File name as: Summary Sheet-{sys_year}")
            webbrowser.open_new(f"http://localhost/OR_SYS_{sys_year}/summary_report.php")

    def display_or(self, sys_name):
        sys_year = sys_name[-4:]
        try:
            os.startfile(f"OR Display-{sys_year}")
        except FileNotFoundError:
            messagebox.showerror("Missing File", f"Change File name as: OR Display-{sys_year}")
            webbrowser.open_new(f"http://localhost/OR_SYS_{sys_year}/orDisplay.php")

    def database_shift(self, sys_name):
        # Change system to sys_name
        self.system_name = sys_name
        database_name_file = open("database_name.txt", 'w')
        database_name_file.write(sys_name)
        database_name_file.close()
        self.database_change()
        self.refresh_main_screen()


if __name__ == "__main__":
    user_module()
    c_user = open('current_user.txt', 'r').read()
    ORSys(c_user)

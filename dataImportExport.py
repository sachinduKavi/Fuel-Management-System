from tkinter import messagebox
from tkinter import filedialog
from database_connection import db_connection
from datetime import date
import os


def data_export(sys_name, user):
    ans = messagebox.askyesno("Export", "Do you want to export the database ?")
    if ans:
        log_file = open('sys_log.txt', 'a')
        log_file.write(f'{date.today()} >> Data File exported by {user}\n')
        log_file.close()
        data_base, cursor = db_connection(sys_name)
        cur_date = date.today()

        # Fetching data from database > oil_records
        cursor.execute("SELECT * FROM oil_records")
        oil_records = cursor.fetchall()

        # Get desktop path and write file
        path_f = os.path.expanduser('~\Desktop')
        path_f = path_f + "/BackUp"
        if not os.path.exists(path_f):
            os.makedirs(path_f)
        exp_file = open(f"{path_f}/Backup-{cur_date}.txt", 'w', encoding='utf-8')

        for record in oil_records:
            for data in record:
                exp_file.write(f"{data}#")
            exp_file.write('\n')

        # Vehicle registration backup
        cursor.execute("SELECT * FROM vehicle_register")
        vehicle_regs = cursor.fetchall()
        exp_file.write("$#Vehicle Registration\n")
        for record in vehicle_regs:
            for data in record:
                exp_file.write(f"{data}#")
            exp_file.write("\n")
        messagebox.showinfo("Success", "The Export completed")
        exp_file.close()


veh_reg = False


def data_import(sys_name, user):
    ans = messagebox.askyesno("Confirm", "Do you want to continue the Import,\n This will Rewrite your data")
    if ans:
        log_file = open('sys_log.txt', 'a')
        log_file.write(f'{date.today()} >> Data Imported, all previous data has been destroyed by {user}\n')
        log_file.close()
        try:
            global veh_reg
            data_base, cursor = db_connection(sys_name)
            data_base.commit()
            file_location = filedialog.askopenfilename()
            file = open(file_location, 'r', encoding='utf-8')
            file_data = file.readlines()
            file.close()
            # Deleting data from the database
            cursor.execute("DELETE FROM oil_records")
            cursor.execute("DELETE FROM vehicle_register")
            for record in file_data:
                record = record[:-1].split("#")[:-1]
                if record[0] == '$':
                    veh_reg = True
                    continue
                print(record)
                if veh_reg:
                    cursor.execute(f"INSERT INTO vehicle_register(reg_num, type, current_page, fuel_type) VALUES('{record[0].upper()}', '{record[1]}', '{record[2]}', '{record[3]}')")
                else:
                    cursor.execute(f"INSERT INTO oil_records VALUES("
                                   f"'{record[0]}',"
                                   f"'{record[1]}',"
                                   f"'{record[2]}',"
                                   f"'{record[3].upper()}',"
                                   f"'{record[4]}',"
                                   f"'{record[5]}',"
                                   f"'{record[6]}',"
                                   f"'{record[7]}')")
            data_base.commit()
            messagebox.showinfo("Success", "Data Imported Successfully")
            veh_reg = True
        except:
            messagebox.showerror("Error", "No File selected or invalid filetype")


if __name__ == "__main__":
    data_export("OR_SYSTEM_2022")

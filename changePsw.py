from tkinter import *
from database_connection import db_connection
from PIL import ImageTk, Image
from tkinter import messagebox
from datetime import date


def current_psw(sys_name, master):
    global c_psw
    if __name__ == "__main__":
        c_psw = Tk()
    else:
        c_psw = Toplevel(master)
        c_psw.geometry(f"+{master.winfo_rootx()+200}+{master.winfo_rooty()+200}")
    c_psw.resizable(width=False, height=False)
    c_psw.geometry("400x210")
    c_psw.title('Change password')
    c_psw.iconbitmap("img/setting.ico")

    Label(c_psw, text='Change password', font=('Arial', 20, 'bold')).pack(pady=10)

    entry_frame = Frame(c_psw)
    entry_frame.pack()
    global  error_label
    # Old password
    Label(entry_frame, text='Old password', font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=E, padx=4)
    old_psw = Entry(entry_frame, font=('Arial', 12, 'bold'), show='\u2022', width=13)
    old_psw.grid(row=0, column=1)
    # New password 01 and 02
    Label(entry_frame, text='New password', font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky=E, padx=4)
    new_psw = Entry(entry_frame, font=('Arial', 12, 'bold'), show='\u2022', width=13)
    new_psw.grid(row=1, column=1, pady=4)

    Label(entry_frame, text='Confirm New password', font=('Arial', 12, 'bold')).grid(row=2, column=0, sticky=E, padx=4)
    new_psw_02 = Entry(entry_frame, font=('Arial', 12, 'bold'), show='\u2022', width=13)
    new_psw_02.grid(row=2, column=1)

    # Invalid error message
    error_label = Label(c_psw, font=('Arial', 10, 'bold'), fg='red')
    error_label.pack()
    c_psw.bind('<Return>', lambda event: change_psw(old_psw, new_psw, new_psw_02, sys_name))

    # Submit button
    sub_img = ImageTk.PhotoImage(Image.open('img/submit.png').resize((70, 40), Image.Resampling.LANCZOS))
    Button(c_psw, image=sub_img, borderwidth=0, command=lambda: change_psw(old_psw, new_psw, new_psw_02, sys_name)).pack(pady=2)

    c_psw.mainloop()


def change_psw(old_psw_e, new_psw_e, new_psw_02_e, sys_name):
    old_psw, new_psw, new_psw_02 = old_psw_e.get(), new_psw_e.get(), new_psw_02_e.get()
    if new_psw == new_psw_02:
        data_base, cursor = db_connection(sys_name)
        cursor.execute("SELECT pws FROM sys_info")
        current_psw = cursor.fetchall()[0][0]
        if old_psw == current_psw:
            cursor.execute(f"UPDATE sys_info SET pws='{new_psw}'")
            data_base.commit()
            c_psw.destroy()
            c_psw.quit()
            log_file = open('sys_log.txt', 'a')
            log_file.write(f'{date.today()} >> Admin password has been changed\n')
            log_file.close()
            messagebox.showinfo("Success", 'Password changed successfully')
            return
        else:
            error_label.config(text='**Invalid Password')
    else:
        error_label.config(text='**New passwords are mismatching')
    # Removing previous contents
    old_psw_e.delete(0, END)
    new_psw_e.delete(0, END)
    new_psw_02_e.delete(0, END)


if __name__ == "__main__":
    current_psw("OR_SYSTEM_2022", None)
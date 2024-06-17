from tkinter import *
from PIL import Image, ImageTk
from database_connection import db_connection
from delete_update import delete_update_start
from system_log import sys_log


def admin_pass(sys_name, master, window):
    global pass_win
    if __name__ == "__main__":
        pass_win = Tk()
    else:
        pass_win = Toplevel(master)
        pass_win.geometry(f"+{master.winfo_rootx()+200}+{master.winfo_rooty()+200}")
    pass_win.geometry("350x130")
    pass_win.title("Admin Only")
    pass_win.resizable(width=False, height=False)
    pass_win.iconbitmap("img/setting.ico")
    bg_color = '#044F66'
    pass_win.config(bg=bg_color)

    Label(pass_win, text='Admin password', font=('Arial', 20, 'bold'), fg='white', bg=bg_color).pack(pady=10)

    # Frame for entry and submit button
    entry_frame = Frame(pass_win, bg=bg_color)
    entry_frame.pack()

    psw_e = Entry(entry_frame, font=('Arial', 15, 'bold'), show="\u2022", width=13)
    psw_e.pack(side=LEFT)
    sub_img = ImageTk.PhotoImage(Image.open("img/left.png").resize((40, 40), Image.Resampling.LANCZOS))
    Button(entry_frame, image=sub_img, borderwidth=0, bg=bg_color, activebackground=bg_color, command=lambda: verify_psw(sys_name, psw_e, master, window)).pack(side=LEFT, padx=5)
    pass_win.bind('<Return>', lambda event: verify_psw(sys_name, psw_e, master, window))
    # Hidden error message
    global error_l
    error_l = Label(pass_win, fg='red', bg=bg_color, font=('Arial', 10, 'bold'))
    error_l.pack()
    # Binding return key

    pass_win.mainloop()


def verify_psw(sys_name, psw, master, window):
    data_base, cursor = db_connection(sys_name)
    entered_psw = psw.get()
    cursor.execute("SELECT pws from sys_info")
    sys_password = cursor.fetchall()[0][0]
    if sys_password == entered_psw:
        pass_win.quit()
        pass_win.destroy()
        c_user = open('current_user.txt', 'r').read()
        if window == 'Delete Update':
            delete_update_start(master, sys_name, c_user)
        elif window == 'Sys_log':
            sys_log(master)
    else:
        error_l.config(text='**Invalid Password')
        psw.delete(0, END)


if __name__ == "__main__":
    admin_pass("OR_SYSTEM_2022", None)

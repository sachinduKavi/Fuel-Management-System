from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox


def user_module():
    global bg_color, user_win
    user_win = Tk()
    user_win.geometry('450x200')
    user_win.title('User Login')
    user_win.iconbitmap('img/setting.ico')
    user_win.resizable(width=False, height=False)

    bg_color = '#1F558F'
    user_win.config(bg=bg_color)

    # User profile
    user_img = ImageTk.PhotoImage(Image.open('img/loggin.png').resize((150, 150), Image.Resampling.LANCZOS))
    Label(user_win, image=user_img, relief=SUNKEN, borderwidth=5, bg=bg_color).pack(side=LEFT, padx=10)
    login_frame = Frame(user_win, bg=bg_color)
    login_frame.pack(side=LEFT)
    Label(login_frame, text='User Name :', font=('Arial', 10, 'bold'), fg='white', bg=bg_color).pack(anchor=W)
    user_name = Entry(login_frame, font=('Arial', 18, 'bold'))
    user_name.pack()
    Label(login_frame, text='Password :', font=('Arial', 10, 'bold'), fg='white', bg=bg_color).pack(anchor=W, pady=(10, 0))
    user_psw = Entry(login_frame, font=('Arial', 18, 'bold'), show='\u2022')
    user_psw.pack()

    sub_img = ImageTk.PhotoImage(Image.open('img/submit.png').resize((70, 35), Image.Resampling.LANCZOS))
    Button(login_frame, image=sub_img, borderwidth=0, bg=bg_color, activebackground=bg_color, command=lambda: check_username(user_name, user_psw)).pack(pady=10, anchor=W)
    user_win.bind('<Return>', lambda event: check_username(user_name, user_psw))

    # Menus
    main_menu = Menu(user_win)
    new_menu = Menu(main_menu, tearoff=0)
    new_menu.add_command(label='New User', command=lambda: add_user(user_win))
    main_menu.add_cascade(menu=new_menu, label='New')
    user_win.configure(menu=main_menu)

    user_win.mainloop()


def check_username(user, psw):
    user_list = open('user_list.txt', 'r').readlines()
    user_credentials = {}
    # Appending file data to dictionary
    for record in user_list:
        record = record[:-1]
        user_file, psw_file = record.split('#')
        user_credentials[user_file] = psw_file
    # Checking weather user name and password exists
    if user.get() not in user_credentials:
        messagebox.showerror('User Error', 'User not found', parent=user_win)
        user.delete(0, END)
        psw.delete(0, END)
    elif user_credentials[user.get()] == psw.get():
        print('password correct')
        c_user_file = open('current_user.txt', 'w')
        c_user_file.write(user.get())
        c_user_file.close()
        user_win.quit()
        user_win.destroy()
    else:
        messagebox.showerror('Password Error', 'User password mismatch', parent=user_win)
        psw.delete(0, END)


def add_user(master):
    global add_user_win
    add_user_win = Toplevel(master)
    # add_user_win.resizable(width=False, height=False)
    add_user_win.geometry("400x200")
    add_user_win.geometry(f'+{master.winfo_rootx()}+{master.winfo_rooty()}')
    add_user_win.title('New user')
    add_user_win.iconbitmap("img/setting.ico")

    Label(add_user_win, text='New user', font=('Arial', 20, 'bold')).pack(pady=10)

    entry_frame = Frame(add_user_win)
    entry_frame.pack()
    global error_label
    Label(entry_frame, text='User Name', font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=E, padx=4)
    new_user_name = Entry(entry_frame, font=('Arial', 12, 'bold'), width=18)
    new_user_name.grid(row=0, column=1, pady=4)
    # New password 01 and 02
    Label(entry_frame, text='password', font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky=E, padx=4)
    new_psw = Entry(entry_frame, font=('Arial', 12, 'bold'), show='\u2022', width=18)
    new_psw.grid(row=1, column=1, pady=4)

    Label(entry_frame, text='Confirm password', font=('Arial', 12, 'bold')).grid(row=2, column=0, sticky=E, padx=4)
    new_psw_02 = Entry(entry_frame, font=('Arial', 12, 'bold'), show='\u2022', width=18)
    new_psw_02.grid(row=2, column=1)

    # Submit button
    sub_img = ImageTk.PhotoImage(Image.open('img/submit.png').resize((70, 35), Image.Resampling.LANCZOS))
    Button(add_user_win, image=sub_img, borderwidth=0, command=lambda: new_user_submit(new_user_name, new_psw, new_psw_02)).pack(pady=10)

    mainloop()


# Submitting new user data to a file
def new_user_submit(user, pass_01, pass_02):
    psw_01 = pass_01.get()
    if psw_01 == pass_02.get():
        user_list = open('user_list.txt', 'a')
        user_list.write(f'{user.get().strip()}#{psw_01}\n')
        add_user_win.quit()
        add_user_win.destroy()
        messagebox.showinfo("Success", 'New user created successfully', parent=user_win)
    else:
        messagebox.showerror('Typo Error', 'Passwords mismatch', parent=add_user_win)
        pass_01.delete(0, END)
        pass_02.delete(0, END)


if __name__ == '__main__':
    user_module()

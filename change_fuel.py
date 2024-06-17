from tkinter import *
from database_connection import db_connection
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import date


def change_fuel_start(master, sys_name, user):
    global fuel_pop_win, user_name
    user_name = user
    if __name__ == '__main__':
        fuel_pop_win = Tk()
    else:
        fuel_pop_win = Toplevel(master)
        fuel_pop_win.geometry(f"+{master.winfo_rootx()+200}+{master.winfo_rooty()+200}")
    fuel_pop_win.geometry("400x200")
    fuel_pop_win.title('Change fuel prices')
    fuel_pop_win.protocol("WM_DELETE_WINDOW", on_closing)
    fuel_pop_win.iconbitmap("img/setting.ico")
    fuel_pop_win.resizable(width=False, height=False)

    Label(fuel_pop_win, text='Change fuel prices', font=('Arial', 20, 'bold'), fg='#706D6D').pack(anchor=W, pady=(10, 2), padx=5)
    Label(fuel_pop_win, text='**Changing oil prices only affect for future records in the database ', font=('Arial', 8, 'bold'), fg='red').pack(anchor=W, pady=(0, 5), padx=5)

    # Entry frame and entries
    entry_frame = Frame(fuel_pop_win)
    entry_frame.pack()

    Label(entry_frame, text='Petrol Price', font=("Arial", 15, 'bold')).grid(row=0, column=0, padx=10)
    Label(entry_frame, text='Diesel Price', font=("Arial", 15, 'bold')).grid(row=0, column=1, padx=10)

    p_price = Entry(entry_frame, font=("Arial", 15, 'bold'), width=6)
    p_price.grid(row=1, column=0)
    d_price = Entry(entry_frame, font=("Arial", 15, 'bold'), width=6)
    d_price.grid(row=1, column=1)

    # Update button
    update_img = ImageTk.PhotoImage(Image.open("img/update.png").resize((120, 50), Image.Resampling.LANCZOS))
    Button(fuel_pop_win, image=update_img, borderwidth=0, command=lambda: update_fuel(sys_name, p_price, d_price)).pack(pady=5)

    fuel_pop_win.mainloop()


def update_fuel(sys_name, p_price, d_price):
    ans = messagebox.askyesno("Confirmation", "Are yo sure you want continue with update values ?", parent=fuel_pop_win)
    if ans:
        log_file = open('sys_log.txt', 'a')
        log_file.write(f'{date.today()} >> Fuel prices has been updated by {user_name}\n')
        log_file.close()
        data_base, cursor = db_connection(sys_name)
        cursor.execute(f"UPDATE sys_info SET diesel_u='{float(d_price.get())}', petrol_u='{float(p_price.get())}'")
        data_base.commit()
        messagebox.showinfo("Successful", "Values updated successfully", parent=fuel_pop_win)
        fuel_pop_win.quit()
        fuel_pop_win.destroy()


def on_closing():
    fuel_pop_win.quit()
    fuel_pop_win.destroy()


if __name__ == '__main__':
    change_fuel_start(None, 'OR_SYSTEM_2022')

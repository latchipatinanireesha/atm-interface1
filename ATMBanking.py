import tkinter as tk
from tkinter.font import BOLD
from PIL import ImageTk, Image
import sqlite3
from imgop import *
from pages import *

#Main App
class App(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('ATMBankingv0.5')
        self.geometry("720x720+0+0")
        self.resizable(False,False)
        self.app_data = {"name": tk.StringVar(), "pin": tk.StringVar(), "balance": tk.StringVar()}
        self.container = tk.Frame(self)
        self.container.pack(side = "top", fill = "both", expand = True)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)
        self.favicon = ImageTk.PhotoImage(Image.open("img/favicon.png"))
        self.iconphoto(False,self.favicon)
        self.frames = {}
        self.frames["LoginPage"] = LoginPage(parent=self.container, controller=self)
        self.frames["MainPage"] = MainPage(parent=self.container, controller=self)
        self.frames["MainPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["LoginPage"].grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def add_page(self):
        self.frames["BalancePage"] = BalancePage(parent = self.container, controller = self, valuename = self.app_data['name'].get())
        self.frames["BalancePage"].grid(row = 0, column = 0, sticky = "nsew")
        self.frames["DepositPage"] = DepositPage(parent = self.container, controller = self, valuename = self.app_data['name'].get())
        self.frames["DepositPage"].grid(row = 0, column = 0, sticky = "nsew")
        self.frames["TransferPage"] = TransferPage(parent = self.container, controller = self, valuename = self.app_data['name'].get(), userpin = self.app_data['pin'].get(), userbalance = self.app_data['balance'])
        self.frames["TransferPage"].grid(row = 0, column = 0, sticky = "nsew")
        self.frames["WithdrawPage"] = WithdrawPage(parent = self.container, controller = self, valuename = self.app_data['name'].get())
        self.frames["WithdrawPage"].grid(row = 0, column = 0, sticky = "nsew")
        self.frames["ChangePINPage"] = ChangePINPage(parent = self.container, controller = self, valuename = self.app_data['name'].get(), userpin = self.app_data['pin'].get())
        self.frames["ChangePINPage"].grid(row = 0, column = 0, sticky = "nsew")

    def del_page(self, done = False):
        self.frames["BalancePage"].destroy()
        if done == True:
            self.frames["DepositPage"].destroy()
            self.frames["TransferPage"].destroy()
            self.frames["WithdrawPage"].destroy()
            self.frames["ChangePINPage"].destroy()

    def bal_page(self):
        self.frames["BalancePage"] = BalancePage(parent = self.container, controller = self, valuename = self.app_data['name'].get())
        self.frames["BalancePage"].grid(row = 0, column = 0, sticky = "nsew")

#LoginPage
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        login_form = tk.Frame(self,width = 720, height = 640, bg = '#004d4d')
        login_form.pack(fill = "both", expand = True)
        please_text = tk.Label(login_form, text = "Please enter your login details", bg = "#004d4d", fg = "#b37700", font = ('Verdana', 12, BOLD))
        please_text.pack(pady = (80,10))
        fullname_label = tk.Label(login_form, text = "Full Name:", bg = "#004d4d", fg = "#b37700", font = ('Verdana', 15, BOLD))
        fullname_label.pack(pady = (100,5))
        self.name_entry = tk.Entry(login_form, textvariable = self.controller.app_data['name'], width = 20, font = ('Verdana', 12, BOLD), bd = 1)
        self.name_entry.pack()
        pin_label = tk.Label(login_form, text = "PIN:", bg = "#004d4d", fg = "#b37700", font = ('Verdana', 15 , BOLD))
        pin_label.pack(pady = (40,5))
        self.pin_entry = tk.Entry(login_form, textvariable = self.controller.app_data['pin'],show = "*", width = 20, font = ('Verdana', 12, BOLD), bd = 1)
        self.pin_entry.pack()
        self.button_login = tk.Button(login_form, cursor = 'hand2', text = "LOGIN", width = 10, height = 3, font = ('Helvetica', 12, BOLD), command = lambda:self.check_login(self.name_entry.get(), self.pin_entry.get()),bg = "#004d4d", fg = '#b37700')
        self.button_login.pack(pady = (40,5))
        self.controller.bind('<Return>', (lambda event: self.check_login(self.name_entry.get(), self.pin_entry.get())))
        bottom_frame = tk.Frame(self, width = 720, height = 30, bg = "#004d4d")
        bottom_frame.pack(fill = 'both')
        bottom_text = tk.Label(bottom_frame, text = "ATMBanking v0.5", bg = "#004d4d", fg = "#a6a6a6", font = ('Verdana', 6, BOLD))
        bottom_text.pack( side = tk.RIGHT)
        global pinwrong
        pinwrong = 0

    def check_login(self, name, id,):
        connection = sqlite3.connect('data/costumers.db')
        cursor = connection.cursor()
        costumers_name = []
        pins = []
        balances = []
        vname = False
        global pinwrong
        for costumer in cursor.execute('select fullname from costumers'):
            costumers_name.append(costumer)
        for pin in cursor.execute('select pin from costumers'):
            pins.append(pin)
        for balance in cursor.execute('select balance from costumers'):
            balances.append(balance)
        for costumer in costumers_name:
            if costumer[0].lower() == name.lower():
                pin_id = costumers_name.index(costumer)
                vname = True
                if pins[pin_id][0] == int(id):
                    self.controller.app_data['balance'] = balances[pin_id][0]
                    self.controller.add_page()
                    self.controller.unbind('<Return>')
                    self.controller.show_frame('MainPage')
                    self.name_entry.delete(0, END)
                    self.pin_entry.delete(0, END)
                else:
                    if pinwrong == 3:
                        wrongpins = tk.Label(self, text = "You enter 3 attemps, app close!", font = ('Helvetica', 12, BOLD), bg = "#004d4d", fg = "darkred")
                        wrongpins.pack(fill = 'both')
                        wrongpins.after(1000, lambda:wrongpins.pack_forget())
                        messagebox.showerror('App Closing..', 'You have 3 attemps, your app close!')
                        self.controller.destroy()
                    else:
                        wrong_pin = tk.Label(self, text = "Your PIN is wrong!", font = ('Helvetica', 12, BOLD), bg = "#004d4d", fg = "darkred")
                        wrong_pin.pack(fill = 'both')
                        wrong_pin.after(1000, lambda:wrong_pin.pack_forget())
                        pinwrong += 1
        if vname == False:
            wrong_name = tk.Label(self, text = "Your details is wrong!", font = ('Helvetica', 12, BOLD), bg = "#004d4d", fg = "darkred")
            wrong_name.pack(fill = 'both')
            wrong_name.after(1000, lambda:wrong_name.pack_forget())
#MainPage
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        main_frame = tk.Frame(self, bg = "#004d4d")
        main_frame.pack(fill = "both", expand = True)
        text_frame = tk.Frame(main_frame, bg = "#004d4d")
        top_text = tk.Label(text_frame, text = "Please choose a option bellow:", bg = "#004d4d", fg = "white", font = ('Verdana', 16, BOLD))
        top_text.pack(pady = 30)
        text_frame.pack(fill = 'x')
        balance_img = BImage()
        buttons_frame = tk.Frame(main_frame, bg = "#004d4d")
        balance_btn = tk.Button(buttons_frame, text = 'BALANCE', image = balance_img, compound = tk.LEFT, bg = "#0e5c5c", font = ('Bebas NEUE', 20), width = 250, height = 90, cursor = 'hand2', command = lambda:[controller.show_frame('BalancePage')])
        balance_btn.image = balance_img
        balance_btn.grid(row = 0, column = 0, sticky = tk.W, padx = 10, pady = (60,40))
        deposit_img = DImage()
        deposit_btn = tk.Button(buttons_frame, text = "DEPOSIT", font = ('Bebas NEUE', 20), image = deposit_img, compound = tk.LEFT, width = 250, height = 90, cursor = 'hand2', command = lambda:controller.show_frame('DepositPage'))
        deposit_btn.image = deposit_img
        deposit_btn.grid(row = 1, column = 0, sticky = tk.W, padx = 10, pady = 40)
        withdraw_img = WImage()
        withdraw_btn = tk.Button(buttons_frame, text = "WITHDRAW", image = withdraw_img, compound = tk.LEFT, font = ('Bebas NEUE', 20), width = 250, height = 90, cursor = 'hand2', command = lambda:controller.show_frame('WithdrawPage'))
        withdraw_btn.image = withdraw_img
        withdraw_btn.grid(row = 2, column = 0, sticky = tk.W, padx = 10, pady = 40)
        transfer_img = TImage()
        transfer_btn = tk.Button(buttons_frame, text = "TRANSFER", image = transfer_img, compound = tk.LEFT, font = ('Bebas NEUE', 20), width = 250, height = 90, cursor = 'hand2', command = lambda:controller.show_frame('TransferPage'))
        transfer_btn.image = transfer_img
        transfer_btn.grid(row = 0, column = 1, sticky = tk.E, padx = 10, pady = (60,40))
        changepin_img = CPImage()
        changepin_btn = tk.Button(buttons_frame, text = "CHANEGE PIN", image = changepin_img, compound = tk.LEFT, font = ('Bebas NEUE', 20), width = 250, height = 90, cursor = 'hand2', command = lambda:controller.show_frame('ChangePINPage'))
        changepin_btn.image = changepin_img
        changepin_btn.grid(row = 1, column = 1, sticky = tk.E, padx = 10, pady = 40)
        exit_img = EImage()
        exit_btn = tk.Button(buttons_frame, text = "EXIT", image = exit_img, compound = tk.LEFT, font = ('Bebas NEUE', 20), width = 250, height = 90, cursor = 'hand2', command = lambda:controller.destroy())
        exit_btn.image = exit_img
        exit_btn.grid(row = 2, column = 1, sticky = tk.E, padx = 10, pady = 40)
        version_text = tk.Label(buttons_frame, text = "ATMBanking v0.5", bg = "#004d4d", fg = "#a6a6a6", font = ('Verdana', 6, BOLD))
        version_text.grid(row = 3, column = 1, sticky = tk.SE, pady= (60,0))
        buttons_frame.pack(fill = 'both')
        buttons_frame.grid_columnconfigure(0, weight = 1)
        buttons_frame.grid_columnconfigure(1, weight = 1)
        buttons_frame.grid_rowconfigure(3, weight = 1)

if __name__ == "__main__":
    app = App()
    app.mainloop()
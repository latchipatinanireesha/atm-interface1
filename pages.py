import tkinter as tk
import sqlite3
from tkinter import END, messagebox
from tkinter.font import BOLD
from PIL import ImageTk, Image
from imgop import *

class BalancePage(tk.Frame):
    def __init__(self, parent, controller, valuename):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        bank_img = BAImage()
        main_frame = tk.Frame(self, bg = "#004d4d")
        main_frame.pack(fill = "both", expand = True)
        logo_frame = tk.Frame(main_frame, bg = "#004d4d")
        bank_logo = tk.Label(logo_frame, image = bank_img, bg = "#004d4d")
        bank_logo.pack(fill = 'both', expand = True, side = tk.LEFT)
        bank_logo.image = bank_img
        logo_frame.pack(fill = 'x', pady = (20,10))
        name = valuename
        balance = check_balance(name)
        first_frame = tk.Frame(main_frame, bg = "#004d4d")
        acc_text = tk.Label(first_frame, font = ('Bebas Neue', 35), bg = "#004d4d", fg = "black", text = f'Dear {name}, your current balance is:')
        acc_text.pack(pady = (30,15))
        first_frame.pack(fill = 'x')
        balance_frame = tk.Frame(main_frame, bg = "#004d4d")
        balance_text = tk.Label(balance_frame, font = ('Bebas Neue', 30), bg = '#086c6c', fg = 'black', text = f'{balance}$', )
        balance_text.pack(pady = 20,ipadx = 50, ipady = 25)
        balance_frame.pack(fill = 'x')
        second_frame = tk.Frame(main_frame, bg = "#004d4d")
        con_text = tk.Label(second_frame, font = ('bebas neue', 35), bg = "#004d4d", fg = "black", text = 'Do you want to make another transaction?')
        con_text.pack()
        second_frame.pack(fill = 'x', pady = (40, 0))
        buttons_frame = tk.Frame(main_frame, bg = "#004d4d")
        btn_continue = tk.Button(buttons_frame, width = 22, height = 2, text = 'CONTINUE', font = ('bebas neue', 20), bg = "#0b3939", fg = 'black', command = lambda:self.controller.show_frame('MainPage'))
        btn_continue.grid(row = 0, column = 0, sticky = tk.W, padx = 20)
        btn_exit = tk.Button(buttons_frame, width = 22, height = 2, text = 'EXIT', font = ('bebas neue', 20), bg = "#0b3939", fg = 'black', command = lambda:controller.destroy())
        btn_exit.grid(row = 0, column = 1, sticky = tk.E, padx = 20)
        version_text = tk.Label(buttons_frame, text = "ATMBanking v0.5", bg = "#004d4d", fg = "#a6a6a6", font = ('Verdana', 6, BOLD))
        version_text.grid(row = 3, column = 1, sticky = tk.SE, pady= (17,0))
        buttons_frame.pack(fill = 'both', pady = (40,0))
        buttons_frame.grid_columnconfigure(0, weight = 1)
        buttons_frame.grid_columnconfigure(1, weight = 1)


class DepositPage(tk.Frame):
    def __init__(self, parent, controller, valuename):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        main_frame = tk.Frame(self, bg = "#004d4d")
        main_frame.pack(fill = 'both', expand = True)
        logo_frame = tk.Frame(main_frame, bg = '#004d4d')
        bank_img = BAImage()
        bank_logo = tk.Label(logo_frame, image = bank_img, bg = "#004d4d")
        bank_logo.pack(fill = 'both', expand = True, side = tk.LEFT)
        bank_logo.image = bank_img
        logo_frame.pack(fill = 'x', pady = (20,10))
        text_frame = tk.Frame(main_frame, bg = "#004d4d")
        up_text = tk.Label(text_frame, font = ('Bebas Neue', 35), bg = "#004d4d", fg = "black", text= "Enter below the amount you want to deposit:")
        up_text.pack()
        text_frame.pack(fill = 'x', pady = (50,10))
        dep_frame = tk.Frame(main_frame, bg = "#004d4d")
        self.dep_entry = tk.Entry(dep_frame, width = 20, bg = "#086c6c", fg = "black", font = ('Bebas Neue', 40), bd = 5, justify = tk.CENTER)
        self.dep_entry.pack()
        dep_frame.pack(fill = "x", pady = (60, 60))
        buttons_frame = tk.Frame(main_frame, bg ="#004d4d")
        btn_continue = tk.Button(buttons_frame, width = 22, height = 2, text = 'DEPOSIT', font = ('bebas neue', 20), bg = "#0b3939", fg = 'black', command = lambda:self.check_deposit(self.dep_entry.get(), valuename))
        btn_continue.grid(row = 0, column = 0, sticky = tk.W, padx = 20)
        btn_exit = tk.Button(buttons_frame, width = 22, height = 2, text = 'EXIT', font = ('bebas neue', 20), bg = "#0b3939", fg = 'black', command = lambda:controller.destroy())
        btn_exit.grid(row = 0, column = 1, sticky = tk.E, padx = 20)
        version_text = tk.Label(buttons_frame, text = "ATMBanking v0.5", bg = "#004d4d", fg = "#a6a6a6", font = ('Verdana', 6, BOLD))
        version_text.grid(row = 3, column = 1, sticky = tk.SE, pady= (21,0))
        buttons_frame.pack(fill = 'both', pady = (70,0))
        buttons_frame.grid_columnconfigure(0, weight = 1)
        buttons_frame.grid_columnconfigure(1, weight = 1)
    
    def check_deposit(self, amount, valname):
        if amount.isdigit() != 0:
            if int(len(amount)) <= 4 and int(len(amount)) >= 2:
                balance = check_balance(valname)
                balance += int(amount) 
                connection = sqlite3.connect('data/costumers.db')
                cursor = connection.cursor()
                update_balance = """Update costumers set balance=? where fullname=?"""
                data = (balance, valname)
                cursor.execute(update_balance,data)
                connection.commit()
                cursor.close()
                
                if messagebox.askyesno('Deposit Succes!', 'The deposit was successful!\nWant to make another deposit?'):
                    self.dep_entry.delete(0, END)
                    self.controller.del_page(done = True)
                    self.controller.show_frame('LoginPage')
                else:
                    self.controller.destroy()    
            else:
                messagebox.showerror('Error amount!', "You entered the wrong amount! You can deposit between $10 and $9999.")
        else:
            messagebox.showerror('Error amount!', "You entered the wrong amount! You can deposit between $10 and $9999.")

class WithdrawPage(tk.Frame):
    def __init__(self, parent, controller, valuename):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        main_frame = tk.Frame(self, bg = "#004d4d")
        main_frame.pack(fill = 'both', expand = True)
        logo_frame = tk.Frame(main_frame, bg = '#004d4d')
        bank_img = BAImage()
        bank_logo = tk.Label(logo_frame, image = bank_img, bg = "#004d4d")
        bank_logo.pack(fill = 'both', expand = True, side = tk.LEFT)
        bank_logo.image = bank_img
        logo_frame.pack(fill = 'x', pady = (20,10))
        text_frame = tk.Frame(main_frame, bg = "#004d4d")
        up_text = tk.Label(text_frame, font = ('Bebas Neue', 28), bg = "#004d4d", fg = "black", text= "Please enter below the amount you want to withdraw:")
        up_text.pack()
        text_frame.pack(fill = 'x', pady = (50,10))
        width_frame = tk.Frame(main_frame, bg = "#004d4d")
        self.width_entry = tk.Entry(width_frame, width = 20, bg = "#086c6c", fg = "black", font = ('Bebas Neue', 40), bd = 5, justify = tk.CENTER)
        self.width_entry.pack()
        width_frame.pack(fill = "x", pady = (60, 60))
        buttons_frame = tk.Frame(main_frame, bg ="#004d4d")
        btn_continue = tk.Button(buttons_frame, width = 22, height = 2, text = 'WITHDRAW', font = ('bebas neue', 20), bg = "#0b3939", fg = 'black', command = lambda:self.check_withdraw(self.width_entry.get(),valuename))
        btn_continue.grid(row = 0, column = 0, sticky = tk.W, padx = 20)
        btn_exit = tk.Button(buttons_frame, width = 22, height = 2, text = 'EXIT', font = ('bebas neue', 20), bg = "#0b3939", fg = 'black', command = lambda:controller.destroy())
        btn_exit.grid(row = 0, column = 1, sticky = tk.E, padx = 20)
        version_text = tk.Label(buttons_frame, text = "ATMBanking v0.5", bg = "#004d4d", fg = "#a6a6a6", font = ('Verdana', 6, BOLD))
        version_text.grid(row = 3, column = 1, sticky = tk.SE, pady= (35,0))
        buttons_frame.pack(fill = 'both', pady = (70,0))
        buttons_frame.grid_columnconfigure(0, weight = 1)
        buttons_frame.grid_columnconfigure(1, weight = 1)
    
    def check_withdraw(self, amount, valuename):
        balance = check_balance(valuename)
        if int(amount) > 10:
            if int(amount) > balance:
                messagebox.showerror('Error amount!', "You don't have the amount requested!")
            else:
                balance -= int(amount) + (2/100) * int(amount)
                connection = sqlite3.connect('data/costumers.db')
                cursor = connection.cursor()
                update_balance = """Update costumers set balance=? where fullname=?"""
                data = (balance, valuename)
                cursor.execute(update_balance,data)
                connection.commit()
                cursor.close()
                if messagebox.askyesno('Withdraw Succes!', "Want to make another transaction?"):
                    self.width_entry.delete(0, END)
                    self.controller.del_page(done = True)
                    self.controller.show_frame('LoginPage')
                else:
                    self.controller.destroy()
        else:
            messagebox.showerror('Error amount!', "You entered the wrong amount! You can deposit between $10 and $9999.")


class TransferPage(tk.Frame):
    def __init__(self, parent, controller, valuename, userpin, userbalance):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        main_frame = tk.Frame(self, bg = "#004d4d")
        main_frame.pack(fill = 'both', expand = True)
        logo_frame = tk.Frame(main_frame, bg = '#004d4d')
        bank_img = BAImage()
        bank_logo = tk.Label(logo_frame, image = bank_img, bg = "#004d4d")
        bank_logo.pack(fill = 'both', expand = True, side = tk.LEFT)
        bank_logo.image = bank_img
        logo_frame.pack(fill = 'x', pady = (20,10))
        withdraw_frame = tk.Frame(main_frame, bg = "#004d4d")
        tranto_text = tk.Label(withdraw_frame, text = "Transfer to:", font = ('Bebas neue', 25), bg = "#004d4d", fg = "black")
        tranto_text.grid(row = 0, column = 0, sticky = "W", padx = (20,5))
        self.tranto_entry = tk.Entry(withdraw_frame, bg = "#086c6c", fg = "black", font = ('bebas Neue', 20), bd = 4, width = 15)
        self.tranto_entry.grid(row = 0, column = 1, sticky = "W", pady = 20)
        money_text = tk.Label(withdraw_frame, text = "MONEY:", font = ('Bebas neue', 25), bg = "#004d4d", fg = "black")
        money_text.grid(row = 1, column = 0, sticky = "W", padx = (20,5))
        self.money_entry = tk.Entry(withdraw_frame, bg = "#086c6c", fg = "black", font = ('bebas Neue', 20), bd = 4, width = 15)
        self.money_entry.grid(row = 1, column = 1, sticky = "W", pady = 20)
        confirm_text = tk.Label(withdraw_frame, text = "confirm pin:", font = ('Bebas neue', 25), bg = "#004d4d", fg = "black")
        confirm_text.grid(row = 3, column = 0, sticky = "W", padx = (20,5))
        self.confirm_entry = tk.Entry(withdraw_frame, bg = "#086c6c", show = "*", fg = "black", font = ('bebas Neue', 20), bd = 4, width = 15)
        self.confirm_entry.grid(row = 3, column = 1, sticky = "W", pady = 20)
        withdraw_frame.pack(fill = 'x', pady = (40,0))
        buttons_frame = tk.Frame(main_frame, bg ="#004d4d")
        btn_continue = tk.Button(buttons_frame, width = 22, height = 2, text = 'TRANSFER', font = ('bebas neue', 20), bg = "#0b3939", fg = 'black', command = lambda:self.check_transfer(self.tranto_entry.get(), self.money_entry.get(), userbalance, self.confirm_entry.get(), userpin, valuename))
        btn_continue.grid(row = 0, column = 0, sticky = tk.W, padx = 20)
        btn_exit = tk.Button(buttons_frame, width = 22, height = 2, text = 'EXIT', font = ('bebas neue', 20), bg = "#0b3939", fg = 'black', command = lambda:controller.destroy())
        btn_exit.grid(row = 0, column = 1, sticky = tk.E, padx = 20)
        version_text = tk.Label(buttons_frame, text = "ATMBanking v0.5", bg = "#004d4d", fg = "#a6a6a6", font = ('Verdana', 6, BOLD))
        version_text.grid(row = 3, column = 1, sticky = tk.SE, pady= (55,0))
        buttons_frame.pack(fill = 'both', pady = (70,0))
        buttons_frame.grid_columnconfigure(0, weight = 1)
        buttons_frame.grid_columnconfigure(1, weight = 1)
    
    def check_transfer(self, toname, tomoney, balance, checkpin, userpin, valuename):
        connection = sqlite3.connect('data/costumers.db')
        cursor = connection.cursor()
        costumers_name = []
        balances = []
        testvar = False
        for costumer in cursor.execute('select fullname from costumers'):
            costumers_name.append(costumer)
        for balanc in cursor.execute('select balance from costumers'):
            balances.append(balanc)
        for costumer in costumers_name:
            if costumer[0].lower() == toname.lower():
                snickname = costumer[0]
                testvar = True
                if snickname == valuename:
                    messagebox.showerror('Transfer To Error', 'Error! You try to transfer to same account where you are logged.')
                else:
                    balance_id = costumers_name.index(costumer)
                    if int(tomoney) <= balance and int(tomoney) > 10:
                        if checkpin == userpin:
                            newbalanceto = int(tomoney) + balances[balance_id][0]
                            newbalanceus = balance - int(tomoney) 
                            newbalanceus -= (2/100) * int(tomoney)
                            sql_updated = """UPDATE costumers SET balance = ? WHERE fullname = ?"""
                            data = (newbalanceto, snickname)
                            cursor.execute(sql_updated, data)
                            connection.commit()
                            sql_updated = """UPDATE costumers SET balance = ? WHERE fullname = ?"""
                            data = (newbalanceus, valuename)
                            cursor.execute(sql_updated, data)
                            connection.commit()
                            cursor.close()
                            messagebox.showinfo('Transfer Succes', 'Your transfer succes!')
                            self.confirm_entry.delete(0, END)
                            self.tranto_entry.delete(0, END)
                            self.money_entry.delete(0, END)
                            self.controller.del_page(done = True)
                            self.controller.show_frame('LoginPage')
                        else:
                            messagebox.showerror('PIN Error', 'You enter a wrong pin, try again!')
                    else:
                        messagebox.showerror('Money Error', 'No money to transfer!')
        if testvar == False:
            messagebox.showerror('Nickname Wrong', 'You try to transfer to a account dosent exist')


class ChangePINPage(tk.Frame):
    def __init__(self, parent, controller, valuename, userpin):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        main_frame = tk.Frame(self, bg = "#004d4d")
        main_frame.pack(fill = 'both', expand = True)
        logo_frame = tk.Frame(main_frame, bg = '#004d4d')
        bank_img = BAImage()
        bank_logo = tk.Label(logo_frame, image = bank_img, bg = "#004d4d")
        bank_logo.pack(fill = 'both', expand = True, side = tk.LEFT)
        bank_logo.image = bank_img
        logo_frame.pack(fill = 'x', pady = (20,10))
        pin_frame = tk.Frame(main_frame, bg = "#004d4d")
        actualpin_text = tk.Label(pin_frame, text = "Actual PIN:", font = ('Bebas neue', 25), bg = "#004d4d", fg = "black")
        actualpin_text.grid(row = 0, column = 0, sticky = "W", padx = (20,5))
        self.actualpin_entry = tk.Entry(pin_frame, bg = "#086c6c", fg = "black", font = ('bebas Neue', 20), bd = 4, width = 15)
        self.actualpin_entry.grid(row = 0, column = 1, sticky = "W", pady = 30)
        newpin_text = tk.Label(pin_frame, text = "New PIN:", font = ('Bebas neue', 25), bg = "#004d4d", fg = "black")
        newpin_text.grid(row = 1, column = 0, sticky = "W", padx = (20,5))
        self.newpin_entry = tk.Entry(pin_frame, bg = "#086c6c", fg = "black", font = ('bebas Neue', 20), bd = 4, width = 15)
        self.newpin_entry.grid(row = 1, column = 1, sticky = "W", pady = 30)
        pin_frame.pack(fill = 'x', pady = (70,0))
        buttons_frame = tk.Frame(main_frame, bg ="#004d4d")
        btn_continue = tk.Button(buttons_frame, width = 22, height = 2, text = 'CHANGE', font = ('bebas neue', 20), bg = "#0b3939", fg = 'black', command = lambda:self.check_pin(int(self.actualpin_entry.get()),self.newpin_entry.get(), valuename, userpin))
        btn_continue.grid(row = 0, column = 0, sticky = tk.W, padx = 20)
        btn_exit = tk.Button(buttons_frame, width = 22, height = 2, text = 'EXIT', font = ('bebas neue', 20), bg = "#0b3939", fg = 'black', command = lambda:controller.destroy())
        btn_exit.grid(row = 0, column = 1, sticky = tk.E, padx = 20)
        version_text = tk.Label(buttons_frame, text = "ATMBanking v0.5", bg = "#004d4d", fg = "#a6a6a6", font = ('Verdana', 6, BOLD))
        version_text.grid(row = 3, column = 1, sticky = tk.SE, pady= (55,0))
        buttons_frame.pack(fill = 'both', pady = (80,0))
        buttons_frame.grid_columnconfigure(0, weight = 1)
        buttons_frame.grid_columnconfigure(1, weight = 1)

    def check_pin(self, actualpin, newpin, valuename, userpin):

                if actualpin == int(userpin):
                    if len(newpin) == 4:
                        if int(newpin) != int(userpin):
                            connection = sqlite3.connect('data/costumers.db')
                            cursor = connection.cursor()
                            update_balance = """Update costumers set pin=? where fullname=?"""
                            data = (newpin, valuename)
                            cursor.execute(update_balance,data)
                            connection.commit()
                            cursor.close()
                            messagebox.showinfo('Your PIN', 'Your PIN has been updated')
                            self.controller.del_page(done = True)
                            self.controller.show_frame("LoginPage")
                        else:
                            messagebox.showerror('PIN Error', 'You entered the same pin from the past.')
                    
                    else:
                        messagebox.showerror('PIN Error','The PIN must have 4 characters, nothing less or more!')
                else:
                    messagebox.showerror('PIN Error', 'The current PIN does not match the one on this name.')
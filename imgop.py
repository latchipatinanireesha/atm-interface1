from PIL import ImageTk, Image
import tkinter as tk
import sqlite3
def BImage():
    #Balance Logo
    bl_logo = Image.open('img/balance.png')
    bl_logo = bl_logo.resize((25,25), Image.Resampling.LANCZOS)
    balance_img = ImageTk.PhotoImage(bl_logo)
    return balance_img
def DImage():
    #Deposit Logo
    dep_logo = Image.open('img/deposit.png')
    dep_logo = dep_logo.resize((25,25), Image.Resampling.LANCZOS)
    deposit_img = ImageTk.PhotoImage(dep_logo)
    return deposit_img
def WImage():
     #Withdraw Logo
    wi_logo = Image.open('img/withdraw.png')
    wi_logo = wi_logo.resize((25,25), Image.Resampling.LANCZOS)
    withdraw_img = ImageTk.PhotoImage(wi_logo)
    return withdraw_img
def TImage():
    #Transfer Logo
    tf_logo = Image.open('img/transfer.png')
    tf_logo = tf_logo.resize((25,25), Image.Resampling.LANCZOS)
    transfer_img = ImageTk.PhotoImage(tf_logo)
    return transfer_img
def CPImage():
    #ChangePIN Logo
    cp_logo = Image.open('img/pin.png')
    cp_logo = cp_logo.resize((25,25), Image.Resampling.LANCZOS)
    changepin_img = ImageTk.PhotoImage(cp_logo)
    return changepin_img
def EImage():
    #Exit Logo
    ex_logo = Image.open('img/exit.png')
    ex_logo = ex_logo.resize((25,25), Image.Resampling.LANCZOS)
    exit_img = ImageTk.PhotoImage(ex_logo)
    return exit_img
def BAImage():
    #Bank Logo
    bn_logo = Image.open('img/mainlogo.png')
    bn_logo = bn_logo.resize((230,170), Image.Resampling.LANCZOS)
    bank_img = ImageTk.PhotoImage(bn_logo)
    return bank_img
def check_balance(name):
    connection = sqlite3.connect('data/costumers.db')
    cursor = connection.cursor()
    costumers_name = []
    balances = []
    pins = []
    for costumer in cursor.execute('select fullname from costumers'):
        costumers_name.append(costumer)
    for balance in cursor.execute('select balance from costumers'):
        balances.append(balance)
    for costumer in costumers_name:
         if costumer[0] == name:
            balance_id = costumers_name.index(costumer)
            actualbalance = balances[balance_id]
            return actualbalance[0]

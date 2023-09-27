import os
import smtplib
import email.message
import re
import shutil
import time
import ctypes
import win32security
import ntsecuritycon
from tkinter import *
from tkinter import ttk
from validate_email_address import validate_email
from observer import Inicio, Pid
import sys
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def abrir_interface_backup():
    interface_backup = Toplevel(root)
    interface_backup.title('Backup')
    
    botao_backup = Button(interface_backup, text='Fazer Backup', command=realizar_backup)
    botao_backup.pack()

root = Tk()
root.title('Binóculo - scythe')
root.iconbitmap('~\\Documents\\scythe\\scythe.ico')
root.geometry("950x650")
bg = PhotoImage(file='~\\Documents\\scythe\\Challenge.png')
root.resizable(0, 0)
label1 = Label(root, image=bg)
label1.place(x=0, y=0)
root.config(background='black')

def increment(*args):
    for i in range(100):
        p1["value"] = i+1
        root.update()
        time.sleep(0.01)

p1 = ttk.Progressbar(root, length=400, cursor='spider',
                     mode="determinate",
                     orient=HORIZONTAL)
p1.pack()
p1.place(x=270, y=320)

is_on = True

def button_mode():
    global is_on
    
    if is_on:
        on_.config(image=on)
        is_on = False
    else:
        on_.config(image=off)
        is_on = True
        
        shutil.rmtree("C:\!TrapFolder")
        shutil.rmtree("C:\lTrapFolder")
        shutil.rmtree("C:\zTrapFolder")
        print("Armadilhas retiradas com sucesso")
        
        Pid()

on = PhotoImage(file='~\Documents\\scythe\\on.png')
off = PhotoImage(file='~\Documents\\scythe\\off.png')

def comandos():
    button_mode()
    increment()
    Inicio()

# Função para definir permissões de leitura apenas
def set_permissions(path):
    dacl = win32security.ACL()
    sid = win32security.ConvertStringSidToSid("S-1-5-32-545")  # SID para o grupo "Usuários"
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntsecuritycon.FILE_GENERIC_READ, sid)
    sid = win32security.ConvertStringSidToSid("S-1-5-32-544")  # SID para o grupo "Administradores"
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntsecuritycon.FILE_GENERIC_READ, sid)
    sd = win32security.SECURITY_DESCRIPTOR()
    sd.SetSecurityDescriptorDacl(1, dacl, 0)
    win32security.SetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION, sd)

# Função para definir permissões de gravação temporariamente
def set_permissions_temp_write(path):
    dacl = win32security.ACL()
    sid = win32security.ConvertStringSidToSid("S-1-5-32-545")  # SID para o grupo "Usuários"
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntsecuritycon.FILE_GENERIC_WRITE, sid)
    sid = win32security.ConvertStringSidToSid("S-1-5-32-544")  # SID para o grupo "Administradores"
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ntsecuritycon.FILE_GENERIC_WRITE, sid)
    sd = win32security.SECURITY_DESCRIPTOR()
    sd.SetSecurityDescriptorDacl(1, dacl, 0)
    win32security.SetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION, sd)

# Verifica se o programa está sendo executado como administrador
if is_admin():
    botao_abrir_backup = Button(root, text='Backup', command=abrir_interface_backup)
    botao_abrir_backup.place(x=700, y=30)

    on_ = Button(root, image=off, bd=0, command=comandos, background='black')
    on_.place(x=800, y=30)

    def realizar_backup():
        pasta_1 = input("Digite o caminho da pasta desejada: ")
        documentos = os.path.expanduser("~/Documents")
        pasta_2 = os.path.join(documentos, "backup")
        
        if not os.path.exists(pasta_2):
            os.makedirs(pasta_2)
        set_permissions_temp_write(pasta_2)  # Defina permissões de gravação temporariamente

        origem = pasta_1
        destino = pasta_2
        arquivos = os.listdir(origem)

        for arquivo in arquivos:
            caminho_origem = os.path.join(origem, arquivo)
            caminho_destino = os.path.join(destino, arquivo)
            shutil.copy2(caminho_origem, caminho_destino)

        # Restaure as permissões para leitura apenas após a cópia
        set_permissions(pasta_2)

        itens_na_pasta_backup = os.scandir(pasta_2)
        num_itens = sum(1 for item in itens_na_pasta_backup)

        print(f'Backup salvo na pasta ({pasta_2}) com sucesso!')
        print(f'Em {time.strftime("%d-%m-%Y %H:%M:%S")}')
        print(f'Número de itens no backup: {num_itens}')

        while True:
            email_destino = input("Digite seu endereço de email: ")
            if validate_email(email_destino):
                break
            else:
                print("Por favor, insira um endereço de email válido.")

        def enviar_email():  
            corpo_email = """
            <p>Olá, somos a Scythe Control.</p>
            <p>Seu Backup foi concluído com sucesso!</p>
            <p>Número de itens no backup: {num_itens}</p>
            <p>Atenciosamente, Sythe Control Co.</p>
            """.format(num_itens=num_itens)

            msg = email.message.Message()
            msg['Subject'] = "Relatório do Backup"
            msg['From'] = 'scythecntrl@gmail.com'
            msg['To'] = email_destino
            password = 'xngkjdjaeagtxgdf' 
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(corpo_email)

            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            
            server.login(msg['From'], password)
            server.sendmail(msg['From'], msg['To'].split(','), msg.as_string().encode('utf-8'))
            server.quit()

            print('Relatório enviado para o email:', email_destino)
        enviar_email()

    root.mainloop()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

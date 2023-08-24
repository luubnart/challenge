# Importação de bibliotecas
from tkinter import *
from tkinter import ttk
import time
import shutil
from observer import Inicio, Pid

#---------------------------------------------------------

# Configurações da interface gráfica
root = Tk()
root.title('Binóculo - scythe')

root.iconbitmap('scythe.ico')  # Ícone da janela
root.geometry("950x650")  # Dimensões da janela
bg = PhotoImage(file='Challenge.png')  # Imagem de fundo
root.resizable(0, 0)  # Impede o redimensionamento da janela
label1 = Label(root, image=bg)
label1.place(x=0, y=0)
root.config(background='black')  # Cor de fundo

# Barra de progresso
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

# Botão Ligado/Desligado
is_on = True

label = Label()

def button_mode():
    global is_on
    
    # Altera entre ligado e desligado
    if is_on:
        on_.config(image=on)
        label.config(bg="black", fg="black")
        is_on = False
    else:
        on_.config(image=off)
        label.config(bg="black", fg="black")
        is_on = True
        
        # Remove os Trapfolders quando desligado
        shutil.rmtree("C:\!TrapFolder")
        shutil.rmtree("C:\lTrapFolder")
        shutil.rmtree("C:\zTrapFolder")
        print("Trap Folders Deletados!!")
        
        # Fecha a janela da interface
        Pid()

# Imagens dos botões
on = PhotoImage(file="on.png")
off = PhotoImage(file="off.png")

def comandos():
    button_mode()
    increment()
    Inicio()

# Cria o botão
on_ = Button(root, image=off, bd=0, command=comandos, background='black')
on_.place(x=800, y=30)

# Inicia a interface
root.mainloop()

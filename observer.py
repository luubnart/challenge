# Importação de bibliotecas
import pathlib
import os
import shutil
import string
import random
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import signal
from tkinter import *
from tkinter import ttk
import time
from win10toast import ToastNotifier
import psutil

#---------------------------------------------------------

# Função para pegar o PID da interface e fechar a janela
def Pid():
    pid = os.getpid()  # Obtém o PID
    os.kill(pid, signal.SIGTERM)  # Fecha a janela

# Função para iniciar o programa
def Inicio():
    # Função para identificar a raiz do sistema
    def RaizIden():
        drive = pathlib.Path.home().drive

        # Identificação da raiz do sistema com base na unidade do usuário
        if drive == 'C:':
            global c, d, e, f
            c = 'C:/'  # Unidade C:
            d = r'C:\!TrapFolder'  # Pasta de armadilha 1
            e = r'C:\lTrapFolder'  # Pasta de armadilha 2
            f = r'C:\zTrapFolder'  # Pasta de armadilha 3
        elif drive == 'E:':
            c = 'E:/'  # Unidade E:
            d = r'C:\!TrapFolder'
            e = r'C:\lTrapFolder'
            f = r'C:\zTrapFolder'
        elif drive == 'D:':
            c = 'D:/'  # Unidade D:
            d = r'C:\!TrapFolder'
            e = r'C:\lTrapFolder'
            f = r'C:\zTrapFolder'
        elif drive == 'F:':
            c = 'F:/'  # Unidade F:
            d = r'C:\!TrapFolder'
            e = r'C:\lTrapFolder'
            f = r'C:\zTrapFolder'
    RaizIden()

    # Nomes das pastas de armadilha
    directory1 = "!TrapFolder" 
    directory2 = 'lTrapFolder'
    directory3 = 'zTrapFolder'

    parent_dir = c  # Diretório principal

    # Função para criar as pastas de armadilha
    def CriandoPastas():
        path1 = os.path.join(parent_dir, directory1)  # Caminho da pasta 1
        path2 = os.path.join(parent_dir, directory2)  # Caminho da pasta 2
        path3 = os.path.join(parent_dir, directory3)  # Caminho da pasta 3

        os.mkdir(path1)  # Cria a pasta 1
        os.mkdir(path2)  # Cria a pasta 2
        os.mkdir(path3)  # Cria a pasta 3

    CriandoPastas()

    # Função para criar arquivos nas pastas de armadilha
    def Arquivos():
        number_of_strings = 5
        length_of_string = 5
        l = 0
        # Criação de arquivos .txt dentro das pastas de armadilha
        for x in range(number_of_strings):
            while l < 5000:
                save_path1 = d
                name_of_file1 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
                completeName1 = os.path.join(save_path1, name_of_file1+".txt")
                file1 = open(completeName1, "w")
                toFile1 = "Armadilha de detecção"
                file1.write(toFile1)
                file1.close()
                l += 1
        m = 0
        for y in range(number_of_strings):
            while m < 5000:
                save_path2 = e
                name_of_file2 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
                completeName2 = os.path.join(save_path2, name_of_file2+".txt")
                file2 = open(completeName2, "w")
                toFile2 = "Armadilha de detecção"
                file2.write(toFile2)
                file2.close()
                m += 1
        n = 0
        for z in range(number_of_strings):
            while n < 5000:
                save_path3 = f
                name_of_file3 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
                completeName3 = os.path.join(save_path3, name_of_file3+".txt")
                file3 = open(completeName3, "w")
                toFile3 = "Armadilha de detecção"
                file3.write(toFile3)
                file3.close()
                n += 1
    Arquivos()

    print("Detector Ligado")

    start = time.time()
    lista = []

    # Função do observador
    def Obervador2():
        class MyEventHandler1(FileSystemEventHandler):
            def on_modified(self, event):
                print(event.src_path, 'Modificado')
                lista.append(event.src_path)
                if len(lista) > 200:
                    stop = time.time()
                    b = start - stop
                    if b < 10:
                        print('Possivel Ransomware Detectado')

                        # Notificação no sistema quando detectar
                        toast = ToastNotifier()
                        toast.show_toast(
                            "Alerta ransomware",
                            "Ransomware Detectado by scythe",
                            duration = 20,
                            icon_path = "scythe.ico",
                            threaded = True,
                        )

                        # Função para encontrar o PID de processos
                        def findProcessIdByName(processName):
                            listOfProcessObjects = []
                            for proc in psutil.process_iter():
                                try:
                                    pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
                                    if processName.lower() in pinfo['name'].lower() :
                                        listOfProcessObjects.append(pinfo)
                                except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
                                    pass
                            return listOfProcessObjects;

                        listOfProcessIds = findProcessIdByName('')  # Encontra PIDs
                        if len(listOfProcessIds) > 0:
                            for elem in listOfProcessIds:
                                processID = elem['pid']
                                os.kill(processID, 9)  # Mata o processo
                                print('Processo foi morto')
                        else :
                            print('Processo NÃO foi morto')
                        observer.stop()

        # Observa as modificações nas pastas
        observer = Observer()
        observer.schedule(MyEventHandler1(), d, recursive=True)
        observer.schedule(MyEventHandler1(), e, recursive=True)
        observer.schedule(MyEventHandler1(), f, recursive=True)
        observer.start()

        try:
            while observer.is_alive():
                observer.join(1)
        except KeyboardInterrupt:
            shutil.rmtree("C:\!TrapFolder")
            shutil.rmtree("C:\lTrapFolder")
            shutil.rmtree("C:\zTrapFolder")
            print("Trap Folders Deletados!!")
            observer.stop()

    Obervador2()

# Inicia o programa
Inicio()

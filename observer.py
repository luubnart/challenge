import os
import shutil
import string
import random
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import signal
from tkinter import *
from tkinter import ttk
from win10toast import ToastNotifier
import psutil
import requests
import hashlib

class Hash():
    def init(self, last_file: str):
        self.malware = False
        self.last_file = last_file

    def generate_hash(self):
        sha256 = hashlib.sha256()
        with open(self.last_file, "rb") as file:
            for chunk in iter(lambda: file.read(4094), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

class API(Hash):
    def init(self, last_file):
        super().init(last_file)
        self.url = "https://mb-api.abuse.ch/api/v1/"
        self.malware_info = {}
        self.database_search()

    def database_search(self):
        errors = ["illegal_hash", "hash_not_found"]
        hash_value = self.generate_hash()
        data = {
            "query": "get_info",
            "hash": hash_value
        }
        response = requests.post(url=self.url, data=data)
        if response.status_code == 200:
            response_data = response.json()
            if response_data["query_status"] not in errors:
                self.malware_info["signature"] = response_data["data"][0]["signature"]
                self.malware_info["sha256"] = response_data["data"][0]["sha256_hash"]
                self.malware_info["locate"] = self.last_file
                self.malware = True
        else:
            self.malware = False

class PublicMalwareDetection(API):
    def init(self, last_file):
        super().init(last_file)
        self.main()

    def main(self):
        if self.malware:
            log_file = "C:\\Users\\scythe\\Documents\\logs.log"
            with open(log_file, "a") as file:
                file.write(f'\nMalware Detected!\n{"-"*20}\nSignature: {self.malware_info["signature"]}\nSHA256: {self.malware_info["sha256"]}\nLocate: {self.malware_info["locate"]}\n{"-"*20}')
            os.remove(self.last_file)

def Pid():
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)

def Inicio():
    def RaizIden():
        drive = os.path.splitdrive(os.path.expanduser("~"))[0]

        if drive == 'C:':
            global c, d, e, f
            c = 'C:/'
            d = r'C:\!Armadilha'
            e = r'C:\lArmadilha'
            f = r'C:\zArmadilha'
        elif drive == 'E:':
            c = 'E:/'
            d = r'C:\!Armadilha'
            e = r'C:\lArmadilha'
            f = r'C:\zArmadilha'
        elif drive == 'D:':
            c = 'D:/'
            d = r'C:\!Armadilha'
            e = r'C:\lArmadilha'
            f = r'C:\zArmadilha'
        elif drive == 'F:':
            c = 'F:/'
            d = r'C:\!Armadilha'
            e = r'C:\lArmadilha'
            f = r'C:\zArmadilha'
    RaizIden()

    directory1 = "!Armadilha"
    directory2 = 'lArmadilha'
    directory3 = 'zArmadilha'

    parent_dir = c

    def CriandoPastas():
        path1 = os.path.join(parent_dir, directory1)
        path2 = os.path.join(parent_dir, directory2)
        path3 = os.path.join(parent_dir, directory3)

        if not os.path.exists(path1):
            os.mkdir(path1)
        if not os.path.exists(path2):
            os.mkdir(path2)
        if not os.path.exists(path3):
            os.mkdir(path3)

    CriandoPastas()

    def Arquivos():
        number_of_strings = 5
        length_of_string = 5
        l = 0

        for x in range(number_of_strings):
            while l < 1000:
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
            while m < 1000:
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
            while n < 1000:
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
    observer = None

    def Obervador2():
        nonlocal observer

        class MyEventHandler1(FileSystemEventHandler):
            def on_modified(self, event):
                print(event.src_path, 'Modificado (RANSOMWARE)')
                lista.append(event.src_path)
                if len(lista) > 200:
                    stop = time.time()
                    b = start - stop
                    if b < 10:
                        print('Ransomware Detectado')

                        toast = ToastNotifier()
                        toast.show_toast(
                            "Alerta ransomware",
                            "Ransomware Detectado by scythe",
                            duration=20,
                            icon_path="scythe.ico",
                            threaded=True,
                        )

                        # Mata os processos suspeitos dentro dos diretórios monitorados
                        for dir_to_check in [d, e, f]:
                            for proc in psutil.process_iter(['pid', 'exe']):
                                try:
                                    process_pid = proc.info['pid']
                                    process_exe = proc.info['exe']
                                    if process_exe and dir_to_check in process_exe:
                                        print(f'Killing process with PID {process_pid}')
                                        os.kill(process_pid, signal.SIGTERM)
                                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                                    pass
                        observer.stop()

        observer = Observer()
        observer.schedule(MyEventHandler1(), d, recursive=True)
        observer.schedule(MyEventHandler1(), e, recursive=True)
        observer.schedule(MyEventHandler1(), f, recursive=True)
        observer.start()

        try:
            while observer.is_alive():
                observer.join(1)
        except KeyboardInterrupt:
            shutil.rmtree(d)
            shutil.rmtree(e)
            shutil.rmtree(f)
            print("Armadilhas retiradas com sucesso")
            observer.stop()

    Obervador2()

if name == "main":
    try:
        Inicio()
    except KeyboardInterrupt:
        print("Programa encerrado pelo usuário")

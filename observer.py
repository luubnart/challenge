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
import time
import win32security
import ntsecuritycon

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

# Caminho do arquivo de texto
caminho_do_arquivo = r"C:\\Users\\koji\\Documents\\scythe\\"

# Defina as permissões de leitura no arquivo
set_permissions(caminho_do_arquivo)

# Agora, você pode usar a função set_permissions_temp_write para dar permissão de gravação temporariamente:
set_permissions_temp_write(caminho_do_arquivo)
# Faça as operações de gravação no arquivo aqui

# Depois que terminar as operações de gravação, remova as permissões de gravação temporariamente
set_permissions(caminho_do_arquivo)


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



                        # Define o limite de consumo de RAM em MB
                        limite_ram_mb = 50

                        # Função para listar e imprimir processos com uso de RAM acima do limite
                        def listar_processos_acima_limite(limite):
                            for processo in psutil.process_iter(attrs=['pid', 'name', 'memory_info']):       
                                try:
                                    info_memoria = processo.info['memory_info']
                                    consumo_ram_mb = info_memoria.rss / (1024 * 1024)  


                                    if consumo_ram_mb > limite:                                      
                                        print(f"Processo que utilizou mais de {limite} MB de RAM:")
                                        print(f"Nome: {processo.info['name']}")
                                        print(f"PID: {processo.info['pid']}")
                                        print(f"Uso de Memória (RSS): {consumo_ram_mb} MB")
                                        print("=" * 40)  # Linha separadora

                                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                                    pass

                        # Lista de processos que não devem ser encerrados
                        processos_permitidos = []

                        # Lê os nomes dos processos permitidos a partir do arquivo
                        with open("processos_permitidos.txt", "r") as arquivo:
                            for linha in arquivo:
                                processo_permitido = linha.strip()  # Remove espaços em branco e quebras de linha
                                processos_permitidos.append(processo_permitido)

                        # Obtém o PID do seu próprio programa
                        meu_pid = os.getpid()

                        # Loop principal
                        while True:
                            # Verifica os processos e imprime os que estão acima do limite de RAM
                            listar_processos_acima_limite(limite_ram_mb)
    
                            # Verifica outros processos e não encerra os processos permitidos
                            for processo in psutil.process_iter(attrs=['pid', 'name']):
                                try:
                                    processo_info = processo.info
                                    pid = processo_info['pid']
                                    nome_processo = processo_info['name']
            
            # Verifica se o processo é permitido e não é o próprio programa
                                    if nome_processo.lower() not in processos_permitidos and pid != meu_pid:
                                        processo_encerrar = psutil.Process(pid)
                                        processo_encerrar.terminate()  # Encerra o processo
                                        print(f"Processo encerrado: {nome_processo} (PID {pid})")
                                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                                    pass

    # Intervalo de verificação (em segundos)
                            time.sleep(15)  # Verifica a cada 15 segundos

                        
                        
                        
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

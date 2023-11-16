from ftplib import FTP
import threading
import os
from colorama import Fore

class UI:
    def __init__(self):
        self.clear_screen()

    def clear_screen(self):
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')

    def print_banner(self):
        print(f"""{Fore.RED}
  █████▒▄▄▄█████▓ ██▓███      ▄████▄   ██░ ██ ▓█████  ▄████▄   ██ ▄█▀▓█████  ██▀███  
▓██   ▒ ▓  ██▒ ▓▒▓██░  ██▒   ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▒████ ░ ▒ ▓██░ ▒░▓██░ ██▓▒   ▒▓█    ▄ ▒██▀▀██░▒███   ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
░▓█▒  ░ ░ ▓██▓ ░ ▒██▄█▓▒ ▒   ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
░▒█░      ▒██▒ ░ ▒██▒ ░  ░   ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
 ▒ ░      ▒ ░░   ▒▓▒░ ░  ░   ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
 ░          ░    ░▒ ░          ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
 ░ ░      ░      ░░          ░         ░  ░░ ░   ░   ░        ░ ░░ ░    ░     ░░   ░ 
                             ░ ░       ░  ░  ░   ░  ░░ ░      ░  ░      ░  ░   ░     
                             ░                       ░                               
            {Fore.LIGHTBLUE_EX}Made by KonaN{Fore.RESET}
            {Fore.LIGHTBLUE_EX}Github: https://github.com/KKonaNN/{Fore.RESET}""")
        
    def print_menu(self):
        print(f"""{Fore.RED}
[1] - Check FTP Connection string (manual input)
[2] - Check FTP Connection file (file.txt)
[3] - Exit
{Fore.RESET}""")
        
    def start(self):
        self.clear_screen()
        self.print_banner()
        self.print_menu()

ui = UI().start()

class FTPChecker:
    def __init__(self, host, user, passwd):
        self.host = host
        self.user = user
        self.passwd = passwd

    def is_connected(self):
        try:
            ftp = FTP(self.host)
            ftp.login(user=self.user, passwd=self.passwd)
            ftp.quit()
            return True
        except Exception as e:
            return False

def check_ftp_connection(ftp_url):
    try:
        host, user, passwd = ftp_url.split(":")

        if not host or not user or not passwd:
            return False
        
        checker = FTPChecker(host, user, passwd)
        if checker.is_connected():
            print(f"{Fore.GREEN}[FTP] - [GOOD]: {host}:{user}:{passwd}" + Fore.RESET)
            g.write(f"{host}:{user}:{passwd}\n")
        else:
            print(f"{Fore.RED}[FTP] - [BAD]: {host}:{user}:{passwd}" + Fore.RESET)
    except:
        pass

if __name__ == '__main__':
    choice = input('Enter your choice: >')

    global g
    g = open(f"ftp_results.txt", "a")

    if choice == '1':
        print(f"{Fore.RED}to exit type: exit{Fore.RESET}")
        while True:
            ftp_url = input('Enter the ftp connection string: >')
            if ftp_url == 'exit':
                break
            check_ftp_connection(ftp_url)
    elif choice == '2':
        name = input('Enter the file name: >')

        with open(name, 'r') as f:
            data  = f.readlines()

        threads = []
        for i in data:
            line = i.rstrip().replace("ftp://", "").replace(" ", ":")
            t = threading.Thread(target=check_ftp_connection, args=(line,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
    else:
        print('Exiting...')
        exit()
    g.close()
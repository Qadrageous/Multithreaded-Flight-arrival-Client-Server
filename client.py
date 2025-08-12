import socket
import time
from prettytable import PrettyTable

def main():
    print("the client is live!")

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as cs: #create a TCP socket 
        serverAdd = ('127.0.0.1', 4999)
        for i in range(3):  # retry connecting to server every 10 seconds till server is alive
            try:
                cs.connect(serverAdd) #connect it with the server (handshake)
                break
            except Exception as e:
                print("Retrying to connect with the server in 5 seconds, please wait!")
                time.sleep(5)
            if i == 2:
                print("No response, exiting...")
                exit(0)

        try:
            
            name = input("Enter your name: ")
            if name == "":
                print("No name entered, exiting...")
                exit(0)
            cs.send(name.encode('utf-8'))
            
            while True:# to keep the code running until the user stop it
            
                menu_table = PrettyTable()
                menu_table.field_names = ["Option", "Menu"]

                menu_table.add_row(["1", "Arrived Flights"])
                menu_table.add_row(["2", "Delayed Flights"])
                menu_table.add_row(["3", "All Flights Coming From A Specific Airport(ICAO)"])
                menu_table.add_row(["4", "Details of a particular flight"])
                menu_table.add_row(["5", "Quit"])

                print(menu_table)
                option = input("Choose Your Option: ")
                print(30 * '=')

                if 1 <= int(option) <= 4:
                
                    cs.send(option.encode('utf-8'))

                    if int(option) == 3:
                        dep_icao = input("Please Enter The Departure ICAO: ")
                        print(30 * '=')
                        cs.send(dep_icao.encode('utf-8'))
                
                    if int(option) == 4:
                        flight_iata = input("Please Enter The Flight IATA: ")
                        print(30 * '=')
                        cs.send(flight_iata.encode('utf-8'))
                    
                    msg = cs.recv(999999)

                    if msg.decode('utf-8') == "ERROR":
                        print("Server encountered an error.")
                        exit(0)
                    else:
                        print(msg.decode('utf-8'))

                elif int(option) == 5:
                    cs.send(option.encode('utf-8'))
                    print('THE CLIENT WILL CLOSE GOODBYE!')
                    exit(0)

                else:
                    print("You Entered A Wrong Number")

        except Exception as e:  # accepts errors for server disconnection while client in alive.
            print("Connection to the server lost." + "\nQuiting...")
            exit(0)
        except KeyboardInterrupt:
            print("\nReceived CTRL + C. \nQuiting... ")
            cs.send("5".encode('utf-8'))
            exit(0)

if __name__ == "__main__":
    main()

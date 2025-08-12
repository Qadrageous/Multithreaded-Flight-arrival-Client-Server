import socket
import time
import customtkinter as ctk



print("the client is live!")



with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as cs:    #create a TCP socket
    serverAdd = ('127.0.0.1', 4999)
    for i in range(3):  #Retry to connect 3 times before exiting
        try:
            cs.connect(serverAdd)  # connect it with the server (handshake)
            break
        except Exception as e:
            print("Retrying to connect with the server in 5 seconds, please wait!")
            time.sleep(5)
        if i == 2:
            print("No response, exiting...")
            exit(0)



    def submit(option, dep_icao, flight_iata):
        nameInput.configure(state="disabled")  #each client can only submit name once
        name = nameInput.get()
        try:
            cs.send(name.encode('utf-8'))

            if option == "1. Arrived Flights":
                #number = "1"
                cs.send("1".encode('utf-8'))

            elif option == "2. Delayed Flights":
                #number = "2"
                cs.send("2".encode('utf-8'))


            elif option == "3. All Flights Coming From A Specific Airport(ICAO)":
                #number = "3"
                cs.send("3".encode('utf-8'))
                cs.send(dep_icao.encode('utf-8'))

            elif option == "4. Details of a particular flight":
                #number = "4"
                cs.send("4".encode('utf-8'))
                cs.send(flight_iata.encode('utf-8'))

            else:
                cs.send("5".encode('utf-8'))
                print("THE CLIENT WILL CLOSE GOODBYE!")
                exit(0)

            msg = cs.recv(999999)
            update_label = lambda: response.configure(text=msg) #show the response in GUI scrolled frame
            update_label()
            #print(msg.decode('utf-8')) >> to show server response on client terminal also

        except Exception as e:  # accepts errors for server disconnection while client in alive.
            print("Connection to the server lost." + "\nQuiting...")
            exit(0)


    #Window theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    #Window size
    root = ctk.CTk()
    root.geometry("1000x800")   #sets gui window size

    #Main frame
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=50, fill="both", expand=True)

    #Output frame
    frame2 = ctk.CTkScrollableFrame(master=root)
    frame2.pack(pady=20, padx=50, fill="both", expand=True)

    #adds title
    Title = ctk.CTkLabel(master=frame, text="Airport Data Retrieval")
    Title.pack(pady=12, padx=10)

    #accepts client name
    nameInput = ctk.CTkEntry(master=frame, placeholder_text="Client Name")
    nameInput.pack(pady=12, padx=10)



    #Dropdown Options menu for client
    optionmenu = ctk.CTkOptionMenu(master=frame, values=["1. Arrived Flights", "2. Delayed Flights", "3. All Flights Coming From A Specific Airport(ICAO)","4. Details of a particular flight", "5. Quit"])
    optionmenu.pack(pady=12, padx=10)
    optionmenu.set("Choose action")

    #Entry for option 3
    dep = ctk.CTkEntry(master=frame, placeholder_text="Departure ICAO")     #takes departure icao code
    dep.pack(pady=12, padx=10)

    #Entry for option 4
    iata = ctk.CTkEntry(master=frame, placeholder_text="FLight IATA")   #takes specific flight iata
    iata.pack(pady=12, padx=10)

    #sends option, departure code, and IATA that has been entered to submit function
    button = ctk.CTkButton(master=frame, text="Submit", command=lambda: submit(optionmenu.get(), dep.get(), iata.get()))
    button.pack(pady=12, padx=10)

    #Additional info
    mustInfo = ctk.CTkLabel(master=frame, text="*For option 3: fill departure icao \n*For option 4: fill flight iata ")
    mustInfo.pack(pady=12, padx=10)

    #Response text
    response = ctk.CTkLabel(master=frame2, text="Response Here:>")
    response.pack(pady=12, padx=10)


    root.mainloop()
import socket
import threading
import time
import requests 
import json
def main():
    def api(params): 

        api_result = requests.get("http://api.aviationstack.com/v1/flights",params)# HTTPS IS NOT ACCESSIBLE IN THE FREE SUBSCRIPTION 

        if api_result.status_code != 200:
            raise Exception("Non-200 response: " + str(api_result.text))

        jData = api_result.json()  

        with open("flights.json", "w") as f: #save the results in a json file for testing 
            json.dump(jData, f, indent=2)
        
    def multi_client(cs):
        cName = cs.recv(1024).decode('utf-8')
        
        if cName == "":
            print("No name entered, closing thread")
            exit(0)
        else:
            print("\nNow we are serving client: " +cName)
    
        while True:
                
            option = cs.recv(1024)
        
            if option.decode('utf-8') =='1': #display all arrived flights 
             try:
                with open("flights.json") as f:
                    flights = json.load(f)
                    output = []
                    for rs in flights["data"]: 
                        if rs["flight_status"] == "landed":
                            x = (
                            "Flight Code (IATA): " + str(rs['flight']['iata'])+
                            "\nDeparture Airport: " + str(rs['departure']['airport'])+
                            "\nArrival Time: " + str(rs['arrival']['actual'])+
                            "\nArrival Terminal: " + str(rs['arrival']['terminal']) +
                            "\nArrival Gate: " + str(rs['arrival']['gate'])+
                            '\n' + 30 * '=')
                            output.append(x)

                    if len(output) == 0:
                        output.append("There Was No Information For That Request"+'\n' + 30 * '=') 

                    message = '\n'.join(output)

                cs.send(message.encode('utf-8'))
                print("\nClient: "+cName+" Has Requested All Arrived flights:(Option-1)\n"
                        "Flight code (IATA), Departure Airport, Arrival Time, Arrival Terminal, Arrival Gate")
             
             except Exception as e:
                    cs.send("ERROR".encode('utf-8'))
                    print("client "+cName+" will be disconnected via encountering an error")
                    cs.close()
                    break

            elif option.decode('utf-8') =='2': # display all delayed flights
             try:
                with open("flights.json") as f:
                    flights = json.load(f)
                    output = []
                    for rs in flights["data"]:
                        if rs["arrival"]['delay'] is not None:
                            x = (
                            "Flight Code (IATA): " + str(rs['flight']['iata'])+
                            "\nDeparture Airport: " + str(rs['departure']['airport'])+
                            "\nOriginal Departure Time: " + str(rs['departure']['actual'])+
                            "\nEstimated Arrival Time: "+ str(rs['arrival']['estimated'])+
                            "\nArrival Terminal: " + str(rs['arrival']['terminal']) +
                            "\nDelayed For: "+ str(rs['arrival']['delay'])+ " minutes"+
                            "\nArrival Gate: " + str(rs['arrival']['gate'])+
                            '\n' + 30 * '=')
                            output.append(x)

                    if len(output) == 0:
                        output.append("There Was No Information For That Request"+'\n' + 30 * '=') 

                    message = '\n'.join(output)

                cs.send(message.encode('utf-8'))
                print("\nClient: "+cName+"Has Requested All Delayed flights:(Option-2)\n"
                        "Flight code (IATA), Departure Airport, Original Departure Time, Estimated Arrival Time, Arrival Terminal, Arrival Delayed Time, Arrival Gate")

             except Exception as e:
                    cs.send("ERROR".encode('utf-8'))
                    print("client "+cName+" will be disconnected via encountering an error")
                    cs.close()
                    break

            elif option.decode('utf-8') =='3': # display all flights from specific airport
                
             dep_icao = cs.recv(1024).decode('utf-8') 

             try:
                with open("flights.json") as f:
                    flights = json.load(f)
                    output = []
                    for rs in flights["data"]:
                        if rs['departure']['icao'] == dep_icao :
                            x = (
                            "Flight Code (IATA): " + str(rs['flight']['iata'])+
                            "\nDeparture Airport: " + str(rs['departure']['airport'])+
                            "\nOriginal Departure Time: " + str(rs['departure']['actual'])+
                            "\nEstimated Arrival Time: "+ str(rs['arrival']['estimated'])+
                            "\nDeparture Gate: " + str(rs['departure']['gate'])+
                            "\nArrival Gate: " + str(rs['arrival']['gate'])+
                            "\nFlight Status: " + str(rs['flight_status'])+
                            '\n' + 30 * '=')
                            output.append(x) 

                    if len(output) == 0:
                        output.append("There Was No Information For That Request"+'\n' + 30 * '=') 

                    message = '\n'.join(output)

                cs.send(message.encode('utf-8'))
                print("\nClient: "+cName+" Has Requested All flights From A Specific Airport Via Airport ICAO :(Option-3) using departure icao: "+ dep_icao+"\n"
                        "Flight code (IATA), Departure Airport, Original Departure Time, Estimated Arrival Time, Departure Gate, Arrival Gate, Flight Status")

             except Exception as e:
                    cs.send("ERROR".encode('utf-8'))
                    print("client "+cName+" will be disconnected via encountering an error")
                    cs.close()
                    break

            elif option.decode('utf-8') =='4': # display details of a specific flight

             flight_iata = cs.recv(1024).decode('utf-8') 
             try:
                with open("flights.json") as f:
                    flights = json.load(f)
                    output = []
                    for rs in flights["data"]:
                        if rs['flight']['iata'] == flight_iata:
                            x = (
                            "Flight Code (IATA): " + str(rs['flight']['iata']) +
                            "\nDeparture Airport: " + str(rs['departure']['airport']) +
                            "\nDeparture Gate: " + str(rs['departure']['gate']) +
                            "\nDeparture Terminal: " + str(rs['departure']['terminal']) +
                            "\nArrival Airport: " + str(rs['arrival']['airport']) +
                            "\nArrival Gate: " + str(rs['arrival']['gate']) +
                            "\nArrival Terminal: " + str(rs['arrival']['terminal']) +
                            "\nFlight Status: " + str(rs['flight_status']) +
                            "\nScheduled Departure Time: " + str(rs['departure']['scheduled']) +
                            "\nScheduled Arrival Time: " + str(rs['arrival']['scheduled']) +
                            '\n' + 30 * '=')
                            output.append(x)

                    if len(output) == 0:
                        output.append("There Was No Information For That Request"+'\n' + 30 * '=') 

                    message = '\n'.join(output)

                cs.send(message.encode('utf-8'))
                print("\nClient: "+cName+" Has Requested All flights From A Specific Airport Via Airport ICAO :(Option-4) using flight iata: "+flight_iata+"\n"
                        "Flight code (IATA), Departure(Airport,Gate,Terminal,Scheduled Time), Arrival(Airport,Gate,Terminal,Scheduled Time), Flight Status")
        
             except Exception as e:
                    cs.send("ERROR".encode('utf-8'))
                    print("client "+cName+" will be disconnected for encountering an error")
                    cs.close()
                    break

            elif option.decode('utf-8') =='5': #disconnect
                    print("\nclient " +cName +" is disconnecting")
                    cs.close()
                    break
            

        print("\nend of the thread of client : " +cName)

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as ss: #create a TCP socket 
    
        ss.bind(("127.0.0.1", 4999))

        print("The server is live!" )

        arr_icao = input("Enter the Airport Code: ")
        params = {
                    'access_key': '122cdd7860a56bf077bbe86b2e570970',
                    'arr_icao': arr_icao,
                    'limit':"100"
                }
        
        for i in range(3):
            try:
                print("Setting up the API..." )
                api(params)
                break
            except Exception as e:
                print("Cannot set up the API, retrying in 2 seconds...")
                time.sleep(2)
            if i == 2:
                print("Disconnecting...")
                exit(0)

        print("Waiting for clients to connect" )

        ss.listen(3)#Turns the socket into passive and handle 3 clients at the same time 

        my_threads = []

        while True:
        
            cs, clientAdd = ss.accept()

            x = threading.Thread(target=multi_client, args=(cs,))
            my_threads.append(x)
            x.start()
            

if __name__ == "__main__":
    main()

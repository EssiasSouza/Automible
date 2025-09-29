import paramiko
import json
import subprocess
import platform 
import os
import time
import getpass
import fnmatch

machines = []
print("*** STARTING APPLICATION... ***")
print("This application uses the file 'Inventory' to get the machines and their credentials.")
print("The file 'Inventory' should be filled as below if each machine uses different credentials:")
print('Example: {"hostname": "192.168.1.1", "username": "MachineUser", "password": "XYZ@123"},')
print("Or you can use a list of IP addresses, like this:")
print(f'192.168.1.1\n192.168.1.10\n192.168.1.2')
print("If do you want to send files you need to use the file 'seding' with the full path of the files to be sent.")
print("NOTE: If you want to send all files, use '*' in the first field. You also can combine * with extensions, like '*.txt' or '*.log'")
print("-" * 50)
print("If your machines use the same credentials, you can type them below. If not, you can leave them blank and the application will use the credentials from the 'Inventory' file.")
username = input("Type the USERNAME below and press ENTER or only press press ENTER (If the user name is on Inventory file):\nUsername: ")

if not username:
    print("Username not provided, using the one from 'Inventory' file.")
    try:
        with open("Inventory", "r") as Inventory:
            for machine in Inventory:
                machines.append(json.loads(machine.strip().rstrip(',')))
    except:
        print("The file Inventory have no credentials\nPlease FIX IT and try again!")
        exit()
else:
    password = getpass.getpass("Password: ")
    with open("Inventory", "r") as Inventory:
        for machine in Inventory:
            ip = machine.strip().rstrip(',')
            machine = '{"hostname": "' + ip + '", "username": "' + username + '", "password": "' + password + '"}'
            machines.append(json.loads(machine.strip().rstrip(',')))

continuous = input("Do you want to STOP to each execution? Type Y or N: ").lower()

def logging(logMessage):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open("Automible.log", "a", encoding="UTF-8") as resultLog:
        resultLog.write(f"{date} - {logMessage}")

def send_file_via_scp(file_path, destination_path, ip, username, password):
    print(f"Connecting to {ip}...")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=ip, username=username, password=password)

        sftp = ssh.open_sftp()
        remote_file_path = os.path.join(destination_path, os.path.basename(file_path))
        print(f"Sending {file_path} to {ip}:{remote_file_path}...")
        sftp.put(file_path, remote_file_path)
        sftp.close()

        print(f"File successfully sent to {ip}.")

    except Exception as e:
        print(f"Failed to send file to {ip}: {e}")

    finally:
        ssh.close()

def entering_ssh_and_run_commands(hostname, username, password, commands, sendings):

    def run_sudo_command(command):
        stdin, stdout, stderr = ssh.exec_command(f"sudo -S {command}")
        stdin.write(password + '\n')
        stdin.flush()
        stdout.channel.recv_exit_status()
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()

        return out, err
    
    def run_command(command):
        stdin, stdout, stderr = ssh.exec_command(command)
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()

        return out, err

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)

        for sending in sendings:
            file_path, destination_path = sending.split(':')
            crate_dir = './CRATE'
            print(file_path, destination_path)

            if file_path == '*':
                for item in os.listdir(crate_dir):
                    full_path = os.path.join(crate_dir, item)
                    if os.path.isfile(full_path):
                        send_file_via_scp(full_path, destination_path, hostname, username, password)

            elif '*' in file_path:
                for item in os.listdir(crate_dir):
                    full_path = os.path.join(crate_dir, item)
                    if os.path.isfile(full_path) and fnmatch.fnmatch(item, file_path):
                        send_file_via_scp(full_path, destination_path, hostname, username, password)

            else:
                full_path = os.path.join(crate_dir, file_path)
                if os.path.isfile(full_path):
                    send_file_via_scp(full_path, destination_path, hostname, username, password)
                else:
                    print(f"File {full_path} does not exist. Skipping...")

        for command in commands:
            print(f"Executando '{command}' em {machine['hostname']}...")
            username = machine['username']
            password = machine['password']

            def result_std(stdout, stderr):
                result = stdout
                error = stderr

                IGNORED_ERRORS = ["[sudo] password", "[sudo] senha", "[sudo] senha para", "[sudo] password for"]
                
                def is_real_error(stderr):
                    if not stderr.strip():
                        return False
                    for ign in IGNORED_ERRORS:
                        if ign.lower() in stderr.lower():
                            return False
                    return True

                if is_real_error(error):
                    print(f"Running with error in {hostname}: {error} : {result}")
                    logging(f"{hostname}; Erro while running command in: {error}\n")
                else:
                    print(f"Command result in {hostname}: {result}")
                    logging(f"{hostname}; {result}\n")

            if command.startswith('sudo'):
                # commandS = f"echo {password} | sudo -S {command[5:]}"
                stdout, stderr = run_sudo_command(command[5:])
                result_std(stdout, stderr)
            else:
                stdout, stderr = run_command(command)
                result_std(stdout, stderr)

        ssh.close()

    except Exception as e:
        print(f"Erro ao conectar em {hostname}: {str(e)}")
        logging(f"Erro ao conectar em {hostname}: {str(e)}\n")
        pass

def ping_ip(ip_address):
    try:
        # Check the platform and adjust the command accordingly
        param = '-c' if platform.system().lower() != 'windows' else '-n'
        command = ['ping', param, '2', ip_address]
        
        # Execute the ping command
        if subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            return "OK"
        else:
            return "NOK"
    except Exception as e:
        print(f"Erro ao executar ping: {str(e)}")
        return "NOK"

with open("sending", "r", encoding="UTF-8") as fileToSend:
    sendings = [line.strip() for line in fileToSend]

with open("commands", "r", encoding="UTF-8") as commandList:
    commands = [line.strip() for line in commandList]

for machine in machines:
    print("=====================================")
    print(machine['hostname'])
    ip_address = machine['hostname']
    ping_result = ping_ip(ip_address)

    if ping_result == "OK":
        print("PING OK")
        entering_ssh_and_run_commands(ip_address, username, password, commands, sendings)
        if continuous == "y" or continuous == "yes" or continuous == "s":
            input("NEXT >> ? (ENTER)")
    if ping_result != "OK":
        print(f"{ip_address}; Sem resposta no PING\n")
        logging(f"{ip_address}; Sem resposta no PING\n")
        if continuous == "y" or continuous == "yes" or continuous == "s":
            input("NEXT >> ? (ENTER)")
        pass

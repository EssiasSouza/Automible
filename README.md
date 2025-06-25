# Essiasble – Remote SSH Command Executor & File Sender

Essiasble is a Python-based tool that automates remote command execution and file transfers over SSH/SCP to multiple Linux-based machines. The application uses an inventory file (`Inventory.txt`) to define host machines and their credentials, and it can execute a sequence of shell commands defined in `commands.txt`.

---

## Features

* Execute multiple shell commands remotely via SSH
* Send files to multiple machines using SCP
* Supports global or per-machine login credentials
* Logs all actions and outputs to a file (`Essiasble.log`)
* Optional manual control between machine executions
* Automatic platform-based ping check before execution

---

## User Guide

### Prerequisites

* Python 3.x
* Linux/Unix or Windows machine
* All of libraries needed are ready to be used as a virtual environment. Follow these steps

1. Before run application execute the command:

```
python3 -m venv venv
```

2. Activate the virtual environment

**for Windows**
```
.\venv\Scripts\activate
```

**for Linux**
```
source venv/bin/activate 
```

3. Install all of libraries in requirements

```
pip install --no-index --find-links=libs -r requirements.txt
```

---

### File Structure

* `Inventory.txt` – List of target machines with credentials or just IPs
* `commands.txt` – List of shell commands to execute on each machine
* `Essiasble.log` – Log output of all command results and errors
* `Essiasble.py` – Main application script

---

### Inventory File Format

There are **two options** for defining your inventory:

#### 1. Per-machine credentials (JSON lines):

```json
{"hostname": "192.168.1.1", "username": "pi", "password": "raspberry"},
{"hostname": "192.168.1.2", "username": "pi", "password": "raspberry"}
```

#### 2. IP-only list (shared credentials mode):

```
192.168.1.1
192.168.1.2
192.168.1.3
```

If you choose the second option, you will be prompted to input a **global username and password** that will be used for all machines.

---

### How to Use

1. **Prepare your `Inventory.txt` and `commands.txt` files.**

2. **Run the application:**

```bash
python Essiasble.py
```

3. **Follow the interactive prompts:**

* Enter a global username/password (or leave blank to use credentials from `Inventory.txt`).
* Choose if you want to pause before processing each machine (`Y/N`).

4. The application will:

   * Ping each machine
   * If online, connect via SSH
   * Execute the commands listed in `commands.txt`
   * Optionally send a predefined file (commented in code)
   * Log all results in `Essiasble.log`

---

## Script Structure

### Credentials Handling

* If a global username is provided, each line in `Inventory.txt` is treated as an IP address.
* Otherwise, each line is parsed as a JSON string containing full connection details.

### Logging

* All results and errors are appended to `Essiasble.log`.

### Command Execution

```python
execute_ssh_command(hostname, username, password, command)
```

* Executes a single command on a remote machine.
* Supports `sudo` by injecting the password with `echo {password} | sudo -S`.

### File Transfer (SCP)

```python
send_file_via_scp(file_path, destination_path, ip, username, password)
```

* Uploads a local file to the remote path using SFTP.

> File transfer is currently **commented** in the main loop. Uncomment the function call to activate it.

### Connectivity Check

```python
ping_ip(ip_address)
```

* Cross-platform ping check to ensure machine is online.

---

## Notes

* Designed for Linux-based remote machines (e.g., Raspberry Pi).
* Hardcoded file path and remote directory for file transfers can be modified as needed:

  ```python
  file_path = r"C:\Path\To\Your\File.txt"
  destination_path = "/home/pi/EDI/"
  ```

---

## License

This project is for educational and internal automation purposes. No formal license.

---

## Author

**Essias Souza** (Essias Souza)[https://github.com/EssiasSouza]
Tech Professional | Python & Automation Specialist
*Known for teaching keyboard music and working with musical tech*
Suzano, São Paulo – Brazil


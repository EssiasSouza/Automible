# Automible – Remote SSH Command Executor & File Sender

Automible is a Python-based tool that automates remote command execution and file transfers over SSH/SCP to multiple Linux-based machines. The application uses an inventory file (`Inventory`) to define host machines and their credentials, and it can execute a sequence of shell commands defined in `commands`.

---

## Features

* Execute multiple shell commands remotely via SSH
* Send files to multiple machines using SCP
* Supports global or per-machine login credentials
* Logs all actions and outputs to a file (`Automible.log`)
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

* `Inventory` – List of target machines with credentials or just IPs
* `commands` – List of shell commands to execute on each machine
* `Automible.log` – Log output of all command results and errors
* `Automible.py` – Main application script

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

#### File of list sending files.

If you want to send one file to each machine in your `Inventory` you can write a file named `sending` with the content to send and the remote destination. For example:

```
file1.txt:/home/user/
file2.jpg:/var/www/public_html/images/
```

In this case to each machine will be runned a sending of the files in order your file.

If want to send all of files in your environment you can use the wildcard * or if is a lot of files with the same extension you can use *.XXX (where XXX is the file extension).For example:

```
*.txt:/home/user/
*.jpg:/var/www/public_html/images/
```

You should use the `CRATE` directory to put your files to be sent. Make sure your user has the privilegies to write files in destination folder.
---

### How to Use

1. **Prepare your `Inventory` and `commands` files.**

2. **Run the application:**

```bash
python Automible.py
```

3. **Follow the interactive prompts:**

* Enter a global username/password (or leave blank to use credentials from `Inventory`).
* Choose if you want to pause before processing each machine (`Y/N`).

4. The application will:

   * Ping each machine
   * If online, connect via SSH
   * Execute the commands listed in `commands`
   * Optionally send a predefined file (commented in code)
   * Log all results in `Automible.log`

---

## Script Structure

### Credentials Handling

* If a global username is provided, each line in `Inventory` is treated as an IP address.
* Otherwise, each line is parsed as a JSON string containing full connection details.

### Logging

* All results and errors are appended to `Automible.log`.

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

**[Essias Souza](https://github.com/EssiasSouza)**

Tech Professional | Python & Automation Specialist
*Known for teaching IT and working with musical tech*
Suzano, São Paulo – Brazil


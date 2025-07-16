
# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
 
## [Unreleased] - 2025-06-25
 
Here we write upgrading notes for brands. It's a team effort to make them as
straightforward as possible.
 
### Added

- Will be added a function to send more than one file and to diferent destination. Example: filex.txt to /home/pi/filex/filex.txt, filey.txt to /home/pi/filey.txt
- A function to choose a port of connection will be added in this next version.
 
### Changed
 
### Fixed
- Fix the alert message showed when it starts.
```
...\venv\Lib\site-packages\paramiko\pkey.py:100: CryptographyDeprecationWarning: TripleDES has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.TripleDES and will be removed from cryptography.hazmat.primitives.ciphers.algorithms in 48.0.0.
  "cipher": algorithms.TripleDES,
...\venv\Lib\site-packages\paramiko\transport.py:258: CryptographyDeprecationWarning: TripleDES has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.TripleDES and will be removed from cryptography.hazmat.primitives.ciphers.algorithms in 48.0.0.
  "class": algorithms.TripleDES,
```
---
 
## [1.1.0] - 2025-06-15
  
In this change I added some function. See the version 1.1.0
 
### Added

- A function to run sudo commands and put the password using the stdin to make it.

### Changed
  
- Fixed the logical changing the stop function to run after the command list.
- Fixed command list execution that was executing one by one connecting and closing the connection. Now to each machine, the script makes a connection and run the whole list of commands saving it in the log file and closing after all of commands.

---
 
## [1.0.1] - 2025-06-15
  
In this change I added some function. See the version 1.0.1.
 
### Added

- A function to wait for a user prompt. If the user type some user, then the application ask the password. This function is important when all of destination machines use the same user and password. If not, the user will need only to push ENTER to the script look for the credentials in the Inventory.txt

### Changed
  
- Nothing was just changed.
 
### Fixed
 
- Fixed the log using strip on the terminal result to avoid log with blank lines..


# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
 
## [Unreleased] - 2025-06-25
 
Here we write upgrading notes for brands. It's a team effort to make them as
straightforward as possible.
 
### Added

- Will be added a function to send more than one file and to diferent destination. Example: filex.txt to /home/pi/filex/filex.txt, filey.txt to /home/pi/filey.txt
 
### Changed
 
### Fixed
 
## [1.0.1] - 2025-06-15
  
In this change I added some function. See the version 1.0.1.
 
### Added

- A function to wait for a user prompt. If the user type some user, then the application ask the password. This function is important when all of destination machines use the same user and password. If not, the user will need only to push ENTER to the script look for the credentials in the Inventory.txt

### Changed
  
- Nothing was just changed.
 
### Fixed
 
- Fixed the log using strip to the result to avoid log with blank lines..
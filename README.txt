#Linux Command Line Emulation with Python
##Overview
Python program to emulate the Linux command line and access control principles. Available commands: useradd, login, logout, groupadd, chmod, chown, chrgrp, usergrp, ls, execute, write, read, mkfile, end. Reads a file containing a list of commands and performs the associated Linux command. Creates and uses 4 files: accounts.txt (manages system accounts), groups.txt (manages system groups), audit.txt (Log file), files.txt (files and permissions). Results of execution printed to terminal and logged in the audit.txt file. First command to the system must be creating the root user using useradd command. Last command must be end.

##Setup
How to compile:
- requires text file containing commands (example given in testcase.txt)
- assumes file is in the same directory as .py file

python3 LinuxCommandLine.py filename

###Provided Example
python3 LinuxCommandLine.py testcase.txt

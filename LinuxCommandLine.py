# Commmand Line Interface Mimicking Linux
# Available Commands: useradd, login, logout, groupadd, chmod, chown, chrgrp, usergrp, ls, execute, write, read, mkfile, end
import sys

loggedIn = False
user = None
group = {}
files = {}

# read in commands from input given at command line
with open(sys.argv[1], 'r') as f:
    commands = f.readlines()

# look at each line in input
for x in range(0, len(commands)):
    # split command up
    words = commands[x].split()

    # terminate program if first command not creating root user
    if (x == 0 and words[0] != 'useradd') or (x==0 and words[1] != 'root'):
        print("Error: First instruction must create superuser root")
        break

    # add a new user to system
    if words[0] == 'useradd':
        # special first command, add root, use 'w' to clear accounts.txt
        if x == 0:
            accounts = open('accounts.txt', 'w')
            accounts.write(words[1] + ' ' + words[2] + "\n")
            accounts.close()
            print('User ' + words[1] + ' created')
            audit = open('audit.txt', 'w')
            audit.write('User ' + words[1] + ' created \n')
            audit.close()

        # must be root to execute
        elif user == 'root':
            accounts = open('accounts.txt', 'r')
            userinfo = accounts.readlines()
            accounts.close()
            matched = False
            # check if user already exists
            for y in range(0, len(userinfo)):
                usernames = userinfo[y].split()
                if words[1] == usernames[0]:
                    matched = True
                    print('Useradd Error: User ' + words[1] + ' already exists')
                    audit = open('audit.txt', 'a')
                    audit.write('Useradd Error: User ' + words[1] + ' already exists \n')
                    audit.close()
                    break

            # create user if doesn't already exist
            if matched == False:
                accounts = open('accounts.txt', 'a')
                accounts.write(words[1] + ' ' + words[2] + "\n")
                accounts.close()
                print('User ' + words[1] + ' created')
                audit = open('audit.txt', 'a')
                audit.write('User ' + words[1] + ' created \n')
                audit.close()

        # throw error if not root
        else:
            print('Useradd Error: Must be root user to execute useradd')
            audit = open('audit.txt', 'a')
            audit.write('Useradd Error: Must be root user to execute useradd \n')
            audit.close()

    # Log in to an account
    elif words[0] == 'login':
        # can't support concurrent users
        if loggedIn == True:
            print('Login Error: Cannot login in, user ' + user + ' already logged in')
            audit = open('audit.txt', 'a')
            audit.write('Login Error: Cannot login in, user ' + user + ' already logged in \n')
            audit.close()
        else:
            a = open('accounts.txt', 'r')
            accounts = a.readlines()
            a.close()
            # check username and password is valid
            for i in range(0, len(accounts)):
                login = accounts[i].split()
                # log in if the valid combo is found
                if words[1] == login[0] and words[2] == login[1]:
                    loggedIn = True
                    user = words[1]
                    print('User ' + words[1] + ' logged in')
                    audit = open('audit.txt', 'a')
                    audit.write('User ' + words[1] + ' logged in \n')
                    audit.close()
                    break

        # user and password combo not correct
        if loggedIn == False:
            print('Login Failed: Incorrect username or password')
            audit = open('audit.txt', 'a')
            audit.write('Login Failed: Incorrect username or password \n')
            audit.close()

    # log out of account
    elif words[0] == 'logout':
        if loggedIn:
            print('User ' + user + ' logged out')
            audit = open('audit.txt', 'a')
            audit.write('User ' + user + ' logged out \n')
            audit.close()
            loggedIn = False
            user = None
        else:
            print('Logout Error: no user logged in')
            audit = open('audit.txt', 'a')
            audit.write('Logout Error: no user logged in \n')
            audit.close()

    # Add groups on the system
    elif words[0] == 'groupadd':
        # must be root to add groups
        if user == 'root':
            # cannot name group nil
            if words[1] == 'nil':
                print('Groupadd Error: Invalid group name cannot be nil')
                audit = open('audit.txt', 'a')
                audit.write('Groupadd Error: Invalid group name cannot be nil \n')
                audit.close()
            # check if group already exists
            elif words[1] in group.keys():
                print('Groupadd Error: Group ' + words[1] + ' already exists')
                audit = open('audit.txt', 'a')
                audit.write('Groupadd Error: Group ' + words[1] + ' already exists \n')
                audit.close()
            # create group
            else:
                group[words[1]] = []
                print('Group ' + words[1] + ' created')
                audit = open('audit.txt', 'a')
                audit.write('Group ' + words[1] + ' created \n')
                audit.close()
        # user is not root
        else:
            print('Groupadd Error: must be root to create groups')
            audit = open('audit.txt', 'a')
            audit.write('Groupadd Error: must be root to create group \n')
            audit.close()

    # Add a user to a group
    elif words[0] == 'usergrp':
        # must be root to execute
        if user == 'root':
            # check if group exists
            if words[2] not in group.keys():
                print('Usergrp Error: could not add ' + words[1] + ' to group, ' + words[2] + ' does not exist')
                audit = open('audit.txt', 'a')
                audit.write('Usergrp Error: could not add ' + words[1] + ' to group, ' + words[2] + ' does not exist \n')
                audit.close()
            # check if user exists
            accounts = open('accounts.txt', 'r')
            userinfo = accounts.readlines()
            accounts.close()
            matched = False
            for y in range(0, len(userinfo)):
                usernames = userinfo[y].split()
                if words[1] == usernames[0]:
                    matched = True
                    break
            # user does not exist
            if matched == False:
                print('Usergrp Error: could not add ' + words[2] + ' to group, ' + words[1] + ' user does not exist')
                audit = open('audit.txt', 'a')
                audit.write('Usergrp Error: could not add ' + words[2] + ' to group, ' + words[1] + ' user does not exist \n')
                audit.close()
            else:
                group[words[2]].append(words[1])
                print('User ' + words[1] + ' added to group ' + words[2])
                audit = open('audit.txt', 'a')
                audit.write('User ' + words[1] + ' added to group ' + words[2] + '\n')
                audit.close()
        # user is not root
        else:
            print('Usergrp Error: must be root to add users to groups')
            audit = open('audit.txt', 'a')
            audit.write('Usergrp Error: must be root to add users to groups \n')
            audit.close()

     # make file
    elif words[0] == 'mkfile':
        # check if file already exists
        if words[1] in files.keys():
            print('Mkfile Error: File ' + words[1] + ' already exists')
            audit = open('audit.txt', 'a')
            audit.write('Mkfile Error: File ' + words[1] + ' already exists \n')
            audit.close()
        # must be logged in
        elif user is None:
            print('Mkfile Error: Must be logged in to create files')
            audit = open('audit.txt', 'a')
            audit.write('Mkfile Error: Must be logged in to create files \n')
            audit.close()
        # reserved filenames
        elif (words[1] == 'accounts.txt') or (words[1] == 'audit.txt') or (words[1] == 'groups.txt') or (words[1] == 'files.txt'):
            print('Mkfile Error: Filename ' + words[1] + ' is reserved')
            audit = open('audit.txt', 'a')
            audit.write('Mkfile Error: Filename ' + words[1] + ' is reserved\n')
            audit.close()
        # create file
        else:
            files[words[1]] = []
            files[words[1]].append(user)
            files[words[1]].append('nil')
            files[words[1]].append('rw- --- ---')
            mkfile = open(words[1], 'w')
            mkfile.close()
            print('File ' + words[1] + ' with owner ' + user + ' and default permissions created')
            audit = open('audit.txt', 'a')
            audit.write('File ' + words[1] + ' with owner ' + user + ' and default permissions created\n')
            audit.close()

    # change file permissions
    elif words[0] == 'chmod':
        fileOwner = files.get(words[1])
        # check if file exists
        if words[1] not in files.keys():
            print('Chmod Error: File ' + words[1] + ' does not exist')
            audit = open('audit.txt', 'a')
            audit.write('Chmod Error: File ' + words[1] + ' does not exist \n')
            audit.close()
        # must be logged in
        elif user is None:
            print('Chmod Error: Must be logged in to edit file permissions')
            audit = open('audit.txt', 'a')
            audit.write('Chmod Error: Must be logged in to edit file permissions \n')
            audit.close()
        # reserved files
        elif words[1] == 'accounts.txt' or words[1] == 'audit.txt' or words[1] == 'groups.txt' or words[1] == 'files.txt':
            print('Chmod Error: Filename ' + words[1] + ' is reserved')
            audit = open('audit.txt', 'a')
            audit.write('Chmod Error: Filename ' + words[1] + ' is reserved\n')
            audit.close()
        # must be file owner or root
        elif user == fileOwner[0] or user == 'root':
            perm = words[2] + words[3] + words[4]
            info = files[words[1]]
            info[2] = perm
            print('Permissions for ' + words[1] + ' set to ' + perm + ' by ' + user)
            audit = open('audit.txt', 'a')
            audit.write('Permissions for ' + words[1] + ' set to ' + perm + ' by ' + user + '\n')
            audit.close()

    # change file owner
    elif words[0] == 'chown':
        # check if file exists
        if words[1] not in files.keys():
            print('Chown Error: File ' + words[1] + ' does not exist')
            audit = open('audit.txt', 'a')
            audit.write('Chown Error: File ' + words[1] + ' does not exist \n')
            audit.close()
        # reserved files
        elif words[1] == 'accounts.txt' or words[1] == 'audit.txt' or words[1] == 'groups.txt' or words[1] == 'files.txt':
            print('Chown Error: Filename ' + words[1] + ' is reserved')
            audit = open('audit.txt', 'a')
            audit.write('Chown Error: Filename ' + words[1] + ' is reserved\n')
            audit.close()
        elif user == 'root':
            # check if user exists
            accounts = open('accounts.txt', 'r')
            userinfo = accounts.readlines()
            accounts.close()
            match = False
            for y in range(0, len(userinfo)):
                usernames = userinfo[y].split()
                if words[2] == usernames[0]:
                    match = True

            if match:
                info = files[words[1]]
                # change owner to new user
                info[0] = words[2]
                print('Owner of ' + words[1] + ' changed to ' + words[2])
                audit = open('audit.txt', 'a')
                audit.write('Owner of ' + words[1] + ' changed to ' + words[2] + '\n')
                audit.close()
            else:
                print('Chown Error: User ' + words[2] + ' does not exist')
                audit = open('audit.txt', 'a')
                audit.write('Chown Error: User ' + words[2] + ' does not exist\n')
                audit.close()
        else:
            print('Chown Error: must be root user to execute')
            audit = open('audit.txt', 'a')
            audit.write('Chown Error: must be root user to execute \n')
            audit.close()

    # change a file's group
    elif words[0] == 'chgrp':
        fileOwner = files.get(words[1])
        if words[1] == 'accounts.txt' or words[1] == 'audit.txt' or words[1] == 'groups.txt' or words[1] == 'files.txt':
            print('Chgrp Error: Filename ' + words[1] + ' is reserved')
            audit = open('audit.txt', 'a')
            audit.write('Chgrp Error: Filename ' + words[1] + ' is reserved\n')
            audit.close()
        # check if file exists
        elif words[1] not in files.keys():
            print('Chgrp Error: File ' + words[1] + ' does not exist')
            audit = open('audit.txt', 'a')
            audit.write('Chgrp Error: File ' + words[1] + ' does not exist \n')
            audit.close()
        elif words[2] not in group.keys():
            print('Chgrp Error: Group ' + words[2] + ' does not exist')
            audit = open('audit.txt', 'a')
            audit.write('Chgrp Error: Group ' + words[2] + ' does not exist \n')
            audit.close()
        elif user is None:
            print('Chgrp Error: Must be logged in to change file group')
            audit = open('audit.txt', 'a')
            audit.write('Chgrp Error: Must be logged in to change file group \n')
            audit.close()
        elif user not in group.get(words[2]) and user != 'root':
            print('Chgrp Error: User ' + user + ' not a member of group ' + words[2])
            audit = open('audit.txt', 'a')
            audit.write('Chgrp Error: User ' + user + ' not a member of group ' + words[2] + '\n')
            audit.close()
        elif user == fileOwner[0] or user == 'root':
            info = files[words[1]]
            # change group
            info[1] = words[2]
            print('Group for ' + words[1] + ' set to ' + words[2] + ' by ' + user)
            audit = open('audit.txt', 'a')
            audit.write('Group for ' + words[1] + ' set to ' + words[2] + ' by ' + user + '\n')
            audit.close()

    # read a file
    elif words[0] == 'read':
        # file does not exist
        if words[1] not in files.keys():
            print('Read Error: File ' + words[1] + ' does not exist')
            audit = open('audit.txt', 'a')
            audit.write('Read Error: File ' + words[1] + ' does not exist \n')
            audit.close()
        # must be logged in
        elif user is None:
            print('Read Error: Must be logged in to read files')
            audit = open('audit.txt', 'a')
            audit.write('Read Error: Must be logged in to read files \n')
            audit.close()
        elif words[1] == 'accounts.txt' or words[1] == 'audit.txt' or words[1] == 'groups.txt' or words[1] == 'files.txt':
            print('Read Error: Filename ' + words[1] + ' is reserved')
            audit = open('audit.txt', 'a')
            audit.write('Read Error: Filename ' + words[1] + ' is reserved\n')
            audit.close()
        else:
            fileInfo = files.get(words[1])
            fperms = fileInfo[2]
            #if user is owner and read enabled for owner or user is root
            if (user == fileInfo[0] and fperms[0] == 'r') or user == 'root':
                r = open(words[1], 'r')
                read = r.read()
                r.close()
                print('User ' + user + ' reads ' + words[1] + ' as: ' + read)
                audit = open('audit.txt', 'a')
                audit.write('User ' + user + ' reads ' + words[1] + ' as: ' + read + '\n')
                audit.close()
            # others have read permission and user not file owner
            elif fperms[6] == 'r' and user != fileInfo[0]:
                r = open(words[1], 'r')
                read = r.read()
                r.close()
                print('User ' + user + ' reads ' + words[1] + ' as: ' + read)
                audit = open('audit.txt', 'a')
                audit.write('User ' + user + ' reads ' + words[1] + ' as: ' + read + '\n')
                audit.close()
            # group has read access and user is in group
            elif fileInfo[1] != 'nil' and user in group.get(fileInfo[1]) and fperms[3] == 'r':
                r = open(words[1], 'r')
                read = r.read()
                r.close()
                print('User ' + user + ' reads ' + words[1] + ' as: ' + read)
                audit = open('audit.txt', 'a')
                audit.write('User ' + user + ' reads ' + words[1] + ' as: ' + read + '\n')
                audit.close()
            else:
                print('User ' + user + ' denied read access to ' + words[1])
                audit = open('audit.txt', 'a')
                audit.write('User ' + user + ' denied read access to ' + words[1] + '\n')
                audit.close()

    # write text to a file
    elif words[0] == 'write':
        # file does not exist
        if words[1] not in files.keys():
            print('Write Error: File ' + words[1] + ' does not exist')
            audit = open('audit.txt', 'a')
            audit.write('Write Error: File ' + words[1] + ' does not exist \n')
            audit.close()
        elif user is None:
            print('Write Error: Must be logged in to write to files')
            audit = open('audit.txt', 'a')
            audit.write('Write Error: Must be logged in to write to file \n')
            audit.close()
        elif words[1] == 'accounts.txt' or words[1] == 'audit.txt' or words[1] == 'groups.txt' or words[1] == 'files.txt':
            print('Write Error: Filename ' + words[1] + ' is reserved')
            audit = open('audit.txt', 'a')
            audit.write('Write Error: Filename ' + words[1] + ' is reserved\n')
            audit.close()
        else:
            fileInfo = files.get(words[1])
            fperms = fileInfo[2]
            # user is owner and owner has permission or user is root
            if (user == fileInfo[0] and fperms[1] == 'w') or user == 'root':
                w = open(words[1], 'a')
                text = ''
                for t in range(2, len(words)):
                    text += (' ' + words[t])
                w.write(text)
                w.close()
                print('User ' + user + ' wrote to ' + words[1] + ':' + text)
                audit = open('audit.txt', 'a')
                audit.write('User ' + user + ' wrote to ' + words[1] + ': ' + text + '\n')
                audit.close()
            # others have write permission and user not file owner
            elif fperms[7] == 'w' and user != fileInfo[0]:
                w = open(words[1], 'a')
                text = ''
                for t in range(2, len(words)):
                    text += (' ' + words[t])
                w.write(text)
                w.close()
                print('User ' + user + ' wrote to ' + words[1] + ':' + text)
                audit = open('audit.txt', 'a')
                audit.write('User ' + user + ' wrote to ' + words[1] + ': ' + text + '\n')
                audit.close()
            # group has write access and user is in group
            elif fileInfo[1] != 'nil' and user in group.get(fileInfo[1]) and fperms[4] == 'w':
                w = open(words[1], 'a')
                text = ''
                for t in range(2, len(words)):
                    text += (' ' + words[t])
                w.write(text)
                w.close()
                print('User ' + user + ' wrote to ' + words[1] + ':' + text)
                audit = open('audit.txt', 'a')
                audit.write('User ' + user + ' wrote to ' + words[1] + ': ' + text + '\n')
                audit.close()
            else:
                print('User ' + user + ' denied write access to ' + words[1])
                audit = open('audit.txt', 'a')
                audit.write('User ' + user + ' denied write access to ' + words[1] + '\n')
                audit.close()

    # execute a file
    elif words[0] == 'execute':
        if words[1] not in files.keys():
            print('Execution Error: File ' + words[1] + ' does not exist')
            audit = open('audit.txt', 'a')
            audit.write('Execution Error: File ' + words[1] + ' does not exist \n')
            audit.close()
        elif user is None:
            print('Execution Error: Must be logged in to execute to files')
            audit = open('audit.txt', 'a')
            audit.write('Execution Error: Must be logged in to execute to files \n')
            audit.close()
        elif words[1] == 'accounts.txt' or words[1] == 'audit.txt' or words[1] == 'groups.txt' or words[1] == 'files.txt':
            print('Execution Error: Filename ' + words[1] + ' is reserved')
            audit = open('audit.txt', 'a')
            audit.write('Execution Error: Filename ' + words[1] + ' is reserved\n')
            audit.close()
        else:
            fileInfo = files.get(words[1])
            fperms = fileInfo[2]
            # user is owner and owner has permission or user is root
            if (user == fileInfo[0] and fperms[2] == 'x') or user == 'root':
                print('File ' + words[1] + ' executed by ' + user)
                audit = open('audit.txt', 'a')
                audit.write('File ' + words[1] + ' executed by ' + user + '\n')
                audit.close()
            # others have write permission and user not file owner
            elif fperms[8] == 'x' and user != fileInfo[0]:
                print('File ' + words[1] + ' executed by ' + user)
                audit = open('audit.txt', 'a')
                audit.write('File ' + words[1] + ' executed by ' + user + '\n')
                audit.close()
            # group has write access and user is in group
            elif fileInfo[1] != 'nil' and user in group.get(fileInfo[1]) and fperms[5] == 'x':
                print('File ' + words[1] + ' executed by ' + user)
                audit = open('audit.txt', 'a')
                audit.write('File ' + words[1] + ' executed by ' + user+ '\n')
                audit.close()
            else:
                print('User ' + user + ' denied execution access to ' + words[1])
                audit = open('audit.txt', 'a')
                audit.write('User ' + user + ' denied execution access to ' + words[1] + '\n')
                audit.close()

    # list files
    elif words[0] == 'ls':
        if words[1] == 'accounts.txt' or words[1] == 'audit.txt' or words[1] == 'groups.txt' or words[1] == 'files.txt':
            print('Chgrp Error: Filename ' + words[1] + ' is reserved')
            audit = open('audit.txt', 'a')
            audit.write('Chgrp Error: Filename ' + words[1] + ' is reserved\n')
            audit.close()
        elif words[1] not in files.keys():
            print('Ls Error: File ' + words[1] + ' does not exist')
            audit = open('audit.txt', 'a')
            audit.write('Ls Error: File ' + words[1] + ' does not exist \n')
            audit.close()
        elif user == None:
            print('Ls Error: Must be logged in to execute to ls')
            audit = open('audit.txt', 'a')
            audit.write('Ls Error: Must be logged in to execute ls \n')
            audit.close()
        else:
            info = files[words[1]]
            print(words[1] + ':' + info[0] + ' ' + info[1] + ' ' + info[2])
            audit = open('audit.txt', 'a')
            audit.write(words[1] + ':' + info[0] + ' ' + info[1] + ' ' + info[2] + '\n')
            audit.close()

    # end program, write groups & files lists and end program
    elif words[0] == 'end':
        # write files and groups.txts
        wfile = open('files.txt', 'w')
        for key in files.keys():
            flist = files.get(key)
            wfile.write(key + ':' + flist[0] + ' ' + flist[1] + ' ' + flist[2] + '\n')
        wfile.close()

        gfile = open('groups.txt', 'w')
        for key in group.keys():
            glist = group.get(key)
            gfile.write(key + ':')
            for person in glist:
                gfile.write(person + ' ')
            gfile.write('\n')
        gfile.close()
        # break and terminate program
        break

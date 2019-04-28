#!/usr/bin/env python
# encoding=utf-8
import sys
from server_cli.server import *

def sss():
    if len(sys.argv) == 1:
        servers = read_servers()
        display(servers)
        if len(servers) != 0:
            id = input("id > ")
            connect_server(id)
        exit(0)

    elif len(sys.argv) == 2:
        if sys.argv[1] == "ls":
            servers = read_servers()
            display(servers)
            return
        elif sys.argv[1] == "add":
            add_server()
            return
        elif sys.argv[1] == "help":
            print_help()
            return
        elif sys.argv[1] == "ping":
            servers = read_servers()
            ping_servers(servers)


    elif len(sys.argv) == 3:
        if sys.argv[1] == "del":
            delete_server(sys.argv[2])
            return
        elif sys.argv[1] == "ssh":
            connect_server(sys.argv[2])
            return
        elif sys.argv[1] == "tag":
            servers = find_server_by_tag(sys.argv[2])
            display(servers)
            return
        elif sys.argv[1] == "modify":
            modify_server(sys.argv[2])
            return
    print("Invalid Command, please type 'sss help' for helping.")

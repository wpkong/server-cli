# encoding: utf-8
import json
from prettytable import PrettyTable
import subprocess
import os
import ping3
import sys
import time
import threading
import curses


config_file = os.path.join(os.environ['HOME'], ".server-cli.profile")


def print_help():
    print("""Usage:
Type 'sss' to entry interaction interface.

Available subcommands:
    ls\t\t\t\tList all servers
    add\t\t\t\tAdd a new server
    ping\t\t\t\tList all server delays in real time
    help\t\t\t\t
    
    del <server id>\t\tDelete a server from database by id
    ssh <server id>\t\tConnect a server via ssh
    tag <tag name>\t\tList all servers contained given tag name
    modify <server id>\t\tModify attributes of specified server
""")


def validate(key, value):
    value = str(value).strip()
    if key == "name":
        if len(value) == 0:
            raise RuntimeError("Input Error: 'name' can NOT be empty!")
    elif key == "user":
        if len(value) == 0:
            raise RuntimeError("Input Error: 'user' can NOT be empty!")
    elif key == "host":
        if len(value) == 0:
            raise RuntimeError("Input Error: 'host' can NOT be empty!")
    elif key == "port":
        if len(value) == 0:
            raise RuntimeError("Input Error: 'name' can NOT be empty!")
        elif not value.isdigit():
            raise RuntimeError("Input Error: 'port' must be an Integer!")
        elif not 0 < int(value) < 65536:
            raise RuntimeError("Input Error: 'port' must be in range between 1 and 65535!")
    elif key == "auth_type":
        if len(value) == 0:
            raise RuntimeError("Input Error: 'auth_type' can NOT be empty!")
        elif not value.isdigit():
            raise RuntimeError("Input Error: 'auth_type' must be an Integer!")
        elif int(value) == 1 or int(value) == 1:
            raise RuntimeError("Input Error: 'auth_type' must be 1 or 2")
    elif key == "password":
        if len(value) == 0:
            raise RuntimeError("Input Error: 'password' can NOT be empty!")
    elif key == "key_file_path":
        if len(value) == 0:
            raise RuntimeError("Input Error: 'key_file_path' can NOT be empty!")
    elif key == "id":
        if len(value) == 0:
            raise RuntimeError("Input Error: 'id' can NOT be empty!")
        elif not value.isdigit():
            raise RuntimeError("Input Error: 'id' must be an Integer!")


def read_servers():
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def write_servers(servers):
    data = json.dumps(servers, indent=2, ensure_ascii=False)
    with open(config_file, "w") as f:
        f.write(data)


def display(servers):
    x = PrettyTable(["id", "name", "user", "host", "port", "tags", "description"])
    x.align["id"] = "l"
    x.padding_width = 1
    for obj in servers:
        x.add_row(
            [str(obj["id"]), obj["name"], obj["user"], obj["host"], obj["port"],
             ",".join(obj["tags"]),
             obj["description"]])
    print(x)


def max_id(servers):
    if len(servers) == 0:
        return 0
    else:
        obj = max(servers, key=lambda p: p["id"])
        return obj["id"]


def add_server():
    name = input("name: ")
    validate("name", name)
    user = input("user: ")
    validate("user", user)
    host = input("host: ")
    validate("host", host)
    port = input("port(default: 22): ")
    if port == "": port = "22"
    validate("port", port)

    key_file = input("key file path(None if use password): ").strip()

    tags = input("tags (use ',' to split): ")
    description = input("description: ")

    servers = read_servers()

    server = {
        "id": max_id(servers) + 1,
        "name": name,
        "user": user,
        "host": host,
        "port": port,
        "key_file": key_file,
        "tags": tags.split(","),
        "description": description
    }
    servers.append(server)
    write_servers(servers)
    print("Successfully added!")


def delete_server(id):
    validate("id", id)
    id = int(id)
    servers = read_servers()
    del_index = -1
    for index, server in enumerate(servers):
        if id == server["id"]:
            del_index = index
            break
    if del_index == -1:
        print("Server not found")
        return
    else:
        del servers[del_index]
    write_servers(servers)
    print("Successfully deleted!")


def modify_server(id):
    validate("id", id)
    id = int(id)
    servers = read_servers()
    modify_index = -1
    for index, server in enumerate(servers):
        if id == server["id"]:
            modify_index = index
            break
    if modify_index == -1:
        print("Server not found")
        return

    server = servers[modify_index]

    name = input("name('{}'): ".format(server["name"]))
    if name.strip() != "": server["name"] = name
    user = input("user('{}'): ".format(server["user"]))
    if user.strip() != "": server["user"] = user
    host = input("host('{}'): ".format(server["host"]))
    if host.strip() != "": server["host"] = host
    port = input("port({}): ".format(server["port"]))
    if port.strip() != "":
        if not port.isdigit():
            raise RuntimeError("Input Error: 'port' must be an Integer!")
        elif not 0 < int(port) < 65536:
            raise RuntimeError("Input Error: 'port' must be in range between 1 and 65535!")
        else:
            server["port"] = port
    key_file = input("key file path('{}', enter '-' if use password): ".format(server["key_file"])).strip()
    if key_file.strip() != "": server["key_file"] = key_file
    if key_file.strip() == "-": server["key_file"] = ""
    tags = input("tags([{}], use ',' to split): ".format(",".join(server["tags"])))
    if tags.strip() != "": server["tags"] = tags.split(',')
    description = input("description('{}'): ".format(server["description"]))
    if description.strip() != "": server["description"] = description

    servers[modify_index] = server
    write_servers(servers)
    print("Successfully added!")


def find_server_by_tag(tag):
    servers = read_servers()
    return [server for server in servers if tag in server["tags"]]


def connect_server(id):
    validate("id", id)
    id = int(id)
    servers = read_servers()
    server = None
    for ser in servers:
        if id == ser["id"]:
            server = ser
    if server is None:
        print("Server not found")
        return
    print("Connecting to {}".format(server["name"]))
    cmd = "ssh {}@{} -p {} ".format(server["user"], server["host"], server["port"])
    if server["key_file"] is not None and server["key_file"] != "":
        cmd += "-i {}".format(server["key_file"])
    subprocess.call(cmd, shell=True)


def ping_servers(servers):
    _run = True
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.nodelay(1)

    try:
        def ping(index):
            while _run:
                delay = ping3.ping(servers[index]["host"])
                if not _run: break
                servers[index]["delay"] = int(delay * 1000)
                if not _run: break
                time.sleep(0.5)

        for index in range(len(servers)):
            servers[index]["delay"] = "inf"
            t = threading.Thread(target=ping, args=[index])
            t.start()

        while True:
            x = PrettyTable(["id", "name", "host", "tags", "description", "delay(ms)"])
            x.align["id"] = "l"
            x.padding_width = 1
            for obj in servers:
                x.add_row(
                    [str(obj["id"]), obj["name"], obj["host"],",".join(obj["tags"]),
                     obj["description"], obj["delay"]])
            stdscr.clear()
            stdscr.addstr(str(x))
            stdscr.refresh()
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        _run = False
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        print("Terminated!")

===========
Server-cli
===========
|License: MIT| |Badge|

.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

.. |Badge| image:: https://img.shields.io/badge/link-996.icu-%23FF4D5B.svg?style=flat-square
    :target: https://996.icu/#/en_US


A server management tool which helps you memorize ssh command



Installation:
==============
::

 $ pip install server-cli

Usage:
==============

Type 'sss' to entry interaction interface.

Available subcommands:
-----------------------

- ls [list all servers]

- add [add a new server]

- help

- del <server id> [delete a server from database by id]

- ssh <server id> [connect a server via ssh]

- tag <tag name> [list all servers contained given tag name]

- modify <server id> [modify attributes of specified server]


Example:
=========

default
--------
List all of services and wait for the specific server id::

 $ sss
 +----+-----------+--------+-----------------+------+--------------------------------+-------------------+
 | id |    name   |  user  |       host      | port |              tags              |    description    |
 +----+-----------+--------+-----------------+------+--------------------------------+-------------------+
 | 1  | 亚马逊aws  | ubuntu |     0.0.0.0     |  22  | shadowsocks,telegramBot,MTpoto |   加利福尼亚机房   |
 | 2  |   阿里云   |  root  |     0.0.0.0     |  22  |      Wechat,shadowsocks        |  阿里云 毕业就到期 |
 | 3  | 腾讯云1号  | ubuntu |     0.0.0.0     |  22  |       Blog,huginn              |                   |
 | 4  | 腾讯云3号  |  kwp   |     0.0.0.0     |  22  |         script                 |                   |
 +----+-----------+--------+-----------------+------+--------------------------------+-------------------+
 id >
 # and enter id you selected

list
-----
List all of services::

 $ sss ls
 +----+-----------+--------+-----------------+------+--------------------------------+-------------------+
 | id |    name   |  user  |       host      | port |              tags              |    description    |
 +----+-----------+--------+-----------------+------+--------------------------------+-------------------+
 | 1  | 亚马逊aws  | ubuntu |     0.0.0.0     |  22  | shadowsocks,telegramBot,MTpoto |   加利福尼亚机房   |
 | 2  |   阿里云   |  root  |     0.0.0.0     |  22  |      Wechat,shadowsocks        |  阿里云 毕业就到期 |
 | 3  | 腾讯云1号  | ubuntu |     0.0.0.0     |  22  |       Blog,huginn              |                   |
 | 4  | 腾讯云3号  |  kwp   |     0.0.0.0     |  22  |         script                 |                   |
 +----+-----------+--------+-----------------+------+--------------------------------+-------------------+


ping
-----
List all server delays in real time::

 $ sss ping
 +----+-----------+-----------------+--------------------------------+-------------------+-----------+
 | id |    name   |       host      |              tags              |    description    | delay(ms) |
 +----+-----------+-----------------+--------------------------------+-------------------+-----------+
 | 1  | 亚马逊aws  |     0.0.0.0     | shadowsocks,telegramBot,MTpoto |   加利福尼亚机房   |    310    |
 | 2  |   阿里云   |     0.0.0.0     |        Wechat,shadowsocks      |  阿里云 毕业就到期  |     45    |
 | 3  | 腾讯云1号  |     0.0.0.0     |          Blog,huginn           |                   |     30    |
 | 5  | 腾讯云3号  |     0.0.0.0     |             script             |                   |     36    |
 +----+-----------+-----------------+--------------------------------+-------------------+-----------+

add
----
Add a new server::

 $ sss add
 name: Test
 user: root
 host: 0.0.0.0
 port(default: 22):
 key file path(None if use password): /path/to/your/key
 tags (use ',' to split): test,local
 description: this is a test

 Successfully added!


delete
-------
Delete a server with the specified <server id>::

 $ sss del 6

 Successfully deleted!


tag
----
Filter out servers that contain the given <tag name>::

 $ sss tag shadowsocks
 +----+-----------+--------+----------------+------+--------------------------------+-------------------+
 | id |    name   |  user  |      host      | port |              tags              |    description    |
 +----+-----------+--------+----------------+------+--------------------------------+-------------------+
 | 1  | 亚马逊aws  | ubuntu |     0.0.0.0    |  22  | shadowsocks,telegramBot,MTpoto |   加利福尼亚机房    |
 | 2  |   阿里云   |  root  |     0.0.0.0    |  22  |       Wechat,shadowsocks       | 阿里云 毕业就到期   |
 +----+-----------+--------+----------------+------+--------------------------------+-------------------+

modify
-------
Modify a server with the specified <server id>::

 $ sss modify 1
 name('亚马逊aws'):
 user('ubuntu'):
 host('0.0.0.0'):
 port(22):
 key file path('/path/to/your/key', enter '-' if use password):
 tags([shadowsocks,telegramBot,MTpoto], use ',' to split):
 description('加利福尼亚机房'):

Todo:
==============
- [x] ping all servers
- [ ] fill password automatically
- [ ] supports Windows


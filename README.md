# rpc_remote_run

>If you want to use server and client under different directories, 
remember to move each of them with ``src/helper.py`` and ``config.ini`` files.
Both of them make use of functionality implemented in these files.
>

## Running server
```consoleLine
python3 src/server.py
```
## Running client 
``python3 src/client.py CLIENT_IP CLIENT_PORT REMOTE_COMMAND``

example:
```consoleLine
python3 src/client.py 127.0.0.1 4567 "ps aux"
```
## Config file
Server's ip and port can be configured in ``config.ini`` file.

```
[rpc.server]
ip = 127.0.0.1
port = 1234
```
As it was mentioned before, both server and client use this file.

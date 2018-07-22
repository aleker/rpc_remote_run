# rpc_remote_run
## Running instruction
If you want to use server and client under different directories, 
remember to move each of them with ``src/helper.py`` and ``config.ini`` files.
Both of them make use of functionality implemented in these two files.

#### Download requirements
```
pip install requirements.txt
```

#### Running server
```consoleLine
python3 src/server.py
```
#### Running client 
``python3 src/client.py CLIENT_IP CLIENT_PORT REMOTE_COMMAND``

>Remember that all clients working at the same time should listen on unique pair of CLIENT_IP and CLIENT_PORT!
>

examples:
```consoleLine
python3 src/client.py 127.0.0.1 4567 "ps aux"
```
```consoleLine
python3 src/client.py 127.0.0.1 4568 "ps -la"
```
```consoleLine
python3 src/client.py 127.0.0.1 4569 "ps aux | grep ola | grep 1"
```

## Additional files description

#### ``config.ini``
Server's ip and port can be configured in ``config.ini`` file. 
Client's IP and PORT are configured when starting client's application.

```
[rpc.server]
ip = 127.0.0.1
port = 1234
```
>As it was mentioned before, **both** server and client **use** this file.
>

#### ``helper.py``
`read_config_file()` function lets read server configuration from ``config.ini`` file.
>As it was mentioned before, **both** server and client **use** this file.
>

import asyncio
from rpcudp.protocol import RPCProtocol
import configparser


class RPCServer(RPCProtocol):
    # Any methods starting with "rpc_" are available to clients.
    def rpc_run_command(self, sender, command):
        # This could return a Deferred as well. sender is (ip,port)
        print("New client at %s:%i wants to: `%s`" % (sender[0], sender[1], command))
        return "Result of `%s` is ... tbc" % command


def read_config_file(config_path):
    config = configparser.ConfigParser()
    dataset = config.read(config_path)
    if len(dataset) == 1 and 'rpc.server' in config:
        return config['rpc.server']
    config.read("../" + config_path)
    if len(dataset) == 1 and 'rpc.server' in config:
        return config['rpc.server']
    raise ValueError("Failed to open/find config file!")


def main():
    # read arguments
    server_config = read_config_file('config.ini')
    server_ip = server_config['ip']
    server_port = server_config['port']

    # start a server on UDP port
    loop = asyncio.get_event_loop()
    print("----- Starting UDP-RPC server -----")

    # One protocol instance will be created to serve all client requests
    listen = loop.create_datagram_endpoint(
        RPCServer, local_addr=(server_ip, server_port))
    transport, protocol = loop.run_until_complete(listen)

    # wait for clients
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # close connection
    transport.close()
    loop.close()


if __name__ == "__main__":
    main()






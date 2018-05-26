import asyncio
import sys
from rpcudp.protocol import RPCProtocol
import configparser


@asyncio.coroutine
def run_command(protocol, address, command):
    # result will be a tuple - first arg is a boolean indicating whether a response
    # was received, and the second argument is the response if one was received.
    result = yield from protocol.run_command(address, command)
    print(result[1] if result[0] else "No response received.")


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
    if len(sys.argv) < 4:
        print("Arguments should be: CLIENT_ADDRESS CLIENT_PORT COMMAND!")
        exit(-1)
    server_config = read_config_file('config.ini')
    server_ip = server_config['ip']
    server_port = server_config['port']
    client_ip = sys.argv[1]
    client_port = sys.argv[2]
    remote_command = sys.argv[3]

    # Start local UDP server to be able to handle responses
    loop = asyncio.get_event_loop()
    print("----- Starting UDP-RPC client -----")
    connect = loop.create_datagram_endpoint(
        RPCProtocol, local_addr=(client_ip, int(client_port)))
    transport, protocol = loop.run_until_complete(connect)

    func = run_command(protocol, (server_ip, int(server_port)), remote_command)
    loop.run_until_complete(func)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    transport.close()
    loop.close()


if __name__ == "__main__":
    main()

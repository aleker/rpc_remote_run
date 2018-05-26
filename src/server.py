import asyncio
from rpcudp.protocol import RPCProtocol
import configparser
import subprocess


class RPCServer(RPCProtocol):
    # Any methods starting with "rpc_" are available to clients.
    def rpc_run_command(self, sender, command):
        print("New client at %s:%i wants to: `%s`" % (sender[0], sender[1], command))
        command_array = self.get_command_name_and_arguments(command)
        try:
            result = subprocess.check_output(command_array,
                                             stderr=subprocess.STDOUT)
            for line in result.strip().decode().splitlines():
                print(line)
            return result
        except subprocess.CalledProcessError:
            return "Error when calling remote command!"
        except FileNotFoundError:
            return "Wrong command!"

    def get_command_name_and_arguments(self, command):
        command_array = command.split()
        return command_array


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

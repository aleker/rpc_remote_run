import asyncio
from rpcudp.protocol import RPCProtocol
import subprocess

from helper import read_config_file

server = None


class RPCServer(RPCProtocol):
    # Any methods starting with "rpc_" are available to clients.
    def rpc_run_command(self, sender, command):
        print("New client at %s:%i wants to: `%s`" % (sender[0], sender[1], command))
        command_array = self.get_command_name_and_arguments(command)
        try:
            result = subprocess.check_output(command_array,
                                             stderr=subprocess.STDOUT)
            # run in background
            asyncio.ensure_future(server.print_result(sender, result))
            return "Proper command!"
        except subprocess.CalledProcessError as e:
            asyncio.ensure_future(server.print_result(sender, e.output.strip().decode()))
            return "Error when calling remote command!"
        except FileNotFoundError as e:
            asyncio.ensure_future(server.print_result(sender, str(e)))
            return "Wrong command!"
        except Exception as e:
            asyncio.ensure_future(server.print_result(sender, str(e)))
            return "Error occurred!"

    def get_command_name_and_arguments(self, command):
        command_array = command.split()
        return command_array


class Server:
    def __init__(self, server_address):
        print("----- Starting UDP-RPC server -----")
        loop = asyncio.get_event_loop()
        # One protocol instance will be created to serve all client requests
        listen = loop.create_datagram_endpoint(
            RPCServer, local_addr=server_address)
        transport, protocol = loop.run_until_complete(listen)
        self.protocol = protocol
        self.transport = transport

    @asyncio.coroutine
    def print_result(self, client_address, result):
        try:
            new_result = result.strip().decode()
        except AttributeError:
            new_result = result
        for line in new_result.splitlines():
            yield from self.protocol.print_result(client_address, line)
        yield from self.protocol.end_connection(client_address)


def main():
    # read arguments
    server_config = read_config_file('config.ini')

    # start a server on UDP port
    global server
    server = Server((server_config['ip'], server_config['port']))

    loop = asyncio.get_event_loop()
    # wait for clients
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # close connection
    server.transport.close()
    loop.close()


if __name__ == "__main__":
    main()

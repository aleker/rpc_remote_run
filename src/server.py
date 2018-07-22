import asyncio

from rpcudp.protocol import RPCProtocol
import subprocess

from helper import read_config_file

server = None


class RPCServer(RPCProtocol):
    # Any methods starting with "rpc_" are available to clients.
    def rpc_run_command(self, sender, command):
        print("New client at %s:%i wants to: `%s`" % (sender[0], sender[1], command))
        asyncio.ensure_future(server.print_result(sender, command))
        return "Request received!"


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
    def print_result(self, client_address, command):
        commands_array = self.get_command_name_and_arguments(command)
        try:
            # command output saved to PIPE
            pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            for line in iter(pipe.stdout.readline, 'b'):
                if line == b'':
                    # time.sleep(1)
                    break
                yield from self.protocol.print_result(client_address, line, False)
            for line in iter(pipe.stderr.readline, 'b'):
                if line == b'':
                    break
                yield from self.protocol.print_result(client_address, line, True)
        except subprocess.CalledProcessError as e:
            yield from self.protocol.print_result(client_address, e.output.strip().decode(), True)
        except FileNotFoundError as e:
            yield from self.protocol.print_result(client_address, str(e), True)
        except Exception as e:
            yield from self.protocol.print_result(client_address, str(e), True)
        yield from self.protocol.end_connection(client_address)

    @staticmethod
    def get_command_name_and_arguments(command):
        command_array = command.split("|")
        return command_array


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

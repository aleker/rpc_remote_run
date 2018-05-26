import asyncio
import sys
from rpcudp.protocol import RPCProtocol


class RPCServer(RPCProtocol):
    # Any methods starting with "rpc_" are available to clients.
    def rpc_sayhi(self, sender, ):
        # This could return a Deferred as well. sender is (ip,port)
        return "New client live at %s:%i" % (sender[0], sender[1])


def main():
    # read arguments
    if len(sys.argv) < 3:
        print("Arguments should be: SERVER_ADDRESS SERVER_PORT!")
        exit(-1)
    server_ip = sys.argv[1]
    server_port = sys.argv[2]

    # start a server on UDP port
    loop = asyncio.get_event_loop()
    print("Starting UDP-RPC server")

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






import asyncio
import sys
from rpcudp.protocol import RPCProtocol


@asyncio.coroutine
def sayhi(protocol, address):
    # result will be a tuple - first arg is a boolean indicating whether a response
    # was received, and the second argument is the response if one was received.
    result = yield from protocol.sayhi(address)
    print(result[1] if result[0] else "No response received.")


def main():
    # read arguments
    if len(sys.argv) < 5:
        print("Arguments should be: SERVER_ADDRESS SERVER_PORT CLIENT_ADDRESS CLIENT_PORT!")
        exit(-1)
    server_ip = sys.argv[1]
    server_port = sys.argv[2]
    client_ip = sys.argv[3]
    client_port = sys.argv[4]

    # Start local UDP server to be able to handle responses
    loop = asyncio.get_event_loop()
    connect = loop.create_datagram_endpoint(
        RPCProtocol, local_addr=(client_ip, int(client_port)))
    transport, protocol = loop.run_until_complete(connect)

    func = sayhi(protocol, (server_ip, int(server_port)))
    loop.run_until_complete(func)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    transport.close()
    loop.close()


if __name__ == "__main__":
    main()

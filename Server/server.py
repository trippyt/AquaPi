import asyncio
from loguru import logger
import os


def start_server(host='127.0.0.1', port=17000,):
    loop = asyncio.get_event_loop()
    server = asyncio.start_server(host, port, loop=loop)
    server = loop.run_until_complete(server)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    print('pid :', os.getpid())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


try:
    start_server()
except:
    logger.exception("Couldn't Start Asyncio Server")

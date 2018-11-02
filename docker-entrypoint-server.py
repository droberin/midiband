#!/usr/local/bin/python3

import logging
from midiband.server import Server, Broadcaster
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


MIDIServer = Server(
    os.environ.get('MIDISERVER_LISTEN_ADDRESS', None),
    os.environ.get('MIDISERVER_LISTEN_PORT', 65200),
)

if not os.environ.get('MIDISERVER_NO_ANNOUNCEMENT', False):
    broadcast_server = Broadcaster(
        MIDIServer.listen_address,
        MIDIServer.listen_port
    )

MIDIServer.start()

# When server ends... just finish things!
if not os.environ.get('MIDISERVER_NO_ANNOUNCEMENT', False):
    broadcast_server.finish()
logging.info("Finishing service")

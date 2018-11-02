from zeroconf import ServiceInfo, Zeroconf
import logging
import socket
import netifaces
import os

from mido import sockets


class Broadcaster:
    info = None
    zeroconf = None
    desc = {'spam': 'ArcangeluS'}

    def __init__(self, announce_address, announce_port, desc=None):
        if type(desc) is 'dict':
            del self.desc
            self.desc = desc
        logging.debug("Requested announce server at address {}".format(announce_address))
        self.zeroconf = Zeroconf()
        self.info = ServiceInfo("_midiband-hub._tcp.local.",
                                socket.gethostname() + "._midiband-hub._tcp.local.",
                                socket.inet_aton(announce_address), announce_port, 0, 0,
                                self.desc, socket.gethostname() + ".local."
                                )
        logging.info("Announcing server")
        self.zeroconf.register_service(self.info)

    def finish(self):
        logging.info("Unregistering announced server")
        self.zeroconf.unregister_service(self.info)
        self.zeroconf.close()


class Server:
    listen_port = None
    listen_address = os.environ.get('MIDIBAND_SERVER_ADDRESS', None)
    broadcaster = None

    def __init__(self, listen_address=None, listen_port=65200):
        if not listen_address:
            if self.listen_address:
                listen_address = self.listen_address
            else:
                logging.info('No listening address requested. Trying to guess...')
                listen_address = self.__try_guessing_listening_address()
            if not listen_address:
                logging.critical("No listening IP address set")
        self.listen_address = listen_address
        self.listen_port = int(listen_port)

    def start(self):
        try:
            address = str(self.listen_address) + ':' + str(self.listen_port)
            (hostname, portnumber) = sockets.parse_address(address)
            logging.info('MIDIBand Serving on {}'.format(address))
            while True:
                try:
                    with sockets.PortServer(hostname, portnumber) as server:
                        for message in server:
                            logging.info("[{}]: {}".format(hostname, message))
                except TypeError:
                    logging.warning("A message was received with no data or a connection went down abruptly")
        except KeyError as e:
            logging.critical("{}".format(e))
            pass
        except KeyboardInterrupt:
            self.broadcaster.finish()

    @staticmethod
    def __try_guessing_listening_address():
        try:
            external_interface = netifaces.gateways()['default'][2][1]
            external_ip_address = netifaces.ifaddresses(external_interface)[2][0]['addr']
            # external_net_mac = netifaces.ifaddresses(external_interface)[17][0]['addr']
            if external_ip_address:
                return external_ip_address
            return False
        except KeyError:
            logging.warning("Error trying to guess IP Address to listen to")
            return False
            pass

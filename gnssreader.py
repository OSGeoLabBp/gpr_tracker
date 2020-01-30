""" setup gnss receiver connection """
import time
import threading
import queue
from queuewriter import QueueWriter
from localiface import LocalIface
from serialiface import SerialIface
from bluetoothiface import BluetoothIface
from nmeagnssunit import NmeaGnssUnit
from gnss import Gnss

class GNSSReader(object):

    def __init__(self):
        iface = LocalIface('test', '/home/siki/ulyxes/data/nmea2.txt')
        mu = NmeaGnssUnit()
        self.q = queue.Queue()
        wr = QueueWriter(self.q)
        self.g = Gnss('', mu, iface, wr)
        self.th = threading.Thread(target=self.do, args=(None,), daemon=True)
        self.running = False

    def start(self):
        """ start the thread """
        self.th.start()
        self.running = True

    def stop(self):
        """ stop the thread """
        self.running = False
        pass

    def do(self, dummy=None):
        """ read position and put into the queue """
        while self.running:
            if self.g.measureIface.state != self.g.measureIface.IF_OK:
                # reset state to normal
                self.g.measureIface.state = self.g.measureIface.IF_OK
            # get position    
            c = self.g.Measure()
            print(c)
            time.sleep(0.8)

def do(g):
    while True:
        if g.measureIface.state != g.measureIface.IF_OK:
            # reset state to normal
            g.measureIface.state = g.measureIface.IF_OK
        # get position    
        c = g.Measure()
        print("writing {}".format(c['id']))
        time.sleep(0.8)

if __name__ == "__main__":
    from queuereader import QueueReader
    iface = LocalIface('test', '/home/siki/ulyxes/data/nmea2.txt')
    mu = NmeaGnssUnit()
    q = queue.Queue()
    wr = QueueWriter(q)
    g = Gnss('', mu, iface, wr)
    th = threading.Thread(target=do, args=(g,), daemon=True)
    th.start()
    rd = QueueReader(wr.GetQueue())

    while True:
        time.sleep(0.1)
        n = rd.GetNext()
        if n:
            print("*** reading {}".format(n['id']))

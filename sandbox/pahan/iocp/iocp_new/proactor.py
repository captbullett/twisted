from twisted.internet import default, defer
from twisted.internet.interfaces import IReactorCore, IReactorTime

import tcp
from iocpcore import iocpcore

class Proactor(iocpcore, default.PosixReactorBase):
    __implements__ = (IReactorCore, IReactorTime)
    handles = None
    iocp = None

    def __init__(self):
        default.PosixReactorBase.__init__(self)
#        self.completables = {}

    blah = None
    """
    def registerHandler(self, handle, handler):
        self.completables[int(handle)] = handler
        CreateIoCompletionPort(handle, self.iocp, int(handle), 1)

    def unregisterHandler(self, handle):
        del self.completables[handle]

    def doIteration(self, timeout):
        if timeout is None:
            timeout = INFINITE
        else:
            timeout = int(timeout * 1000)
        (ret, bytes, key, ov) = GetQueuedCompletionStatus(self.iocp, timeout)
        if int(key) not in self.completables:
            raise ValueError("unexpected completion key %s" % (key,)) # what's the right thing to do here?
        o = self.completables[int(key)]
        if __debug__:
            print "IOCPReactor got event", ret, bytes, key, ov, ov.object
        m = getattr(o, str(ov.object), None)
        if __debug__:
            print "... calling", m, "to handle"
        m(bytes)
    """

    def listenTCP(self, port, factory, backlog=5, interface=''):
        p = tcp.Port((interface, port), factory, backlog)
        p.startListening()
        return p

    def connectTCP(self, host, port, factory, timeout=30, bindAddress=None):
        c = tcp.Connector((host, port), factory, timeout, bindAddress)
        c.connect()
        return c
    
    def disconnectAll(self):
        pass

    def removeAll(self):
        pass

def install():
    p = Proactor()
    from twisted.internet import main
    main.installReactor(p)


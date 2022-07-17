"""
    Each server can request any packet from any server on the network.
    To do this, each has its own IP address.
    For simplicity, this is just an integer (natural) number from 1 to N, where N is the total number of servers.
    The algorithm is the following. 
    The server with IP = 2 is about to send a packet of information to the server with IP = 3.
    To do this, it first sends a packet to the router, and already that one looks at the IP address and
        revise the package to the desired node (server).
    To implement this scheme, it is planned to declare three classes:
        Server - to describe the operation of servers in the network;
        Router - to describe the operation of routers in the network (in this task, one router is required);
        Data - to describe a package of information.
"""


class Server:
    __IP_ADRESS = 0

    def __new__(cls, *args, **kwargs):
        cls.__IP_ADRESS += 1
        return super().__new__(cls)

    def __init__(self):
        self.buffer = list()
        self.ip = Server.__IP_ADRESS
        self.router = None

    def send_data(self, data):
        if self.router:
            self.router.buffer.append(data)

    def get_data(self):
        c = self.buffer.copy()
        self.buffer.clear()
        return c

    def get_ip(self):
        return self.ip


class Router:

    def __init__(self):
        self.buffer = list()
        self.connects = dict()

    def link(self, server):
        if server.ip not in self.connects:
            self.connects[server.ip] = server
            server.router = self

    def unlink(self, server):
        if server.ip in self.connects:
            del self.connects[server.ip]
            server.router = None

    def send_data(self):
        for data in self.buffer:
            if data.ip in self.connects:
                server = self.connects[data.ip]
                server.buffer.append(data)
        self.buffer.clear()


class Data:

    def __init__(self, data, ip):
        self.data = data
        self.ip = ip


router = Router()   # creating object of the class Router
sv_from = Server()    # creating object №1 of the class Server
sv_from2 = Server()    # creating object №2 of the class Server
router.link(sv_from)    # connecting sever №1 to the router
router.link(sv_from2)    # connecting sever №2 to the router
router.link(Server())    # creating object №3 of the class Server
router.link(Server())    # creating object №4 of the class Server
sv_to = Server()    # creating object №5 of the class Server
router.link(sv_to)    # connecting sever №5 to the router

sv_from.send_data(Data("Hello", sv_to.get_ip()))    # sending data with the string
sv_from2.send_data(Data("Hello", sv_to.get_ip()))    # sending data with the string
sv_to.send_data(Data("Hi", sv_from.get_ip()))    # sending data with the string
router.send_data()    # sending data from the router to the servers
msg_lst_from = sv_from.get_data()    # getting data on the server
msg_lst_to = sv_to.get_data()    # getting data on the server


for msg in msg_lst_to:
    print('IP:', msg.ip, 'data:', msg.data)    # reading messenge from the input data
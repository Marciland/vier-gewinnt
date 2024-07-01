'''Networking.'''
from socket import AF_INET, SOCK_STREAM, socket


class Communication:
    '''Handles in and out.'''

    def __init__(self, ip: str) -> None:
        self.ip = ip
        self._port = 51231
        self.connection: socket = None

    def wait_for_connection(self) -> None:
        '''Wait for an incoming connection.'''
        with socket(family=AF_INET, type=SOCK_STREAM) as s:
            s.bind((self.ip, self._port))
            s.listen()
            con, _ = s.accept()
            self.connection = con

    def get_move(self) -> int:
        '''Waits for the next move.'''
        while True:
            data = self.connection.recv(1)
            if len(data) == 1:
                move = data.decode(encoding='utf-8')
                return int(move)

    def send_move(self, move: int) -> None:
        '''Makes a move.'''
        data = str(move).encode(encoding='utf-8')
        self.connection.send(data)

    def join(self) -> None:
        '''Join a game.'''
        self.connection = socket(family=AF_INET, type=SOCK_STREAM)
        self.connection.connect((self.ip, self._port))

'''Any dialog with the user.'''
from tkinter import ACTIVE, LEFT, Button, Frame, Label
from tkinter.simpledialog import Dialog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components import GameFrame
    from components.menu import MultiplayerSubMenu


class EndMessage(Dialog):
    '''Dialog that popups after game ends.'''

    def __init__(self, frame, title: str, remis: bool) -> None:
        self.frame: GameFrame = frame
        self.msg = self._create_message(remis)
        self.replay: bool = False
        super().__init__(parent=frame, title=title)

    def _create_message(self, remis: bool) -> str:
        match self.frame.current_player:
            case 0:
                player = 'computer'
            case 1:
                player = 'player1'
            case 2:
                player = 'player2'
        player = self.frame.window.translation.get(player)
        msg = player + self.frame.window.translation.get('replay')
        if remis:
            msg = self.frame.window.translation.get('draw')
        return msg

    def body(self, master):
        Label(master=master, text=self.msg).pack()
        return master

    def buttonbox(self):
        # taken from Dialog and modified for custom language
        box = Frame(self)
        w = Button(box, text=self.frame.window.translation.get('retry'),
                   width=10, command=self._ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text=self.frame.window.translation.get('cancel'),
                   width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        box.pack()

    def _ok(self):
        self.replay = True
        self.ok()


class ErrorMessage(Dialog):
    '''Dialog that popups if an error occurs.'''

    def __init__(self, frame, title: str, msg: str) -> None:
        self.frame: MultiplayerSubMenu = frame
        self.msg = msg
        super().__init__(parent=frame, title=title)

    def buttonbox(self):
        # taken from Dialog and modified for custom language
        box = Frame(self)
        w = Button(box, text='Ok', width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        box.pack()

    def body(self, master):
        Label(master=master, text=self.msg).pack()
        return master

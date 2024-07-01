'''Contains a root window that renders the other components.'''
from os import getcwd, path
from tkinter import Frame, PhotoImage, Tk

from assets import Dimension

from .game import GameFrame
from .menu import MainMenu, MenuFrame, MultiplayerMenu, SettingsMenu
from .network import Communication
from .settings import Settings
from .translation import TranslationTable


class MainWindow(Tk):
    '''The main window the user interacts with.'''

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.withdraw()
        # show after rendering
        self.after(0, self.deiconify)
        self.resizable(False, False)
        self.iconbitmap(r"res\icon.ico")
        self.current_frame: Frame = None
        self.background_img: PhotoImage = PhotoImage(file=path.join(getcwd(),
                                                                    'res/menu_background.png'))
        self.settings: Settings = settings
        self.translation = TranslationTable(language=settings.language)
        self.title(self.translation.get("title"))
        self.show_main_menu()

    def _get_starting_position(self, width: int, height: int) -> str:
        '''
        Returns a geometry string of the tkinter format:
        width x height + startx + starty

        The geometry string is used to determine
        where the window is placed
        and what its size is.
        '''
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        startx = screen_w//2 - width//2
        starty = screen_h//2 - height//2
        return f'{width}x{height}+{startx}+{starty}'

    def _get_size(self, width: int, height: int) -> str:
        '''
        Returns a geometry string of the tkinter format:
        width x height

        The geometry string is used to determine
        what its size is.
        '''
        return f'{width}x{height}'

    def _update_frame(self, frame: MenuFrame) -> None:
        '''Renders the given frame with its according size.'''
        if not self.current_frame:
            self.geometry(self._get_starting_position(width=self.settings.resolution.width,
                                                      height=self.settings.resolution.height))
        if self.current_frame:
            self.current_frame.destroy()
            self.geometry(self._get_size(width=self.settings.resolution.width,
                                         height=self.settings.resolution.height))
        frame.place(x=0, y=0,
                    width=self.settings.resolution.width,
                    height=self.settings.resolution.height)
        self.current_frame = frame
        self.update()

    def show_main_menu(self) -> None:
        '''Renders the main menu.'''
        self._update_frame(MainMenu(window=self))

    def show_settings_menu(self) -> None:
        '''Renders the settings menu.'''
        self._update_frame(SettingsMenu(window=self))

    def show_multiplayer_menu(self) -> None:
        '''Renders the multiplayer menu.'''
        self._update_frame(MultiplayerMenu(window=self))

    def start_singleplayer(self) -> None:
        '''Starts a solo game vs the computer.'''
        singleplayer: GameFrame = GameFrame(window=self, solo=True,
                                            difficulty=self.settings.difficulty)
        singleplayer.new_game()
        self._update_frame(singleplayer)

    def start_local_multiplayer(self) -> None:
        '''Starts a 2 player versus.'''
        multiplayer: GameFrame = GameFrame(window=self, solo=False)
        multiplayer.new_game()
        self._update_frame(multiplayer)

    def host_multiplayer(self) -> None:
        '''Hosts a 2 player versus.'''
        multiplayer: GameFrame = GameFrame(window=self, solo=False,
                                           communication=Communication('127.0.0.1'))
        multiplayer.com.wait_for_connection()
        multiplayer.new_game()
        self._update_frame(multiplayer)

    def join_multiplayer(self, ip: str) -> None:
        '''Joins a 2 player versus.'''
        self.settings.last_ip = ip
        self.settings.save()
        multiplayer: GameFrame = GameFrame(window=self, solo=False,
                                           communication=Communication(ip=ip))
        multiplayer.com.join()
        multiplayer.new_game()
        self._update_frame(multiplayer)
        multiplayer.player_turn = False
        multiplayer.make_move(multiplayer.com.get_move())

    def set_difficulty(self, difficulty: int) -> None:
        '''Changes the difficulty to given value.'''
        self.settings.difficulty = difficulty
        self.settings.save()

    def set_resolution(self, dimension: Dimension) -> None:
        '''Changes the resolution to given value.'''
        self.settings.resolution = dimension
        self.geometry(self._get_starting_position(width=self.settings.resolution.width,
                                                  height=self.settings.resolution.height))
        self.settings.save()

    def set_language(self, language: str) -> None:
        '''Changes the language to given value.'''
        self.settings.language = language
        self.translation.current_language = language
        self.settings.save()

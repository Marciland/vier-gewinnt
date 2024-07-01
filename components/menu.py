'''contains all menu components.'''
from tkinter import Button, Entry

from assets import (Difficulty, Language, MenuFrame, MenuPosition, Resolution,
                    SubMenu, ErrorMessage)


class MainMenu(MenuFrame):
    '''Creates a menu frame for the player to select the game mode.'''

    def __init__(self, window) -> None:
        super().__init__(window=window)
        self._prepare_main_menu()

    def _prepare_main_menu(self) -> None:
        singleplayer = Button(master=self,
                              command=self.window.start_singleplayer)
        singleplayer_text = self.window.translation.get('singleplayer')
        self._configure_menu_button(button=singleplayer,
                                    font=self.font,
                                    text=singleplayer_text

                                    )
        self._place_menu_button(button=singleplayer,
                                position=MenuPosition.TOP)
        multiplayer = Button(master=self,
                             command=self.window.show_multiplayer_menu)
        multiplayer_text = self.window.translation.get('multiplayer')
        self._configure_menu_button(button=multiplayer,
                                    font=self.font,
                                    text=multiplayer_text)
        self._place_menu_button(button=multiplayer,
                                position=MenuPosition.MIDDLE)
        settings = Button(master=self,
                          command=self.window.show_settings_menu)
        settings_text = self.window.translation.get('settings')
        self._configure_menu_button(button=settings,
                                    font=self.font,
                                    text=settings_text)
        self._place_menu_button(button=settings,
                                position=MenuPosition.BOTTOM)
        exit_game = Button(master=self,
                           command=self.window.destroy)
        exit_text = self.window.translation.get('exit')
        self._configure_menu_button(button=exit_game,
                                    font=self.font,
                                    text=exit_text)
        self._place_menu_button(button=exit_game,
                                position=MenuPosition.BACK)


class SettingsMenu(SubMenu):
    '''Creates a menu frame for the player to change settings.'''

    def __init__(self, window) -> None:
        super().__init__(window=window)
        self._prepare_settings_menu()

    def _prepare_settings_menu(self) -> None:
        difficulty = Button(master=self,
                            command=lambda: self.show_sub_menu(DifficultyMenu))
        difficulty_text = self.window.translation.get('difficulty')
        self._configure_menu_button(difficulty,
                                    font=self.font,
                                    text=difficulty_text)
        self._place_menu_button(button=difficulty,
                                position=MenuPosition.TOP)
        resolution = Button(master=self,
                            command=lambda: self.show_sub_menu(ResolutionMenu))
        resolution_text = self.window.translation.get('resolution')
        self._configure_menu_button(resolution,
                                    font=self.font,
                                    text=resolution_text)
        self._place_menu_button(button=resolution,
                                position=MenuPosition.MIDDLE)
        language = Button(master=self,
                          command=lambda: self.show_sub_menu(LanguageMenu))
        language_text = self.window.translation.get('language')
        self._configure_menu_button(language,
                                    font=self.font,
                                    text=language_text)
        self._place_menu_button(button=language,
                                position=MenuPosition.BOTTOM)


class DifficultyMenu(SubMenu):
    '''Shows a sub menu for changing the difficulty.'''

    def __init__(self, window) -> None:
        super().__init__(window=window)
        self.difficulty_buttons: dict[str, Button] = {}
        self._prepare_difficulty_menu()
        self._configure_difficulty_buttons()

    def _prepare_difficulty_menu(self) -> None:
        easy = Button(master=self.window,
                      text=self.window.translation.get('easy'),
                      command=lambda: self._change_difficulty(Difficulty.EASY))
        self.difficulty_buttons.update({Difficulty.EASY.name: easy})
        medium = Button(master=self.window,
                        text=self.window.translation.get('medium_dif'),
                        command=lambda: self._change_difficulty(Difficulty.MEDIUM))
        self.difficulty_buttons.update({Difficulty.MEDIUM.name: medium})
        hard = Button(master=self.window,
                      text=self.window.translation.get('hard'),
                      command=lambda: self._change_difficulty(Difficulty.HARD))
        self.difficulty_buttons.update({Difficulty.HARD.name: hard})
        extreme = Button(master=self.window,
                         text=self.window.translation.get('extreme'),
                         command=lambda: self._change_difficulty(Difficulty.EXTREME))
        self.difficulty_buttons.update({Difficulty.EXTREME.name: extreme})

    def _configure_difficulty_buttons(self) -> None:
        for index, button in enumerate(list(self.difficulty_buttons.values())):
            self._configure_menu_button(button=button,
                                        font=self.small_font,
                                        text=button['text'])
            if index % 2 == 0:
                top = 0 if index == 0 else 1
                button.place(x=self.button_margin_x,
                             y=(top + 1) * self.button_margin_y +
                             top * self.button_height,
                             width=self.button_width//2,
                             height=self.button_height)
            else:
                top = 0 if index == 1 else 1
                button.place(x=self.button_margin_x+self.button_width//2,
                             y=(top + 1) * self.button_margin_y +
                             top * self.button_height,
                             width=self.button_width//2,
                             height=self.button_height)
        self._set_difficulty_button()

    def _change_difficulty(self, difficulty: Difficulty) -> None:
        self.window.set_difficulty(difficulty.value)
        for _difficulty, button in self.difficulty_buttons.items():
            if _difficulty == difficulty.name:
                button.configure(state='disabled')
            else:
                button.configure(state='active')

    def _set_difficulty_button(self):
        match self.window.settings.difficulty:
            case Difficulty.EASY.value:
                self._change_difficulty(Difficulty.EASY)
            case Difficulty.MEDIUM.value:
                self._change_difficulty(Difficulty.MEDIUM)
            case Difficulty.HARD.value:
                self._change_difficulty(Difficulty.HARD)
            case Difficulty.EXTREME.value:
                self._change_difficulty(Difficulty.EXTREME)


class ResolutionMenu(SubMenu):
    '''Shows a sub menu for changing the resolution.'''

    def __init__(self, window) -> None:
        super().__init__(window=window)
        self.resolution_buttons: dict[str, Button] = {}
        self._prepare_resolution_menu()
        self._set_resolution_button()

    def _prepare_resolution_menu(self) -> None:
        small = Button(master=self.window,
                       command=lambda: self._change_resolution(Resolution.SMALL))
        small_text = self.window.translation.get('small_res')
        self._configure_menu_button(button=small,
                                    font=self.font,
                                    text=small_text)
        self._place_menu_button(button=small,
                                position=MenuPosition.TOP)
        self.resolution_buttons.update({Resolution.SMALL.name: small})
        medium = Button(master=self.window,
                        command=lambda: self._change_resolution(Resolution.MEDIUM))
        medium_text = self.window.translation.get('medium_res')
        self._configure_menu_button(button=medium,
                                    font=self.font,
                                    text=medium_text)
        self._place_menu_button(button=medium,
                                position=MenuPosition.MIDDLE)
        self.resolution_buttons.update({Resolution.MEDIUM.name: medium})

    def _change_resolution(self, resolution: Resolution) -> None:
        self.window.set_resolution(resolution.value)
        self.window.show_settings_menu()
        # call the "next" frame as self will be destroyed when changing resolutions
        self.window.current_frame.show_sub_menu(ResolutionMenu)

    def _set_resolution_button(self):
        match self.window.settings.resolution:
            case Resolution.SMALL.value:
                self._toggle_resolution_button(Resolution.SMALL)
            case Resolution.MEDIUM.value:
                self._toggle_resolution_button(Resolution.MEDIUM)

    def _toggle_resolution_button(self, resolution: Resolution):
        for _resolution, button in self.resolution_buttons.items():
            if _resolution == resolution.name:
                button.configure(state='disabled')
            else:
                button.configure(state='active')


class LanguageMenu(SubMenu):
    '''Shows a sub menu for changing the language.'''

    def __init__(self, window) -> None:
        super().__init__(window=window)
        self.language_buttons: dict[str, Button] = {}
        self._prepare_language_menu()
        self._set_language_button()

    def _prepare_language_menu(self) -> None:
        english = Button(master=self.window,
                         command=lambda: self._change_language(Language.ENGLISH))
        english_text = self.window.translation.get('english')
        self._configure_menu_button(button=english,
                                    font=self.font,
                                    text=english_text)
        self._place_menu_button(button=english,
                                position=MenuPosition.TOP)
        self.language_buttons.update({Language.ENGLISH.value: english})
        german = Button(master=self.window,
                        command=lambda: self._change_language(Language.GERMAN))
        german_text = self.window.translation.get('german')
        self._configure_menu_button(button=german,
                                    font=self.font,
                                    text=german_text)
        self._place_menu_button(button=german,
                                position=MenuPosition.MIDDLE)
        self.language_buttons.update({Language.GERMAN.value: german})

    def _change_language(self, language: Language) -> None:
        self.window.set_language(language.value)
        self.window.title(self.window.translation.get("title"))
        for _language, button in self.language_buttons.items():
            if _language == language.value:
                button.configure(state='disabled')
            else:
                button.configure(state='active')

    def _set_language_button(self):
        match self.window.settings.language:
            case Language.ENGLISH.value:
                self._change_language(Language.ENGLISH)
            case Language.GERMAN.value:
                self._change_language(Language.GERMAN)


class MultiplayerMenu(SubMenu):
    '''
    Submenu for selecting the multiplayer mode.
    Choose from:
        - local
        - online
        - online "bot fight"
    '''

    def __init__(self, window) -> None:
        super().__init__(window=window)
        self._prepare_multiplayer_menu()

    def _prepare_multiplayer_menu(self) -> None:
        local = Button(master=self,
                       command=self.window.start_local_multiplayer)
        local_text = self.window.translation.get('multiplayer_local')
        self._configure_menu_button(button=local,
                                    font=self.font,
                                    text=local_text)
        self._place_menu_button(button=local,
                                position=MenuPosition.TOP)
        online = Button(master=self,
                        command=lambda: self.show_sub_menu(MultiplayerSubMenu, False))
        online_text = self.window.translation.get('multiplayer_online')
        self._configure_menu_button(button=online,
                                    font=self.font,
                                    text=online_text)
        self._place_menu_button(button=online,
                                position=MenuPosition.MIDDLE)
        online_ai = Button(master=self,
                           command=lambda: self.show_sub_menu(MultiplayerSubMenu, True))
        online_ai_text = self.window.translation.get('multiplayer_online_ai')
        self._configure_menu_button(button=online_ai,
                                    font=self.font,
                                    text=online_ai_text)
        self._place_menu_button(button=online_ai,
                                position=MenuPosition.BOTTOM)


class MultiplayerSubMenu(SubMenu):
    '''Submenu for selecting the multiplayer mode.'''

    def __init__(self, window, bot_war: bool) -> None:
        super().__init__(window=window)
        self.bot_war = bot_war
        self.validation = self.register(self._validate_entry)
        self._prepare_multiplayer_sub_menu()

    def _validate_entry(self, what) -> bool:
        valid_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
        for char in list(what):
            if char not in valid_chars:
                return False
        return True

    def _ip_valid(self, ip: str) -> bool:
        return len([i for i in ip.split('.') if i]) == 4 \
            and ip.count('.') == 3 \
            and len(ip) >= 7

    def _join_multiplayer(self, ip: str) -> None:
        if self._ip_valid(ip):
            self.window.join_multiplayer(ip)
        else:
            title = self.window.translation.get('bad_ip_title')
            msg = self.window.translation.get('bad_ip_msg')
            ErrorMessage(frame=self, title=title, msg=msg)

    def _prepare_multiplayer_sub_menu(self) -> None:
        host = Button(master=self.window,
                      command=self.window.host_multiplayer)
        host_text = self.window.translation.get('multiplayer_host')
        self._configure_menu_button(button=host,
                                    font=self.font,
                                    text=host_text)
        self._place_menu_button(button=host,
                                position=MenuPosition.TOP)
        ip = Entry(master=self.window, justify='center',
                   validate='all',
                   validatecommand=(self.validation, '%S'))
        ip.configure(font=self.small_font,
                     background='pale turquoise')
        ip.insert(0, self.window.settings.last_ip)
        ip.place(x=self.button_margin_x,
                 y=(MenuPosition.BOTTOM.value+1) * self.button_margin_y +
                 MenuPosition.MIDDLE.value * self.button_height +
                 self.button_margin_y*3//4,
                 width=self.button_width,
                 height=self.button_height//2)
        join = Button(master=self.window,
                      command=lambda: self._join_multiplayer(ip.get()))
        join_text = self.window.translation.get('multiplayer_join')
        self._configure_menu_button(button=join,
                                    font=self.font,
                                    text=join_text)
        self._place_menu_button(button=join,
                                position=MenuPosition.BOTTOM)

'''base classes to inherit from.'''
from tkinter import Button, Frame, Label
from tkinter.font import Font
from typing import TYPE_CHECKING

from .dataclasses import MenuPosition, Resolution

if TYPE_CHECKING:
    from components import MainWindow


class MenuFrame(Frame):
    '''Frame extension for the game's menu.'''

    def __init__(self, window) -> None:
        super().__init__(master=window)
        self.window: MainWindow = window
        match self.window.settings.resolution:
            case Resolution.SMALL.value:
                self.font: Font = Font(family='Cooper Black',
                                       size=27)
                self.small_font: Font = Font(family='Cooper Black',
                                             size=21)
                self.background_img = self.window.background_img.subsample(7)
            case Resolution.MEDIUM.value:
                self.font: Font = Font(family='Cooper Black',
                                       size=37)
                self.small_font: Font = Font(family='Cooper Black',
                                             size=31)
                self.background_img = self.window.background_img.subsample(5)
        self.button_height = self.window.settings.resolution.height // 7
        self.button_width = self.window.settings.resolution.width * 4 // 7
        self.button_margin_y = self.button_height // 2
        self.button_margin_x = self.window.settings.resolution.width // 4.6
        self._prepare_menu()

    def _prepare_menu(self) -> None:
        self.background = Label(master=self,
                                name='background',
                                image=self.background_img)
        self.background.place(x=0, y=0,
                              width=self.window.settings.resolution.width,
                              height=self.window.settings.resolution.height)

    def _configure_menu_button(self, button: Button, font: Font, text: str) -> None:
        button.configure(font=font,
                         text=text,
                         background='pale turquoise',
                         activebackground='pale turquoise')
        button.lift(self.background)

    def _place_menu_button(self, button: Button, position: MenuPosition) -> None:
        button.place(x=self.button_margin_x,
                     y=(position.value+1) * self.button_margin_y +
                     position.value * self.button_height,
                     width=self.button_width,
                     height=self.button_height)


class SubMenu(MenuFrame):
    '''Any SubMenu.'''

    def __init__(self, window) -> None:
        super().__init__(window=window)
        self._prepare_sub_menu()

    def _enter_sub_menu(self) -> None:
        for child in self.winfo_children():
            if child.winfo_name() in ['back', 'background']:
                continue
            child.place_forget()

    def _enter_settings_sub_menu(self) -> None:
        for child in self.winfo_children():
            if child.winfo_name() == 'back':
                child.configure(text=self.window.translation.get('save'))
                break

    def _prepare_sub_menu(self) -> None:
        back = Button(master=self,
                      name='back',
                      command=self.window.show_main_menu)
        back_text = self.window.translation.get('back')
        self._configure_menu_button(button=back,
                                    font=self.font,
                                    text=back_text)
        self._place_menu_button(button=back, position=MenuPosition.BACK)

    def show_sub_menu(self, sub_menu: 'SubMenu', args=None) -> None:
        '''needs to be called from different frame, thus not prefixed with _'''
        self._enter_sub_menu()
        if args is None:
            self._enter_settings_sub_menu()
            return sub_menu(window=self.window)
        return sub_menu(self.window, args)

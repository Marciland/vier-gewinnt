'''Contains the games that can be played.'''
from time import perf_counter
from tkinter import Frame
from typing import TYPE_CHECKING

from assets import Cell, EndMessage
from helper import board_helper as BoardHelper
from helper import bot_helper as BotHelper

from .board import Board

if TYPE_CHECKING:
    from components import MainWindow


class GameFrame(Frame):
    '''Provides a game frame with a connect four board.'''

    def __init__(self, window) -> None:
        super().__init__(master=window)
        self.board: Board = None
        self.solo = True
        self.difficulty = 0
        self.window: MainWindow = window
        self.current_player = 1

    def new_game(self) -> None:
        '''Sets up a new game.'''
        self.current_player = 1
        self.board = Board(frame=self)
        for index, entry_point in self.board.entry_points.items():
            entry_point.widget.configure(state='normal')
            entry_point.widget.configure(command=lambda i=index:
                                         self._make_move(i))
            entry_point.widget.bind("<Enter>", lambda _, entry=entry_point:
                                    entry.change_state(self.current_player))
            entry_point.widget.bind("<Leave>", lambda _, entry=entry_point:
                                    entry.change_state(-1))

    def _drop_coin(self, cells: list[Cell]) -> bool:
        for cell in cells:
            if cell.is_empty():
                cell.change_state(self.current_player)
                return True
        return False

    def _get_next_player(self) -> int:
        '''
        Depending on current player, the next current player is defined.
        0 = bot
        1 = player1
        2 = player2
        '''
        if self.current_player in [0, 2]:
            return 1
        if self.solo:
            return 0
        return 2

    def _make_move(self, col_index: int) -> None:
        affected_cells = BoardHelper.get_cells_in_col(self.board.cells,
                                                      col_index)
        # start at the bottom of the board
        affected_cells.reverse()
        if not self._drop_coin(affected_cells):
            # skip win conditions if nothing happened, also do not swap current player!
            return None
        self.board.entry_points[col_index].change_state(-1)
        if BoardHelper.board_is_full(self.board.cells):
            return self._end_game(remis=True)
        if BoardHelper.has_connected_four(board_cells=self.board.cells,
                                          cols=self.board.cols,
                                          rows=self.board.rows):
            return self._end_game(remis=False)
        self.current_player = self._get_next_player()
        if self.current_player == 0:
            start = perf_counter()
            possible_moves = self.board.get_possible_moves()
            move = BotHelper.calculate_next_move(difficulty=self.difficulty,
                                                 board=self.board,
                                                 possible_moves=possible_moves)
            print('Computer move calculated in:', perf_counter()-start)
            return self._make_move(move)
        return None

    def _end_game(self, remis: bool) -> None:
        '''Stops interactivity and asks for a new game.'''
        for _, entry_point in self.board.entry_points.items():
            entry_point.widget.configure(state='disabled')
            entry_point.widget.unbind("<Enter>")
            entry_point.widget.unbind("<Leave>")
        title = self.window.translation.get('end_title')
        end_message = EndMessage(frame=self,
                                 title=title,
                                 remis=remis)
        if end_message.replay:
            self.new_game()
        else:
            self.window.show_main_menu()

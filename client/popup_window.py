import pygame
from constants import *
from position import Position


class PopupWindow:
    def __init__(self, surface):
        self.surface = surface

    # def display_server_disconnected():
    #     Tk().wm_withdraw()
    #     messagebox.showerror('Server Error', 'A server error has occured.')

    # def display_user_connecting():
    #     Tk().wm_withdraw()
    #     messagebox.showinfo('', 'Waiting for the user to connect.')

    # def close_window():
    #     Tk().root.destroy()

    def display(self):
        FONT = pygame.font.Font(None, 32)
        popup_window_size = Position(350, 250)
        window_text = ["Waiting for the opponent", "to connect"]
        window_name = []
        window_coordinates = []

        for line in window_text:
            window_line = FONT.render(line, True, (0, 0, 0))
            window_name.append(window_line)
            window_coordinates.append(window_line.get_rect())

        popup_window_coordinates = Position(WINDOW_SIZE / 2 - popup_window_size.x / 2,
                                            WINDOW_SIZE / 2 - popup_window_size.y / 2)

        window_size = pygame.Rect(popup_window_coordinates.x, popup_window_coordinates.y,
                                  popup_window_size.x, popup_window_size.y)

        pygame.draw.rect(self.surface, (255, 255, 255), window_size, border_radius =15)

        for i, line in enumerate(window_name):
            window_coordinates[i].center = (WINDOW_SIZE / 2,
                                            WINDOW_SIZE / 2 + (i - 2) * 28 + 40)
            self.surface.blit(line, window_coordinates[i])

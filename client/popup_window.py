from tkinter import *
from tkinter import messagebox


class PopupWindow:
    def display_server_disconnected():
        # # window_name = FONT.render(window_name, True, BLACK)
        # # window_coordinates = window_name.get_rect()
        # window_coordinates.center = (self.window_X, self.window_Y)
        # window_size = pygame.Rect(self.X, self.Y, self.window_width, self.window_height)
        # pygame.draw.rect(SCREEN, WINDOWS_COLOR, window_size)
        # return SCREEN.blit(window_name, window_coordinates)

        Tk().wm_withdraw()
        messagebox.showerror('Server Error', 'A server error has occured.')
        # B = Tkinter.Button(top, text ="Hello", command = helloCallBack)

import os
import pygame
import sys
import win32api
import win32con
import win32gui
import imgui
from imgui.integrations.pygame import PygameRenderer
from OpenGL.GL import *

fuchsia = (255, 0, 255)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)


def get_window():
    hwnd = win32gui.FindWindow(None, "Blitz")
    windowrect = win32gui.GetWindowRect(hwnd)
    x = windowrect[0]
    y = windowrect[1]
    width = windowrect[2] - x
    height = windowrect[3] - y
    return x , y, width, height


class Gui:

    def __init__(self):
        self.screen = None

    def update(self):
        global is_gui_visible
        pygame.init()
        inf = get_window()
        hwnd = pygame.display.get_wm_info()["window"]
        exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        exstyle |= win32con.WS_EX_LAYERED
        exstyle |= win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, exstyle)

        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               exstyle | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

        self.screen = pygame.display.set_mode((inf[2], inf[3]), pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(':D')
        imgui.create_context()
        impl = PygameRenderer()

        io = imgui.get_io()
        io.display_size = inf[2], inf[3]

        while True:

            win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], -1, get_window()[0], get_window()[1], 0,
                                  0,
                                  0x0001)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                impl.process_event(event)

            if is_gui_visible:
                win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], -1, get_window()[0], get_window()[1], 0,
                                      0,
                                      0x0001)
                imgui.new_frame()
                imgui.style_colors_classic()
                if imgui.begin_main_menu_bar():
                    if imgui.begin_menu("trtrrrtrtrt", True):

                        clicked_quit, selected_quit = imgui.menu_item(
                            "Destroy!", 'turning off cheat', False, True
                        )

                        if clicked_quit:
                            exit(1)
                        imgui.end_menu()

                    imgui.end_main_menu_bar()
                imgui.show_test_window()

                imgui.begin("Visuals", True)
                imgui.end()

                glClearColor(1, 0, 1, 1)
                glClear(GL_COLOR_BUFFER_BIT)
                imgui.render()
                impl.render(imgui.get_draw_data())

                pygame.display.flip()


Gui().update()

import os
import pygame

# Colors
black = (0,0,0)
white = (255,255,255)
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)
grey  = (127,127,127)

windows = {}
deffont = {}
defprop = {}

defprop['type']    = 'blank'  # window type
defprop['BG']      = black    # background color
defprop['FG']      = white    # foreground color
defprop['dis_FG']  = grey     # foreground color if disabled
defprop['inset']   = 10       # border-inset, if any
defprop['a-thick'] = 9        # border thickness, if active
defprop['n-thin']  = 3        # border thickness, if not
defprop['line']    = 5        # general line thickness
defprop['size']    = 24       # font size
defprop['Label']   = '(none)' # label, if any
defprop['flags']   = 0        # flags, as follows:
# 0x01 - whether the window/button is visible
# 0x02 - whether the window/button has a border
# 0x04 - whether the window/button is enabled
# 0x08 - whether the window/button is active
# 0x10 - whether the window/button has a submenu
# 0x20 - whether the window/button is blank (if visible, but regardless of type)

def get_font(size):
    if size not in deffont:
        deffont[size] = pygame.font.Font(None, size)
    return deffont[size]

def get_property(win_id, property):
    value = None
    if win_id in windows:
        W = windows[win_id]
        if property in W:
            value = W[property]
        elif property in defprop:
            value = defprop[property]
    return value

def ui_set_property(win_id, property, value):
    if win_id not in windows:
        windows[win_id] = {}
    W = windows[win_id]
    W[property] = value

def draw_border(win_id, bbox, flags):
    if flags & 0x04: # enabled
        FG = get_property(win_id, 'FG')
        if flags & 0x08: # active
            thickness = get_property(win_id, 'a-thick')
        else: # inactive
            thickness = get_property(win_id, 'n-thin')
    else: # disabled
        FG = get_property(win_id, 'dis_FG')
        thickness = get_property(win_id, 'n-thin')
    d = get_property(win_id, 'inset')
    (x, y, w, h) = bbox
    pygame.draw.rect(screen, FG, (x+d, y+d, w-2*d, h-2*d), thickness)

def draw_back(win_id, bbox, flags):
    thickness = get_property(win_id, 'line')
    FG = get_property(win_id, 'FG')

def draw_exit(win_id, bbox, flags):
    thickness = get_property(win_id, 'line')
    FG = get_property(win_id, 'FG')

def draw_up(win_id, bbox, flags):
    thickness = get_property(win_id, 'line')
    FG = get_property(win_id, 'FG')

def draw_down(win_id, bbox, flags):
    thickness = get_property(win_id, 'line')
    FG = get_property(win_id, 'FG')

def draw_scroll(win_id, bbox, flags):
    None

def draw_menu_item(win_id, bbox, flags):
    d    = get_property(win_id, 'inset')
    FG   = get_property(win_id, 'FG')
    text = get_property(win_id, 'Label')
    size = get_property(win_id, 'size')
    font = get_font(size)
    label = font.render(str(text), 1, (FG))
    (x, y, w, h) = bbox
    screen.blit(label, (x+2*d,y+2*d))
    if flags & 0x10: # we have a submenu
        thickness = get_property(win_id, 'line')
        xl = x + w - 6*d
        yt = y + 2*d
        y0 = y + h/2
        xr = x + w - 2*d
        yb = y + h - 2*d
        pygame.draw.lines(screen, FG, True, [(xl,yt), (xl,yb), (xr,y0)], thickness)

def ui_win_draw(win_id):
    flags = get_property(win_id, 'flags')
    if flags & 0x01: # visible
        bbox = get_property(win_id, 'bbox')
        BG   = get_property(win_id, 'BG')
        pygame.draw.rect(screen, BG, bbox, 0) # 0-thickness = fill
    if (flags & 0x21) == 0x01: # visible, but not blank
        if flags & 0x02: # there's a border
            draw_border(win_id, bbox, flags)
        type = get_property(win_id, 'type')
        if type == 'Back':
            draw_back(win_id, bbox, flags)
        elif type == 'Exit':
            draw_exit(win_id, bbox, flags)
        elif type == 'Up':
            draw_up(win_id, bbox, flags)
        elif type == 'Down':
            draw_down(win_id, bbox, flags)
        elif type == 'Scroll':
            draw_scroll(win_id, bbox, flags)
        elif type == 'Menu Item':
            draw_menu_item(win_id, bbox, flags)

# Element Types
# 0 - blank
# 1 - Back
# 2 - Exit
# 3 - Up
# 4 - Down
# 5 - Scroll
# 6 - Menu Item

def ui_redraw(bbox, element_type, flags, opt_arg):
    bBorders = flags &  1
    bActive  = flags &  2
    bEnabled = flags &  4
    bSubMenu = flags &  8
    bVisible = flags & 16
    pygame.draw.rect(screen, black, bbox, 0) # 0-thickness = fill
    if bVisible:
        (x, y, w, h) = bbox
        d = h / 10
        if w < h:
            d = w / 10
        if d < 5:
            d = 5
        if bBorders:
            color = grey
            if bEnabled:
                color = white
            thickness = 3
            if bActive:
                thickness = 9
            pygame.draw.rect(screen, color, (x+d, y+d, w-2*d, h-2*d), thickness)
        thickness = 5
        if element_type == 1:
            bboxi = (x+3*d, y+3*d, w-6*d, h-6*d)
            pygame.draw.arc(screen, color, bboxi, 0,    3.14, thickness)
            pygame.draw.arc(screen, color, bboxi, 4.71, 6.28, thickness)
            xarr = x+3*d
            yarr = y+h/2
            pygame.draw.lines(screen, color, True, [(xarr-d,yarr), (xarr+d,yarr), (xarr,yarr+d)], thickness)
        elif element_type == 2:
            bboxi = (x+3*d, y+3*d, w-6*d, h-6*d)
            pygame.draw.arc(screen, color, bboxi, 0,    1.22, thickness)
            pygame.draw.arc(screen, color, bboxi, 1.92, 6.28, thickness)
            pygame.draw.lines(screen, color, False, [(x+w/2,y+h/2), (x+w/2,y+2*d)], thickness)
        elif element_type == 3:
            xl = x + 3*d
            yt = y + 3*d
            x0 = x + w/2
            xr = x + w - 6*d
            yb = y + h - 6*d
            pygame.draw.lines(screen, color, True, [(xl,yb), (x0,yt), (xr,yb)], thickness)
        elif element_type == 4:
            xl = x + 3*d
            yt = y + 3*d
            x0 = x + w/2
            xr = x + w - 6*d
            yb = y + h - 6*d
            pygame.draw.lines(screen, color, True, [(xl,yt), (x0,yb), (xr,yt)], thickness)
        elif element_type == 5:
            bboxi = (x+d, y, w-2*d, h)
            pygame.draw.rect(screen, grey, bboxi, 0)
            if opt_arg:
                (s_min, s_max) = opt_arg
                bboxi = (x+2*d, y+(h*s_min)/100, w-4*d, (h*(s_max-s_min))/100)
                pygame.draw.rect(screen, blue, bboxi, 0)
        elif element_type == 6:
            if opt_arg:
                font  = pygame.font.Font(None, h-3*d)
                label = font.render(str(opt_arg), 1, (color))
                screen.blit(label, (x+2*d,y+2*d))
            if bSubMenu:
                xl = x + w - 6*d
                yt = y + 2*d
                y0 = y + h/2
                xr = x + w - 2*d
                yb = y + h - 2*d
                pygame.draw.lines(screen, color, True, [(xl,yt), (xl,yb), (xr,y0)], thickness)
        else:
            None


def ui_refresh():
    pygame.display.update()

def ui_init(driver, device, screen_w, screen_h):
    os.environ["SDL_VIDEODRIVER"] = driver
    os.environ["SDL_FBDEV"] = device
    pygame.init()
    pygame.display.init()
    pygame.mouse.set_visible(0)
    pygame.font.init()
    global screen
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
    screen.fill(red)
    pygame.display.update()

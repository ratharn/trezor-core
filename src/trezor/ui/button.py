from micropython import const

from trezor import io
from trezor import ui

from trezor.ui import display
from trezor.ui import contains
from trezor.ui import rotate
from trezor.ui import Widget


DEFAULT_BUTTON = {
    'bg-color': ui.C_KEY_BTN,
    'fg-color': ui.C_FONT,
    'text-style': ui.NORMAL,
    'border-color': ui.C_SCREEN_BG,
    'radius': ui.BTN_RADIUS,
}
DEFAULT_BUTTON_ACTIVE = {
    'bg-color': ui.C_KEY_BTN_DIS,
    'fg-color': ui.C_FONT,
    'text-style': ui.NORMAL,
    'border-color': ui.C_SCREEN_BG,
    'radius': ui.BTN_RADIUS,
}
DEFAULT_BUTTON_DISABLED = {
    'bg-color': ui.C_KEY_BTN_DIS,
    'fg-color': ui.C_FONT_DIS,
    'text-style': ui.NORMAL,
    'border-color': ui.C_KEY_BTN_DIS,
    'radius': ui.BTN_RADIUS,
}

CANCEL_BUTTON = {
    'bg-color': ui.C_CANCEL_BTN,
    'fg-color': ui.C_FONT,
    'text-style': ui.BOLD,
    'border-color': ui.C_SCREEN_BG,
    'radius': ui.BTN_RADIUS,
}
CANCEL_BUTTON_ACTIVE = {
    'bg-color': ui.C_CANCEL_BTN_DIS,
    'fg-color': ui.C_FONT_DIS,
    'text-style': ui.BOLD,
    'border-color': ui.C_SCREEN_BG,
    'radius': ui.BTN_RADIUS,
}

CONFIRM_BUTTON = {
    'bg-color': ui.C_CONFIRM_BTN,
    'fg-color': ui.C_FONT,
    'text-style': ui.BOLD,
    'border-color': ui.C_SCREEN_BG,
    'radius': ui.BTN_RADIUS,
}
CONFIRM_BUTTON_ACTIVE = {
    'bg-color': ui.C_CONFIRM_BTN_DIS,
    'fg-color': ui.C_FONT_DIS,
    'text-style': ui.BOLD,
    'border-color': ui.C_SCREEN_BG,
    'radius': ui.BTN_RADIUS,
}

CLEAR_BUTTON = {
    'bg-color': ui.C_CLEAN_BTN,
    'fg-color': ui.C_FONT,
    'text-style': ui.NORMAL,
    'border-color': ui.C_CLEAN_BTN,
    'radius': ui.BTN_RADIUS,
}
CLEAR_BUTTON_ACTIVE = {
    'bg-color': ui.C_CLEAN_BTN_DIS,
    'fg-color': ui.C_FONT_DIS,
    'text-style': ui.NORMAL,
    'border-color': ui.C_CLEAN_BTN_DIS,
    'radius': ui.BTN_RADIUS,
}


BTN_CLICKED = const(1)

BTN_STARTED = const(1)
BTN_ACTIVE = const(2)
BTN_DIRTY = const(4)
BTN_DISABLED = const(8)


class Button(Widget):

    def __init__(self, area, content,
                 normal_style=None,
                 active_style=None,
                 disabled_style=None,
                 absolute=False):
        self.area = area
        self.content = content
        self.normal_style = normal_style or DEFAULT_BUTTON
        self.active_style = active_style or DEFAULT_BUTTON_ACTIVE
        self.disabled_style = disabled_style or DEFAULT_BUTTON_DISABLED
        self.absolute = absolute
        self.state = BTN_DIRTY

    def enable(self):
        self.state &= ~BTN_DISABLED
        self.state |= BTN_DIRTY

    def disable(self):
        self.state |= BTN_DISABLED | BTN_DIRTY

    def taint(self):
        self.state |= BTN_DIRTY

    def render(self):
        if not self.state & BTN_DIRTY:
            return
        state = self.state & ~BTN_DIRTY
        if state & BTN_DISABLED:
            style = self.disabled_style
        elif state & BTN_ACTIVE:
            style = self.active_style
        else:
            style = self.normal_style
        ax, ay, aw, ah = self.area
        tx = ax + aw // 2
        ty = ay + ah // 2 + 8
        display.bar_radius(ax, ay, aw, ah,
                           style['border-color'],
                           ui.C_SCREEN_BG,
                           style['radius'])
        display.bar_radius(ax + 3, ay + 3, aw - 6, ah - 6,
                           style['bg-color'],
                           style['border-color'],
                           style['radius'])

        if isinstance(self.content, str):
            display.text_center(tx, ty, self.content,
                                style['text-style'],
                                style['fg-color'],
                                style['bg-color'])

        else:
            display.icon(tx - 15, ty - 20, self.content,
                         style['fg-color'],
                         style['bg-color'])

        self.state = state

    def touch(self, event, pos):
        if self.state & BTN_DISABLED:
            return
        if not self.absolute:
            pos = rotate(pos)
        if event == io.TOUCH_START:
            if contains(pos, self.area):
                self.state = BTN_STARTED | BTN_DIRTY | BTN_ACTIVE
        elif event == io.TOUCH_MOVE and self.state & BTN_STARTED:
            if contains(pos, self.area):
                if not self.state & BTN_ACTIVE:
                    self.state = BTN_STARTED | BTN_DIRTY | BTN_ACTIVE
            else:
                if self.state & BTN_ACTIVE:
                    self.state = BTN_STARTED | BTN_DIRTY
        elif event == io.TOUCH_END and self.state & BTN_STARTED:
            self.state = BTN_DIRTY
            if contains(pos, self.area):
                return BTN_CLICKED

from trezor import ui, loop, res, io
from trezor.utils import unimport


def display_homescreen_lock(unlocked):
    if unlocked:
        image = res.load('trezor/res/unlock-home3.toif')
        ui.display.image(0, 0, image)
    else:
        image = res.load('trezor/res/lock-home3.toif')
        ui.display.image(0, 0, image)


class NullContext:

    async def call(self, msg, types):
        pass


@unimport
async def layout_homescreen():
    from apps.common.request_pin import request_pin

    ctx = NullContext()
    touch = loop.select(io.TOUCH)
    unlocked = False

    while True:
        display_homescreen_lock(unlocked)
        await touch
        await request_pin(ctx)
        unlocked = True


@unimport
async def layout_signtx_preview(ctx, msg):
    from trezor.ui.scroll import paginate
    await paginate(page_signtx_preview, 3)


async def page_signtx_preview(page, page_count):
    from trezor.ui.button import Button, CONFIRM_BUTTON, CONFIRM_BUTTON_ACTIVE
    from trezor.ui.scroll import render_scrollbar, animate_swipe
    from trezor.ui.text import Text
    from apps.common.confirm import hold_to_confirm
    ui.display.bar(0, 0, 240, 240, ui.C_SCREEN_BG)

    content = Text('Sign transaction', ui.ICON_RESET)
    content.render()
    render_scrollbar(page, page_count)

    if page + 1 == page_count:
        await hold_to_confirm(NullContext(), content)
    else:
        await animate_swipe()

from trezor import ui, loop, res, io
from trezor.utils import unimport


def display_homescreen_lock(unlocked):
    image = res.load('apps/homescreen/res/trezor_logo.toig')
    ui.display.icon(0, 0, image, ui.WHITE, ui.BLACK)
    if unlocked:
        label = 'My TREZOR (Unlocked)'
    else:
        label = 'My TREZOR (Locked)'
    ui.display.text_center(120, 210, label, ui.BOLD, ui.WHITE, ui.BLACK)


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

    ui.display.clear()

    content = Text('Sign transaction', ui.ICON_RESET)
    content.render()
    render_scrollbar(page, page_count)

    if page + 1 == page_count:
        await hold_to_confirm(NullContext(), content)
    else:
        await animate_swipe()

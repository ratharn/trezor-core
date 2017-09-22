from trezor import ui, loop, res, io
from trezor.utils import unimport


def display_homescreen_lock(unlocked):
    if unlocked:
        image = res.load('trezor/res/unlock-home4.toif')
        ui.display.image(0, 0, image)
    else:
        image = res.load('trezor/res/lock-home4.toif')
        ui.display.image(0, 0, image)


class NullContext:

    async def call(self, msg, types):
        pass


async def click():
    touching = False
    while True:
        if touching:
            ev, *pos = await loop.select(io.TOUCH)
            if ev == io.TOUCH_END:
                return
        else:
            ev, *pos = await loop.select(io.TOUCH)
            if ev == io.TOUCH_START:
                touching = True


@unimport
async def layout_homescreen():
    from apps.common.request_pin import request_pin

    ctx = NullContext()
    unlocked = False

    while True:
        display_homescreen_lock(unlocked)
        await click()
        await request_pin(ctx)
        unlocked = True
        display_homescreen_lock(unlocked)
        await click()
        await layout_signtx_preview(ctx, None)


@unimport
async def layout_signtx_preview(ctx, msg):
    from trezor.ui.scroll import paginate
    await paginate(page_signtx_preview, 2)


async def page_signtx_preview(page, page_count):
    from trezor.ui.button import Button, CONFIRM_BUTTON, CONFIRM_BUTTON_ACTIVE
    from trezor.ui.scroll import render_scrollbar, animate_swipe
    from trezor.ui.text import Text
    from apps.common.confirm import hold_to_confirm
    ui.display.bar(0, 0, 240, 240, ui.C_SCREEN_BG)

    content = Text('Send', ui.ICON_RESET, ui.MONO, '0.1337 BTC', ui.NORMAL, ui.C_FONT_DIS, 'to address', ui.MONO, ui.C_FONT, '1BGuTrv4FovfosXih', 'Cc2yUcQv5mPi3ewnv')
    content.render()
    render_scrollbar(page, page_count)

    if page + 1 == page_count:
        content = Text('Confirm sending', ui.ICON_RESET, ui.MONO, '0.1337 BTC', ui.NORMAL, ui.C_FONT_DIS, 'with fee',
                       ui.MONO, ui.C_FONT, '0.0001 BTC')
        await hold_to_confirm(NullContext(), content)
    else:
        await animate_swipe()

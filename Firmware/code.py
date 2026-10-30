import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.macros import Macros, Press, Release, Tap

keyboard = KMKKeyboard()

macros = Macros()
encoder_handler = EncoderHandler()
keyboard.modules = [macros, encoder_handler]

keyboard.col_pins = (board.D1, board.D2, board.D3, board.D6, board.D7)
keyboard.row_pins = (board.D0,)
keyboard.diode_orientation = type(keyboard).DIODE_COL2ROW

encoder_handler.pins = ((board.D8, board.D9, board.D10, False),)

OPEN_ANIKOTO = KC.MACRO(
    Press(KC.LGUI), Tap(KC.R), Release(KC.LGUI),
    KC.MACRO_SLEEP_MS(200),
    "https://anikoto.com\n"
)

keyboard.keymap = [
    [
        OPEN_ANIKOTO,
        KC.LSFT(KC.R),
        KC.MEDIA_PLAY_PAUSE,
        KC.L,
        KC.C
    ]
]

encoder_handler.map = [
    ((KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN, KC.AUDIO_MUTE),)
]

displayio.release_displays()

i2c = busio.I2C(board.SCL, board.SDA)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

try:
    text_area = label.Label(terminalio.FONT, text="GEAR 5", color=0xFFFFFF, x=45, y=15)
    group = displayio.Group()
    group.append(text_area)
    display.root_group = group
except Exception as e:
    pass

if __name__ == '__main__':
    keyboard.go()
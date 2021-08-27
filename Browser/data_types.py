from enum import Enum, auto


class SupportedBrowsers(Enum):
    """定义应启动哪个浏览器。
    """

    chromium = auto()
    firefox = auto()
    webkit = auto()

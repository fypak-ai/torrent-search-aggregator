from .yts import YTSSource
from .nyaa import NyaaSource
from .eztv import EZTVSource
from .x1337 import X1337Source
from .tpb import TPBSource
from .rarbg import RARBGSource
from .torrentgalaxy import TorrentGalaxySource
from .kickass import KickassSource
from .limetorrents import LimeTorrentsSource


def get_all_sources():
    return [
        YTSSource(),
        NyaaSource(),
        EZTVSource(),
        X1337Source(),
        TPBSource(),
        RARBGSource(),
        TorrentGalaxySource(),
        KickassSource(),
        LimeTorrentsSource(),
    ]

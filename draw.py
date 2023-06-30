import os
import os.path as osp
from warnings import warn

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib.ttFont import TTFont


# from define.transfer_data import hanzi_transfer, hanzi_plus_transfer, english_transfer, NUMBER_CN2AN, time_transfer

FontsPATH=os.path.split(r"C:\Users\abget\Study\黑盒攻击\代码部分\Data\Fonts")
default_fonts = osp.join(*FontsPATH, "wxkai.ttf")  # )  #


def compare(vec1: np.ndarray, vec2: np.ndarray):
    return vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def compare2(vec1: np.ndarray, vec2: np.ndarray):
    return 1 / (1 + np.linalg.norm(vec1 - vec2))


class Font2pic:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Font2pic, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    @staticmethod
    def to_vac(p, flag: bool = True) -> np.ndarray:
        if flag:
            return np.array(p).astype(int).flatten()
        else:
            return np.array(p).astype(np.uint8)

    def __init__(self, font=default_fonts, _img_size=25):
        self.font_name = font
        self.font = ImageFont.truetype(font, _img_size)
        self._font = TTFont(self.font_name)
        self.img_size = _img_size
        self._dict: dict[str, Image.Image] = {}
        self.etc = []
        for _tt in [i for i in os.listdir(osp.join(*FontsPATH)) if str(i).endswith(".ttf")]:
            p = osp.join(*FontsPATH, _tt)
            self.etc.append((TTFont(p), ImageFont.truetype(p, _img_size)))

    def __getitem__(self, item):
        if item not in self._dict:
            self._dict[item] = self.draw_character(item)
        return self._dict[item]

    def __iter__(self):
        return iter(self._dict.items())

    def has_char(self, _c, font=None):
        cmap = font if font else self._font
        for table in cmap['cmap'].tables:
            if ord(_c) in table.ttFont.getBestCmap():
                return True
        return False

    def change_font(self, font):
        self.font_name = font
        self.font = ImageFont.truetype(font, self.img_size)
        self._font = TTFont(self.font_name)

    def draw_character(self, c: str, size=None) -> Image.Image:
        """

        :param size:
        :param c:
        :return:
        """

        font = self.font
        if not self.has_char(c):
            warn("draw: 字体不支持部分字符,已更换为其他字体")
            for cmap, _font in self.etc:
                if self.has_char(c, cmap):
                    font = _font
                    break
            else:
                warn("都没有")
        size = size if size else self.img_size
        img = Image.new('1', (size, size), 255)
        draw = ImageDraw.Draw(img)
        # draw.textbbox(txt, font=font)
        draw.text((0, 0), c, font=font, fill=0)
        return img


str_draw = Font2pic()
# str_draw['你'].show()
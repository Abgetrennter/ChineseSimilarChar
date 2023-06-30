from Const import pianpang, HanziStructure
import os

characters = cjk_ideographs = (
        '\u3007'  # 节选自hanzi包
        '\u4E00-\u9FFF'  # CJK Unified Ideographs
        '\u3400-\u4DBF'  # CJK Unified Ideographs Extension A
        '\uF900-\uFAFF'  # CJK Compatibility Ideographs
)


class HanZiDict:
    """缓存用,避免生成大量重复的"""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._dict: dict[str, HanZi] = {}

    def __call__(self, c):
        return self[c]

    def __getitem__(self, item):
        if isinstance(item, list):
            item = tuple(item)
        if item not in self._dict:
            self._dict[item] = HanZi(item)

        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __repr__(self):
        _s = ""
        for i, k in enumerate(self._dict):
            _s += f"{i}:{self._dict[k]}\n"
        return _s


def Pianpang(parts):
    if len(parts) == 2:
        return Hanzi_dict[parts[0]], Hanzi_dict[parts[1]]
    elif parts[-1] in pianpang:
        return Hanzi_dict[parts[:-1]], Hanzi_dict[parts[-1]]
    else:
        # 默认切分最左边,理论上是找到能成字的最大部分,但是太麻烦了
        return Hanzi_dict[parts[0]], Hanzi_dict[parts[1:]]


class HanZi:
    def __getitem__(self, item):
        return self.sub[item]

    def __init__(self, c: str | tuple[str] = None):
        self.c = c
        self.father:set[str] = set()
        self.count = 0
        self.struct = HanziStructure.独体
        self.sub: tuple = (HanZi, HanZi)
        # 糊弄IDE检查

        if isinstance(c, str):
            char_deal(self, c)
        elif isinstance(c, tuple):
            if len(c) == 1:
                self.c = c[0]
                char_deal(self, c[0])
            else:
                list_deal(self, c)
        else:
            raise ValueError("HanZi: 无效的参数")

    def __repr__(self):
        return f"{self.c}->HanZi({self.count}, {self.struct.name}, {''.join(str(i) for i in self.sub)})"

    def __str__(self):
        return "".join(self.c)

    def __iter__(self):
        return iter(self.sub)

    def my_iter(self):
        _q = [self]
        while _q:
            _ = _q.pop(0)
            yield _.c
            if _.sub:
                _q.extend(_.sub)


def char_deal(self:HanZi, c: str):
    self.struct = Hanzi_Structure.get(c, HanziStructure.独体)
    parts: tuple[str] = Hanzi_Splits.get(c, ())
    if self.struct == HanziStructure.独体:
        self.count = char_count.get(c, 5)
        self.sub = ()
        return
    if len(parts) == 2:
        self.sub = Hanzi_dict[parts[0]], Hanzi_dict[parts[1]]
    elif len(parts) > 2:
        # 一般认为最左边和最右边是偏旁,部首表验证一下
        self.sub = Pianpang(parts)
    else:
        self.struct = HanziStructure.独体
        self.count = char_count.get(c, 5)
        self.sub = ()
        return
        # raise ValueError("HanZi: 无效的参数")
    if c in char_count:
        self.count = char_count[c]
    else:
        self.count = sum(self.count for self in self.sub)
    for cc in self.sub:
        cc.father.add(self.c)


def list_deal(self:HanZi, c: tuple[str]):
    self.sub = Pianpang(c)
    self.count = sum(self.count for self in self.sub)
    self.struct = HanziStructure.组合
    for cc in self.sub:
        cc.father.add(self.c)


# def __getitem__(self, item):
#     return self.sub[item]


def judege_hanzi(c: str):
    for i in c:
        i = ord(i)
        if i == 0x3007 or (0x4e00 <= i <= 0x9fff) or (0x3400 <= i <= 0x4dbf) or (0xf900 <= i <= 0xfaff):
            #
            continue
        else:
            return False
    return True




# if os.path.exists('Data/HanZiDict.pkl'):
#     from pickle import load
#     Hanzi_dict = load(open('Data/HanZiDict.pkl', 'rb'))
#     pass
# else:
#     from _Load import Hanzi_Splits, Hanzi_Structure, Splits_Hanzi, char_count
#     Hanzi_dict = HanZiDict()
#     for i in Hanzi_Splits:
#         Hanzi_dict[i]
#     from pickle import dump
#     dump(Hanzi_dict,open('Data/HanZiDict.pkl', 'wb'))
# Hanzi_Splits_Prue: dict[HanZi, tuple[HanZi]] \
#     = {Hanzi_dict[key]: tuple(Hanzi_dict[i] for i in value) for key, value in Hanzi_Splits.items()}
# Splits_Hanzi_Prue: dict[HanZi, tuple[HanZi]] \
#     = {Hanzi_dict[key]: tuple(Hanzi_dict[i] for i in value) for key, value in Splits_Hanzi.items()}
# import pickle
# pickle.dump(Hanzi_dict, open("Data/Hanzi_dict.pkl", "wb"))

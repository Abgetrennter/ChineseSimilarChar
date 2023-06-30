from HanZi import HanZi,HanZiDict
from Const import HanziStructure
from draw import str_draw,compare
from pickle import load
Hanzi_dict = load(open('Data/HanZiDict.pkl', 'rb'))

def cal_stru_sim(origin, replacer):
    return abs(origin.struct - replacer.struct) + 1


def 递归计算相似度(origin: HanZi, replacer: HanZi) -> float:
    """
    递归计算两个字的相似度,不考虑形如 "也" "他" 这种的情况,假定 origin 是原始字, replacer 是目标.
    :param origin:
    :param replacer:
    :return:
    """
    if origin.struct == HanziStructure.独体 or replacer.struct == HanziStructure.独体:
        if replacer.struct == HanziStructure.组合 or origin.struct == HanziStructure.组合:
            # 懒得写解释了
            return .0
        else:
            return compare(str_draw.to_vac(str_draw[origin.c]), str_draw.to_vac(str_draw[replacer.c]))
    return (递归计算相似度(origin.sub[0], replacer.sub[0]) * origin.sub[0].count
            +
            递归计算相似度(origin.sub[1], replacer.sub[1]) * origin.sub[1].count) \
        / (origin.count * cal_stru_sim(origin, replacer))


def char_flatten(_char: HanZi) -> str:
    """
    将一个汉字横向拆分成多个汉字
    :param _char: 字符
    :return: 列表形式拆分字符
    """
    # splitable = ()
    ret = ""
    _l = [_char]
    while _l:
        c = _l.pop(0)
        match c.struct:
            case HanziStructure.左右 | HanziStructure.左中右:
                _l.extend(c.sub)
            case HanziStructure.组合:
                # ret += "".join(c.c)
                # continue
                return _char.c
            case _:
                ret += c.c
    return ret


def char_sim(_char: HanZi,N=1) -> str:
    c = _char
    _sps = c.sub
    # 自己，偏旁一，偏旁二,,,,
    chars = []
    for _sp in _sps:
        chars.extend(Hanzi_dict[c] for c in _sp.father)
    set_chars = [cc for cc in set(chars) if cc != c]

    if not set_chars:
        return c.c
    replaces = sorted(set_chars, key=lambda char: 递归计算相似度(_char, char), reverse=True)
    return "".join(str(i) for i in replaces[:N])


# def char_mars(*args, **kwargs) -> str:
#     return _char_mars(*args, **kwargs).c


def char_mars(_char: HanZi, func: int = 2,N=1) -> str:
    # 火星文版本,添加&删除偏旁
    if _char.father:
        adds = [Hanzi_dict[i] for i in _char.father]
    elif _char.sub:
        adds = [i for i in _char.sub if i.struct != HanziStructure.组合]
    else:
        return _char.c

    match func:
        case 1:
            return choice(adds)
        case 2:

            __l = ((c, (c.count - _char.count) / _char.count) for c in adds)
            __l = sorted(filter(lambda x: x[1] < 1 if x[1] > 0 else x[1] > -0.5, __l),
                         key=lambda x: abs(x[1]))  # , reverse=True)
            if __l:
                return "".join(str(i) for i in __l[0][:N])
            else:
                return _char.c
        case 0 | _:
            return "".join(str(i) for i in adds[:N])

if __name__ == '__main__':
    s='好'
    print(char_mars(Hanzi_dict[s],5))
    print(char_sim(Hanzi_dict[s],5))
    print(char_flatten(Hanzi_dict[s]))
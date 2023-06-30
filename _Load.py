from json import load
with open('Data/count.json', encoding='utf-8') as f:
    char_count = load(f)

with open('Data/HanziSplit.json', encoding='utf-8') as f:
    Hanzi_Splits = load(f)

with open('Data/HanziStructure.json', encoding='utf-8') as f:
    Hanzi_Structure = load(f)

_sp_chars = {}
for chara, splits in Hanzi_Splits.items():
    for sp in splits:
        if sp in _sp_chars:
            _sp_chars[sp].append(chara)
        else:
            _sp_chars[sp] = [chara]
Splits_Hanzi: dict[str, tuple[str]] = {name: tuple(chars) for name, chars in _sp_chars.items()}

# all_char= {*char_count.keys(), *hp.keys(), *hs.keys()}
# count_struct_split={char:[0, [], []] for char in all_char}
#
# for char in all_char:
#     if char in char_count:
#         count_struct_split[char][0]=char_count[char]
#     else:
#         count_struct_split[char][0]=0
#     if char in hs:
#         count_struct_split[char][1]=hs[char]
#     else:
#         count_struct_split[char][1]=[]
#     if char in hp:
#         count_struct_split[char][2]=hp[char]
#     else:
#         count_struct_split[char][2]=[]
#
# with open('Data/count_struct_split.json','w', encoding='utf-8') as f:
#     dump(count_struct_split,f,ensure_ascii=False)
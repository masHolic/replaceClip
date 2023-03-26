#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# loop infinitely and replace the contents of the clipboad.
# Ctrl-C to stop.
# Operation confirmed only on Windows 10.
# The replacement regular expression is read from the json file with the same name as the script.

from os import path
from time import sleep
from typing import Dict
import pyperclip, re, json
import pprint

# https://qiita.com/koppe/items/f27be003726b03304b24
def read_jsonc(filepath: str):
    with open(filepath, 'r', encoding="utf-8") as f:
        jsonc_text = f.read()
    json_text = re.sub(r'/\*[\s\S]*?\*/|//.*', '', jsonc_text)
    json_dict = json.loads(json_text)
    pprint.pprint(json_dict, sort_dicts=False)
    return json_dict

# https://qiita.com/Cartelet/items/bb19f3b7ed900699b789
def replaces_text(text: str, trdict: Dict[str, str]) -> str:
    return re.sub(
        "|".join(trdict.keys()), lambda m: next(
            (re.sub(pattern, trdict[pattern], m.group(0)) for pattern in trdict
            if re.fullmatch(pattern, m.group(0)))), text)

def main():
    json_path = path.splitext(path.basename(__file__))[0] + '.jsonc'
    replace_dict = read_jsonc(json_path)
    previous_text = pyperclip.paste()
    while True:
        copied_text = str(pyperclip.paste())
        if previous_text != copied_text:
            replaced_text = replaces_text(copied_text, replace_dict)
            pyperclip.copy(''.join(replaced_text))
            previous_text = replaced_text
            print('---Rewrite Complete!---')
            print(replaced_text)
        sleep (0.3)

if __name__ == "__main__":
    main()

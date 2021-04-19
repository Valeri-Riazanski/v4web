# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 02:08:16 2021

@author: kot
"""


def search4letters(phrase: str, letters: str = 'aeiou') -> str:
    list_phrase = list(phrase)
    list_letters = list(letters)
    frequency = {}
    for ch in list_letters:
        frequency.setdefault(ch, 0)
    for l in list_phrase:
        if l in list_letters:
            frequency[l] += 1
    list_freq = []
    for k, v in sorted(frequency.items()):
        list_freq.extend([k, '=', str(v), ' '])
    return ''.join(list_freq)


    # return set(letters).intersection(set(phrase))

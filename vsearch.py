# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 02:08:16 2021

@author: kot
"""


def search4letters(phrase: str, letters: str = 'aeiou') -> set:
    return set(letters).intersection(set(phrase))

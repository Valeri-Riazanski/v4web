# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 00:18:26 2021

@author: kot
"""
import mysql.connector
from typing import Dict


class UseDataBase:
    def __init__(self, config: Dict) -> None:
        """

        :type config: object
        """
        self.configuration = config

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

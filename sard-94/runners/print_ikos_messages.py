#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import sys

def print_messages(db_file, file_name):
    types=['warning','error','note']

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT status,line FROM checks JOIN statements on statements.id=checks.statement_id WHERE status>0")
    messages = c.fetchall()

    for message in messages:
        print(file_name+":"+str(message[1])+": "+types[message[0]-1])

    conn.close()

if __name__ == '__main__':
    print_messages(sys.argv[1],sys.argv[2])

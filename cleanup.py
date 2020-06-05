#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@package: SamateAnalyzer

@author:  Christoph Gentsch, DLR e.V.

"""
import MySQLdb
import re

db = MySQLdb.connect(user="root", passwd="root", db="debian_issues")
db.set_character_set('utf8')
c = db.cursor()
c.execute('SET NAMES utf8;')
c.execute('SET CHARACTER SET utf8;')
c.execute('SET character_set_connection=utf8;')

c.execute("SELECT id_cve,cwe_id FROM cve")
result = c.fetchall()

for cwe in result:
    search = re.search("CWE-(\d+)", cwe[1])
    if search:
        cwe_number = int(search.group(1))
        new_cwe = str("CWE-{:03d}".format(cwe_number))
        print(new_cwe)
        c.execute("UPDATE cve SET cwe_id=%s WHERE id_cve=%s", (new_cwe, cwe[0]))

db.commit()
c.close()

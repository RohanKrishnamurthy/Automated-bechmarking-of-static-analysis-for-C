#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@package: SamateAnalyzer

@author:  Christoph Gentsch, DLR e.V.
@created: 21.11.18
"""

import xml.etree.ElementTree as ElementTree
import MySQLdb
import re
import hashlib


def import_manifest(file_name, db_name):
    db = MySQLdb.connect(user="root", passwd="****", db="samate")
    c = db.cursor()

    root = ElementTree.parse(file_name).getroot()

    for testCase in root:

        for file in testCase.findall('file'):
            path = file.get('path')

            # exclude multi-tests and windows tests
            if not re.match("CWE.*[0-9]+\.c$", path) or re.match(".*w32,*", path):
                break

            for flaw in file.findall('flaw'):
                line = flaw.get('line')

                if flaw.get('name'):
                    file_hash = hashlib.md5((path + str(line)).encode()).hexdigest()
                    cwe = re.search('(CWE-.*):', flaw.get('name')).group(1)

                    # print(file_hash, path, line, cwe)

                    c.execute("INSERT INTO "+db_name+" VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE cwe=%s",
                        (file_hash, path, line, cwe, cwe))

    db.commit()
    c.close()


if __name__ == '__main__':
    import_manifest("manifest_juliet_c_13")
    #import_manifest("manifest-94.xml", "manifest_wireshark_18")

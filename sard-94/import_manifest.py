#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@package: SamateAnalyzer

@author:  Christoph Gentsch, DLR e.V.
@created: 20.12.18
@author:  Rohan Krishnamurthy, DLR e.V.
@update:  16.07.20
"""
import xml.etree.ElementTree as ElementTree
import MySQLdb
import re
import hashlib

def import_manifest(file_name):
    db = MySQLdb.connect(user="root", passwd="****", db="sard94")
    c = db.cursor()

    root = ElementTree.parse(file_name).getroot()

    for testCase in root:
        cve = testCase.findall('description')[0].text

        for file in testCase.findall('file'):
            path = file.get('path')

            for flaw in file.findall('flaw'):
                line = int(flaw.get('line'))

                if flaw.get('name'):
                    rel_path = re.search("SATE/wireshark-1.8.0/(.*\.c)", path)
                    if rel_path:
                        rel_path = rel_path.group(1)
                        file_hash = hashlib.md5((rel_path + str(line)).encode()).hexdigest()
                        cwe = re.search('(CWE-.*):', flaw.get('name')).group(1)

                        c.execute("INSERT INTO manifest VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE cwe=%s",
                            (file_hash, cve, rel_path, line, cwe, cwe))

    db.commit()
    c.close()


if __name__ == '__main__':
    import_manifest("manifest-94.xml")

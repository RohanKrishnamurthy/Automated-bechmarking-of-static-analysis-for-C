#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@package: SamateAnalyzer

@author:  Christoph Gentsch, DLR e.V.
@created: 21.11.18
"""
import fileinput
import re
import MySQLdb
import hashlib


def import_all():
    db = MySQLdb.connect(user="root", passwd="****", db="samate")
    db.set_character_set('utf8')
    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    #import_framac_log(c)
    #import_ikos_log(c)
    #import_cppcheck_log(c)
    #import_flawfinder_log(c)
    #import_clang_log(c)
    #import_scanbuild_log(c)
    #import_infer_log(c)
    #import_pscan_log(c)
    #import_sparse_log(c)
    import_oclint_log(c)
    #import_adlint_log(c)

    db.commit()
    c.close()

def import_oclint_log(cursor, tool_id='oclint', tool_log_file='runners/oclint-results.log'):
    n = 0
    with fileinput.input(tool_log_file) as f:

        for line in f:
            search = re.search(".*/(CWE.*\.c):(\d+):\d+: (.*) \[.*\|P(\d)\]", line)
            if search:
                file = search.group(1)
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file + str(line_no)).encode()).hexdigest()
                severity = 7 - int(search.group(4))
                desc = search.group(3).replace("'", "").strip()
                save_log_entry(cursor, desc, file, file_hash, line_no, tool_id, severity)
                n = n + 1
    print("imported", n, "lines")


def import_adlint_log(cursor, tool_id='adlint', tool_log_file='runners/adlint-results.log'):
    n = 0
    with fileinput.input(tool_log_file) as f:

        for line in f:
            search = re.search(".*/(CWE.*\.c):(\d+):\d+:(.*):c_builtin:(.*)", line)
            if search:
                file = search.group(1)
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file + str(line_no)).encode()).hexdigest()
                severity = search.group(3)
                desc = search.group(4).replace("'", "").strip()
                save_log_entry(cursor, desc, file, file_hash, line_no, tool_id, map_severity(severity))
                n = n + 1
    print("imported", n, "lines")

def import_sparse_log(cursor, tool_id='sparse', tool_log_file='runners/sparse-results.log'):
    n = 0
    with fileinput.input(tool_log_file) as f:
        for line in f:
            search = re.search(".*/(CWE.*\.c):(\d+):\d+: (.*): (.*)", line)
            if search:
                file = search.group(1)
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file + str(line_no)).encode()).hexdigest()
                severity = search.group(3)
                desc = search.group(4).replace("'", "").strip()
                save_log_entry(cursor, desc, file, file_hash, line_no, tool_id, map_severity(severity))
                n = n + 1
    print("imported", n, "lines")


def import_pscan_log(cursor, tool_id='pscan', tool_log_file='runners/pscan-results.log'):
    n = 0
    with fileinput.input(tool_log_file) as f:
        for line in f:
            search = re.search(".*/(CWE.*\.c):(\d+) (.*): (.*)", line)
            if search:
                file = search.group(1)
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file + str(line_no)).encode()).hexdigest()
                severity = search.group(3)
                if severity == "SECURITY":
                    sev = 5
                else:
                    sev = 1
                desc = search.group(4).replace("'", "").strip()
                save_log_entry(cursor, desc, file, file_hash, line_no, tool_id, sev)
                n = n + 1
    print("imported", n, "lines")


def import_infer_log(cursor, tool_id='infer', tool_log_file='runners/infer-results.log'):
    n = 0
    with fileinput.input(tool_log_file) as f:
        for line in f:
            search = re.search(".*/(CWE.*\.c):(\d+): (.*): (.*)", line)
            if search:
                file = search.group(1)
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file + str(line_no)).encode()).hexdigest()
                severity = search.group(3)
                desc = search.group(4).replace("'", "").strip()
                save_log_entry(cursor, desc, file, file_hash, line_no, tool_id, map_severity(severity))
                n = n + 1
    print("imported", n, "lines")


def import_scanbuild_log(cursor, tool_id='scan-build', tool_log_file='runners/scan-build-results.log'):
    n = 0
    with fileinput.input(tool_log_file) as f:

        for line in f:
            search = re.search("(CWE.*\.c):(\d+):\d+: (.*): (.*)", line)
            if search:
                file = search.group(1)
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file + str(line_no)).encode()).hexdigest()
                severity = search.group(3)
                desc = search.group(4).replace("'", "").strip()
                save_log_entry(cursor, desc, file, file_hash, line_no, tool_id, map_severity(severity)+1)
                n = n + 1
    print("imported", n, "lines")


def import_clang_log(cursor, tool_id='clang-tidy', tool_log_file='runners/clang-results.log'):
    n = 0
    with fileinput.input(tool_log_file) as f:

        for line in f:
            search = re.search(".*/(CWE.*\.c):(\d+):\d+: (.*): (.*)", line)
            if search:
                file = search.group(1)
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file + str(line_no)).encode()).hexdigest()
                severity = search.group(3)
                desc = search.group(4).replace("'", "").strip()
                save_log_entry(cursor, desc, file, file_hash, line_no, tool_id, map_severity(severity)+1)
                n = n + 1
    print("imported", n, "lines")


def import_flawfinder_log(cursor, tool_id='flawfinder', tool_log_file='runners/flawfinder-results.log'):
    n = 0
    with fileinput.input(tool_log_file) as f:

        for line in f:
            search = re.search(".*/(CWE.*\.c):(\d+): {2}\[(\d)\] (.*)", line)
            if search:
                file = search.group(1)
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file + str(line_no)).encode()).hexdigest()
                severity = int(search.group(3)) + 1
                desc = search.group(4).replace("'", "").strip()
                save_log_entry(cursor, desc, file, file_hash, line_no, tool_id, severity)
                n = n + 1
    print("imported", n, "lines")


def import_cppcheck_log(cursor, tool_id='cppcheck', tool_log_file='runners/cppcheck-results.log'):
    n = 0
    with fileinput.input(tool_log_file) as f:

        for line in f:
            search = re.search(".*/(CWE.*\.c):(\d+)\]: (.*)", line)
            if search:
                file = search.group(1)
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file + str(line_no)).encode()).hexdigest()
                desc = search.group(3).replace("'", "").strip()
                save_log_entry(cursor, desc, file, file_hash, line_no, tool_id, 5)
                n = n + 1
    print("imported", n, "lines")


def import_ikos_log(cursor, tool_id='ikos', tool_log_file='runners/ikos-results.log'):
    n = 0
    with fileinput.input(tool_log_file) as f:

        for line in f:
            search = re.search(".*/(CWE.*\.c):(\d+): (.*)", line)
            if search:
                file = search.group(1)
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file + str(line_no)).encode()).hexdigest()
                desc = search.group(3).replace("'", "").strip()
                save_log_entry(cursor, desc, file, file_hash, line_no, tool_id, map_severity(desc))
                n = n + 1
    print("imported", n, "lines")


def import_framac_log(cursor, tool_id='frama-c', tool_log_file='runners/framac-results.log'):
    n = 0

    with fileinput.input(tool_log_file) as f:
        state = 'header'
        source = ''
        file = ''
        line_no = 0
        file_hash = ''

        for line in f:

            if state == 'header':
                search = re.search("\[(.*)\] .*/(CWE.*\.c):(\d+):", line)
                if search:
                    source = search.group(1)
                    file = search.group(2)
                    line_no = int(search.group(3))
                    file_hash = hashlib.md5((file + str(line_no)).encode()).hexdigest()
                    state = 'desc'
                continue

            if state == 'desc':
                desc = line.strip()

                if contains_one_of_this(desc,["status invalid"]):
                    severity = 5
                elif contains_one_of_this(desc, ["out of bounds","uninitialized","overflow","division"]):
                    severity = 4
                elif contains_one_of_this(desc,["status unknown"]):
                    severity = 3
                else:
                    severity = 3

                if source == "value:alarm" and line_no > 0:
                    save_log_entry(cursor, desc, file, file_hash, line_no, tool_id, severity)
                    n += 1

                state = 'header'
                continue
    print("frama-c: imported", n, "lines")


def contains_one_of_this(text, phrases):
    for phrase in phrases:
        if text.find(phrase)>-1:
            return True
    return False


def map_severity(text):
    if text.find('error') > -1:
        severity = 5
    elif text.find('warning') > -1:
        severity = 4
    elif text.find('style') > -1:
        severity = 3
    elif text.find('note') > -1:
        severity = 1
    else:
        severity = 0

    return severity


def save_log_entry(c, desc, file, file_hash, line_no, tool_id, severity=0):
    c.execute("SELECT description, severity FROM tool_log WHERE hash_id=%s AND tool_id=%s", (file_hash, tool_id))
    result = c.fetchone()

    if result:
        desc = result[0] + "; " + desc
        new_severity = max(severity, result[1])
        c.execute("UPDATE tool_log SET description=%s, severity=%s WHERE hash_id=%s AND tool_id=%s",
                  (desc, new_severity, file_hash, tool_id))

    else:
        c.execute("INSERT INTO tool_log SET hash_id=%s, filename=%s, line=%s, description=%s, tool_id=%s, severity=%s",
                  (file_hash, file, line_no, desc, tool_id, severity))


if __name__ == '__main__':
    import_all()

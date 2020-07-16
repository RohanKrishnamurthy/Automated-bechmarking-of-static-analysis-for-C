#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@package: SamateAnalyzer

@author:  Christoph Gentsch, DLR e.V.
@created: 20.12.18
@author:  Rohan Krishnamurthy, DLR e.V.
@update:  16.07.20
"""

import fileinput
import re
import MySQLdb
import hashlib
import reverser
from argparse import ArgumentParser
from pathlib import Path


def save_log_entry(cursor, desc, file, function_hash, line_no, tool_id, severity=0):
    if function_hash == "":
        return

    cursor.execute("SELECT description, severity FROM tool_log WHERE filename=%s AND line=%s AND tool_id=%s",
                   (file, line_no, tool_id))
    result = cursor.fetchone()

    if result:
        desc = result[0] + "; " + desc
        new_severity = max(severity, result[1])
        cursor.execute("UPDATE tool_log SET description=%s, severity=%s WHERE filename=%s AND line=%s AND tool_id=%s",
                       (desc[0:1023], new_severity, file, line_no, tool_id))

    else:
        cursor.execute(
            "INSERT INTO tool_log SET hash_id=%s, filename=%s, line=%s, description=%s, tool_id=%s, severity=%s",
            (function_hash, file, line_no, desc[0:1023], tool_id, severity))


def import_clang_log(cursor, base_dir, tool_id='clang-tidy', tool_log_file='logs/clang-results.log'):
    n = 0
    p = Path(base_dir)

    with fileinput.input(tool_log_file) as f:

        for line in f:
            search = re.search("(.*\.c):(\d+):(\d+): (.*): (.*)", line)
            if search:
                file = search.group(1)
                file_path = str(next(p.glob("**/" + file))).replace(base_dir + "/", "")
                line_no = int(search.group(2))
                function_hash = get_function_hash(base_dir, file_path, line_no)
                severity = search.group(4)
                desc = search.group(5).replace("'", "").strip()
                save_log_entry(cursor, desc, file_path, function_hash, line_no, tool_id, map_severity(severity))
                n = n + 1
    print("imported", n, "lines")


def import_framac_log(cursor, tool_id='frama-c', tool_log_file='logs/framac-results.log'):
    n = 0

    with fileinput.input(tool_log_file) as f:

        state = 'header'
        file_path = ''
        line_no = 0
        file_hash = ''

        for line in f:

            if state == 'header':
                search = re.search("\[value:alarm\] .*/.*/SARD-testsuite-94/wireshark/(.*\.c):(\d+):", line)
                if search:
                    file_path = search.group(1)
                    line_no = int(search.group(2))
                    file_hash = hashlib.md5((file_path + str(line_no)).encode()).hexdigest()
                    state = 'desc'
                continue

            if state == 'desc' and line_no > 0:
                desc = line.replace("'", "").strip()

                if contains_one_of_this(desc, ["status invalid"]):
                    severity = 5
                elif contains_one_of_this(desc, ["out of bounds", "uninitialized", "overflow", "division"]):
                    severity = 4
                elif contains_one_of_this(desc, ["status unknown"]):
                    severity = 3
                else:
                    severity = 3

                save_log_entry(cursor, desc, file_path, file_hash, line_no, tool_id, severity)
                n += 1

                state = 'header'
                continue

    print("frama-c: imported", n, "lines")


def import_ikos_log(cursor, base_path, tool_id='ikos', tool_log_file='logs/ikos-results.log'):
    n = 0

    with fileinput.input(tool_log_file) as f:
        for line in f:
            search = re.search("(.*\.c):(\d+): (.*)", line)
            if search:
                file_path = search.group(1)
                line_no = int(search.group(2))
                function_hash = get_function_hash(base_path, file_path, line_no)
                desc = search.group(3).replace("'", "").strip()
                save_log_entry(cursor, desc, file_path, function_hash, line_no, tool_id, map_severity(desc))
                n += 1

    print("imported", n, "lines")


def import_infer_log(cursor, tool_id='infer', tool_log_file='logs/infer-results.log'): #copied from "bugs.txt"
    n = 0

    with fileinput.input(tool_log_file) as f:
        for line in f:
            search = re.search("(.*\.c):(\d+): (.*): (.*)", line)
            if search:
                file_path = search.group(1)
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file_path + str(line_no)).encode()).hexdigest()
                desc = search.group(4).replace("'", "").strip()
                save_log_entry(cursor, desc, file_path, file_hash, line_no, tool_id, map_severity(search.group(3)))
                n += 1

    print("imported", n, "lines")


def import_cppcheck_log(cursor, base_path, tool_id='cppcheck', tool_log_file='logs/cppcheck-results.log'):
    n = 0
    p = Path(base_path)

    with fileinput.input(tool_log_file) as f:

        for line in f:
            file_path = None

            # default case: we have a full file path
            search = re.search("wireshark/([a-z0-9/\-_]*\.c):(\d+)\]: \((.*)\) (.*)", line)

            if search:
                file_path = search.group(1)
            else:  # warum auch immer: sometimes we have a filename only
                search = re.search("([a-z0-9/\-_]*\.c):(\d+)\]: \((.*)\) (.*)", line)
                if search:  # try to find it in the path
                    file = search.group(1)
                    file_iter = p.glob("**/" + file)
                    try:
                        file_path = str(next(file_iter)).replace(base_path + "/", "")
                    except StopIteration:
                        print("error importing: ", file)
                        continue

            if file_path:
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file_path + str(line_no)).encode()).hexdigest()
                severity_text = search.group(3)
                desc = search.group(4).replace("'", "").strip()
                save_log_entry(cursor, desc, file_path, file_hash, line_no, tool_id, map_severity(severity_text))
                n += 1

    print("imported", n, "lines")


def import_flawfinder_log(cursor, tool_id='flawfinder',
                          tool_log_file='logs/flawfinder-results.log'):
    n = 0
    with fileinput.input(tool_log_file) as f:

        for line in f:
            search = re.search(".*/wireshark/(.*\.c):(\d+): {2}\[(\d)\] (.*)", line)
            if search:
                file_path = search.group(1)
                line_no = int(search.group(2))
                file_hash = hashlib.md5((file_path + str(line_no)).encode()).hexdigest()
                severity = int(search.group(3))+1
                desc = search.group(4).replace("'", "").strip()
                save_log_entry(cursor, desc, file_path, file_hash, line_no, tool_id, severity)
                n += 1
    print("imported", n, "lines")


def get_function_hash(base_dir, file_path, line_no):
    try:
        rvsr = reverser.Reverser(base_dir, file_path)
        function_name = rvsr.get_function_at(line_no)
    except Exception as e:
        print(e)
        function_name = ""

    return hashlib.md5((file_path + ":" + function_name).encode()).hexdigest()


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


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('base_dir', help='Source code base directory, containing compilation database')
    args = arg_parser.parse_args()

    db = MySQLdb.connect(user="root", passwd="****", db="sard94")
    db.set_character_set('utf8')
    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    import_framac_log(c)
    # import_clang_log(c, args_base_dir)
    # import_ikos_log(c, args.base_dir)
    # import_flawfinder_log(c, args.base_dir)
    # import_cppcheck_log(c, args.base_dir)
    # import_infer_log(c)

    db.commit()
    c.close()

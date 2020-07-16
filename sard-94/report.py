#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@package: SamateAnalyzer

@author:  Christoph Gentsch, DLR e.V.
@created: 21.11.18
@author:  Rohan Krishnamurthy, DLR e.V.
@update:  16.07.20
"""
import MySQLdb
import numpy as np
import time

sfp_clusters = ["Memory Access", "Resource Management", "Tainted Input", "Risky Values", "Authentication",
                "Access Control", "Information Leak", "Memory Management", "Exception Management", "Synchronization",
                "API", "Malware", "Unused Entities", "Other"]


def get_tools(cursor):
    cursor.execute("SELECT distinct(tool_id) FROM tool_log")
    return [result[0] for result in cursor.fetchall()]


def print_reports(cursor):
    tools = get_tools(cursor)

    cursor.execute("SELECT count(*) FROM manifest")
    condition_positive = cursor.fetchone()[0]

    for tool in tools:
        cursor.execute("SELECT count(*) FROM tool_log where tool_id=%s", (tool,))
        predicted_positive = cursor.fetchone()[0]

        cursor.execute(
            "SELECT count(distinct(tool_log.hash_id)) FROM sard94.tool_log join manifest on manifest.hash_id=tool_log.hash_id where severity>1 AND tool_id=%s",
            (tool,))
        true_positive = cursor.fetchone()[0]

        if predicted_positive > 0:
            precision = true_positive / predicted_positive
            recall = true_positive / condition_positive
            if true_positive > 0:
                f1 = 2 * precision * recall / (precision + recall)
            else:
                f1 = 0
        else:
            precision, recall, f1 = (0, 0, 0)

        print(tool, predicted_positive, precision, recall, f1)


def print_score(cursor):
    cloc = 1981699
    #cloc = 4719409

    cursor.execute("SELECT count(*) FROM tool_log where tool_id='flawfinder' and severity > 4")
    predicted_positive_flaw = cursor.fetchone()[0]

    cursor.execute("SELECT count(*) FROM tool_log where tool_id='cppcheck'")
    predicted_positive_cpp = cursor.fetchone()[0]

    score = (predicted_positive_flaw + predicted_positive_cpp ) / cloc * 1000

    return score


if __name__ == '__main__':
    db = MySQLdb.connect(user="root", passwd="****", db="sard94")
    c = db.cursor()

    print_reports(c)
    print(print_score(c))

    db.close()

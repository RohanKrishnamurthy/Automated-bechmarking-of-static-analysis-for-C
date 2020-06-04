#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@package: SamateAnalyzer

@author:  Christoph Gentsch, DLR e.V.
@created: 10.12.18
"""
import MySQLdb
from itertools import combinations
import math
import numpy as np

def get_tools(cursor):
    cursor.execute("SELECT distinct(tool_id) FROM tool_log")
    return [result[0] for result in cursor.fetchall()]

def get_tool_query(tools):
    tool_query = ""
    for tool in tools:
        tool_query = tool_query + "tool_id='" + tool + "' OR "
    return  tool_query[0:-4]


def tool_stats(cursor, tools, min_severity=0):
    cursor.execute("SELECT count(*) FROM manifest_juliet_c_13")
    condition_positive = int(cursor.fetchone()[0])
    all_lines = 4785252

    cursor.execute("SELECT count(distinct(tool_log.hash_id)) FROM tool_log WHERE " + get_tool_query(tools) + " and severity>%s", (min_severity,))
    predicted_positive = cursor.fetchone()[0]
    predicted_negative = all_lines - predicted_positive

    cursor.execute("SELECT count(distinct(tool_log.hash_id)) FROM manifest_juliet_c_13 join tool_log ON " +
        "manifest_juliet_c_13.hash_id=tool_log.hash_id WHERE " + get_tool_query(tools) + " and severity>%s", (min_severity,))
    tp = true_positive = cursor.fetchone()[0]

    fp = predicted_positive - true_positive #false_positive
    fn = condition_positive - true_positive #false_negative
    tn = predicted_negative - fn #true negative

    if predicted_positive > 0:
        precision = true_positive / predicted_positive
        recall = true_positive / condition_positive
        if true_positive > 0:
            f1 = 2 * precision * recall / (precision + recall)
            mcc = ((tp*tn)-(fp*fn))/math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
        else:
            f1 = 0
            mcc = -1
    else:
        precision, recall, f1, mcc = (0, 0, 0, 0)

    return (precision, recall, f1, mcc)

def combine(cursor, num_tools, min_severity):

    tools = get_tools(cursor)
    num_combinations = int(math.factorial(len(tools)) / (math.factorial(len(tools) - num_tools) * math.factorial(num_tools)))
    stats = np.zeros((num_combinations, 4))
    names = []
    combs = combinations(tools, num_tools)
    n = 0

    for combination in combs:
        names.append(str(combination))
        stats[n,:] = tool_stats(cursor, combination, min_severity)
        n = n + 1

    best_combo_index = np.argmax(stats,0)[3]
    print("best combo: ",names[best_combo_index],", scores: ",stats[best_combo_index])
    print("average: ",np.mean(stats,0))

if __name__ == '__main__':
    db = MySQLdb.connect(user="root", passwd="****", db="samate")
    db.set_character_set('utf8')
    c = db.cursor()

    #combine(c, 2, 1)
    # combine(c, 2, 3)
    #combine(c, 3, 1)
    # combine(c, 3, 3)


    #print(tool_stats(c, ['frama-c', 'cppcheck', 'flawfinder'], 1))
    print(tool_stats(c, ['flawfinder_f', 'cppcheck', 'clang'], 1))
    
    db.close()

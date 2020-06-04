#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@package: SamateAnalyzer

@author:  Christoph Gentsch, DLR e.V.
@created: 21.11.18
"""
import MySQLdb
import numpy as np
import time
import csv
import math

sfp_clusters = ["Memory Access", "Resource Management", "Tainted Input", "Risky Values", "Authentication",
                "Access Control", "Information Leak", "Memory Management", "Exception Management", "Synchronization",
                "API", "Malware", "Unused Entities", "Other"]


def get_tools(cursor):
    cursor.execute("SELECT distinct(tool_id) FROM tool_log")
    return [result[0] for result in cursor.fetchall()]


def get_sfp_names(cursor):
    cursor.execute("""
        SELECT sfp_cluster, SUM(tool_count),SUM(total_count) AS total,SUM(tool_count)/SUM(total_count) as percent FROM
        (SELECT cwe,count(cwe) as total_count FROM manifest_juliet_c_13 group by cwe) as tab2 LEFT JOIN
        (SELECT cwe,count(cwe) as tool_count FROM (SELECT distinct(tool_log.hash_id),cwe FROM manifest_juliet_c_13 join 
        tool_log on manifest_juliet_c_13.hash_id=tool_log.hash_id where tool_id=%s) as tab3 group by cwe) 
        as tab1 ON tab1.cwe=tab2.cwe
        JOIN cwe on cwe.cwe=tab2.cwe group by sfp_cluster ORDER BY total DESC
    """, ('framac',))

    results = cursor.fetchall()
    return [cluster[0] for cluster in results]


def sfp_stats(cursor, tool, min_severity=0):
    cursor.execute("""
        SELECT sfp_cluster, SUM(tool_count),SUM(total_count) AS total,SUM(tool_count)/SUM(total_count) as recall FROM
        (SELECT cwe,count(cwe) as total_count FROM manifest_juliet_c_13 group by cwe) as tab2 LEFT JOIN
        (SELECT cwe,count(cwe) as tool_count FROM (SELECT distinct(tool_log.hash_id),cwe FROM manifest_juliet_c_13 join 
        tool_log on manifest_juliet_c_13.hash_id=tool_log.hash_id where tool_id=%s and severity>%s) as tab3 group by cwe) 
        as tab1 ON tab1.cwe=tab2.cwe
        JOIN cwe on cwe.cwe=tab2.cwe group by sfp_cluster ORDER BY total DESC
    """, (tool, min_severity,))

    results = cursor.fetchall()
    return [float(cluster[3]) if cluster[3] else 0 for cluster in results]


def tool_stats(cursor, tool, min_severity=0):
    cursor.execute("SELECT count(*) FROM manifest_juliet_c_13")
    condition_positive = cursor.fetchone()[0]
    all_lines = 4785252

    cursor.execute("""SELECT count(*) FROM tool_log WHERE tool_id=%s and severity>%s""", (tool, min_severity,))
    predicted_positive = cursor.fetchone()[0]
    predicted_negative = all_lines - predicted_positive

    cursor.execute("""SELECT count(*) FROM manifest_juliet_c_13 join tool_log ON 
        manifest_juliet_c_13.hash_id=tool_log.hash_id WHERE tool_id=%s and severity>%s""", (tool, min_severity,))
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

    return (precision, recall, mcc)


def print_reports(cursor):
    tools = get_tools(cursor)

    all_stats = np.zeros((13, len(tools)))

    for n in range(0, len(tools)):
        for sev in range(-1,5):
            stats =  tool_stats(cursor, tools[n], sev)
            print(tools[n],sev, stats)

        all_stats[:, n] = sfp_stats(cursor, tools[n])

    print(tools)
    print(all_stats * 100)


def get_html_report(cursor, min_severity, file_name):
    time_str = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

    tools = get_tools(cursor)
    sfp_names = get_sfp_names(cursor)
    sfp_names.append('#precision')
    sfp_names.append('#recall')
    sfp_names.append('#f1')

    all_stats = np.zeros((16, len(tools)))

    for n in range(0, len(tools)):
        all_stats[0:13, n] = sfp_stats(cursor, tools[n], min_severity)
        all_stats[13:16, n] = tool_stats(cursor, tools[n], min_severity)

    markup = """
    <html>
    <head>
    <title>FOSS C SATE Report</title>
    <link rel="stylesheet" href="styles.css">
    </head>
    <body>
    <h2>FOSS C SATE Report (severity>{:d})</h2>
    <h3>{:s}</h3>
    <table>
        <tr><th> </th>
    """.format(min_severity, time_str)

    for tool in tools:
        markup += "<th>" + tool + "</th>"

    for n in range(0, all_stats.shape[0]):
        markup += "</tr>\n<tr><td>" + sfp_names[n] + "</td>"

        for value in all_stats[n, :]:
            markup += "<td style='background-color:#64{:02x}64'>".format(int(value*150)+100) + str.format("{:.2%}", value) + "</td>\n"

    markup += "</tr>\n"

    markup += "</table></body></html>"

    f = open(file_name, "w", encoding="utf-8")
    f.write(markup)
    f.close()

    return markup

def get_csv_report(cursor, min_severity, file_name):

    tools = get_tools(cursor)
    sfp_names = get_sfp_names(cursor)
    sfp_names.append('#precision')
    sfp_names.append('#recall')
    sfp_names.append('#f1')

    all_stats = np.zeros((16, len(tools)))

    for n in range(0, len(tools)):
        all_stats[0:13, n] = sfp_stats(cursor, tools[n], min_severity)
        all_stats[13:16, n] = tool_stats(cursor, tools[n], min_severity)

    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        header = ['sfp']
        header.extend(tools)
        writer.writerow(header)

        for n in range(0, all_stats.shape[0]):
            row = [sfp_names[n]]
            row.extend(all_stats[n, :])
            writer.writerow( row )


if __name__ == '__main__':
    db = MySQLdb.connect(user="root", passwd="root", db="samate")
    c = db.cursor()

    print_reports(c)
    #get_csv_report(c,4, "report5.csv")
    get_html_report(c,0, "report0.html")

    db.close()

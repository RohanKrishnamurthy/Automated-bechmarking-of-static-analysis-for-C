# Benchmarking Open-Source Static Analyzers for Security Testing

Automated process of evaluation of 11 open source SAST tools for the C programming language on the Juliet Test Suite
for C/C++ and of six tools on the Wireshark production software.

Authors: Christoph Gentsch, Rohan Krishnamurthy and Thomas Heinze, German Aerospace Center (DLR), Jena, Germany

**Paper**

This evaluation of different open-source tools is availble as part of the submission of the paper for ISOLA'2020 conference.
The submitted copy of the paper is available in this repository [here](paper/sast_isola.pdf).

**File structure:**

- `main.sh/`

  - contains pre-requisits packages for Ubuntu 18.04 and initiation of evaluation.
  
- `menu.sh/`

  - provides modularity for the evaluation of tool of your choice (out of the installed 11 tools)

- `runners/`

  - this folder contains scripts to install and eventually run the tool on Juliet test suite

- `import_log.py/`

  - imports the results from the tools

- `report.py/`

  - provides output of the evaluation in CLI, as HTML and as CSV formats

## Evaluation procedure

1. Run main.sh
    - setup a MySQL-database and import the database.sql script with pre-imported Juliet Manifest and CWE dataset
2. Run menu.sh
    - install the SAST tools to test and run the specific "runner"-script
    - choose the tool to be evaluated and wait for the process to complete (Note: wait times are different for each and every tool)
    - import the generated log file with import_log.py 
    - generate a report with report.py
    - results in CLI/HTML/CSV formats
3. For production software Wireshark:
    - cd sard-94 and run the specific "runner"-script
    - import the generated log file with import_log.py (uncomment the code to select the tool intended to be run)
    - generate a report with report.py
    - results in CLI/HTML/CSV formats



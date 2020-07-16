#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@package: SamateAnalyzer

@author:  Christoph Gentsch, DLR e.V.
@created: 20.12.18
@author:  Rohan Krishnamurthy, DLR e.V.
@update:  16.07.20
"""
from argparse import ArgumentParser
from clang import cindex
import os, re

if 'CLANG_LIBRARY_PATH' in os.environ:
    cindex.Config.set_library_path(os.environ['CLANG_LIBRARY_PATH'])


def get_compiler_args(base_dir, source_file):

    comp_db = cindex.CompilationDatabase.fromDirectory(base_dir)

    source_file_path = base_dir + '/' + source_file
    source_file = source_file_path

    file_args = comp_db.getCompileCommands(source_file_path)

    if not file_args:
        raise Exception("no entry in compile database for: "+source_file)

    args = [a for a in file_args[0].arguments
            if (a.startswith("-D") or a.startswith("-I") or a.startswith("-f") or a.startswith("-p"))]

    if 'C_INCLUDE_PATH' in os.environ:
        includes = os.environ['C_INCLUDE_PATH']
        args.extend(['-I'+line for line in includes.split(':')])

    new_args = []

    for arg in args:
        new_arg = arg
        if arg == "-I.":
            new_arg = "-I"+file_args[0].directory
        elif arg.startswith("-I"):
            m = re.search("-I\./(.*)", arg)
            if m:
                new_arg = "-I"+file_args[0].directory + "/" + m.group(1)
            else:
                m2 = re.search("-I\.\./(.*)", arg)
                if m2:
                    new_arg = "-I"+file_args[0].directory + "/../" + m2.group(1)

        new_args.append(new_arg)

    return new_args

if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('base_dir', help='Source code base directory, containing compilation database')
    arg_parser.add_argument('source_file', help='C source file to parse.')
    args = arg_parser.parse_args()

    ret = ""
    for arg in get_compiler_args(args.base_dir, args.source_file):
        ret += arg+" "

    print(ret)

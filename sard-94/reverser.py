#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@package: SamateAnalyzer

@author:  Christoph Gentsch, DLR e.V.
@created: 02.01.19
@author:  Rohan Krishnamurthy, DLR e.V.
@update:  16.07.20
"""
from argparse import ArgumentParser
from clang import cindex
from clang.cindex import Cursor, CursorKind
import os, sys, re

if 'CLANG_LIBRARY_PATH' in os.environ:
    cindex.Config.set_library_path(os.environ['CLANG_LIBRARY_PATH'])


class Reverser:
    function_dict = {}
    source_file = ""
    translation_unit = None

    def __init__(self, base_dir, source_file):

        index = cindex.Index.create()
        comp_db = cindex.CompilationDatabase.fromDirectory(base_dir)

        source_file_path = base_dir + '/' + source_file
        self.source_file = source_file_path

        file_args = comp_db.getCompileCommands(source_file_path)

        if not file_args:
            raise Exception("no entry in compile database for: " + source_file)

        args = [a for a in file_args[0].arguments
                if (a.startswith("-D") or a.startswith("-I") or a.startswith("-f") or a.startswith("-p"))]

        if 'C_INCLUDE_PATH' in os.environ:
            includes = os.environ['C_INCLUDE_PATH']
            args.extend(['-I' + line for line in includes.split(':')])

        new_args = []

        for arg in args:
            new_arg = arg
            if arg == "-I.":
                new_arg = "-I" + file_args[0].directory
            elif arg.startswith("-I"):
                m = re.search("-I\./(.*)", arg)
                if m:
                    new_arg = "-I" + file_args[0].directory + "/" + m.group(1)
                else:
                    m2 = re.search("-I\.\./(.*)", arg)
                    if m2:
                        new_arg = "-I" + file_args[0].directory + "/../" + m2.group(1)

            new_args.append(new_arg)

        new_args.append("-w")

        self.translation_unit = index.parse(source_file_path, new_args)

        for error in self.translation_unit.diagnostics:
            print(error, file=sys.stderr)

    def _get_function_rec(self, cursor, n=100):
        if n > 0:
            if cursor.kind == CursorKind.FUNCTION_DECL:
                return cursor.spelling
            elif cursor.semantic_parent:
                return self._get_function_rec(cursor.semantic_parent, n - 1)
            else:
                return ""
        else:
            return ""

    def get_function_at(self, line_no):
        loc = self.translation_unit.get_location(self.source_file, (line_no, -1))
        cursor = Cursor.from_location(self.translation_unit, loc)
        return self._get_function_rec(cursor)


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('base_dir', help='Source code base directory, containing compilation database')
    arg_parser.add_argument('source_file', help='C source file to parse')
    arg_parser.add_argument('line_no', type=int, help='C source file line number')
    args = arg_parser.parse_args()

    reverser = Reverser(args.base_dir, args.source_file)
    print(reverser.get_function_at(args.line_no))

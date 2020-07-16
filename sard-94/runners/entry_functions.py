#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@package: SamateAnalyzer

@author:  Christoph Gentsch, DLR e.V.
@created: 18.12.18
@author:  Rohan Krishnamurthy, DLR e.V.
@update:  16.07.20
"""
from argparse import ArgumentParser, FileType
from clang import cindex
from clang.cindex import CursorKind, LinkageKind
import os, sys, re

if 'CLANG_LIBRARY_PATH' in os.environ:
    cindex.Config.set_library_path(os.environ['CLANG_LIBRARY_PATH'])

class EntryFunctions:
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

        new_args.append("-w")

        self.translation_unit = index.parse(source_file_path, new_args)

        for error in self.translation_unit.diagnostics:
            print(error, file=sys.stderr)

    @staticmethod
    def get_unique_nodes(node_list):
        new_list = []
        if node_list:
            for node in node_list:
                if node not in new_list:
                    new_list.append(node)

        return new_list

    def get_subnodes(self, node, ls=None):
        ls = ls if ls is not None else []
        for n in node.get_children():
            # print('   ',node.spelling,node.kind)
            ls.append(n)
            self.get_subnodes(n, ls)
        return ls

    def get_all_subnodes(self, node, node_kind=None, ls=None):
        ls = ls if ls is not None else []
        for n in node.get_children():
            if n.location.file is not None and n.location.file.name == self.source_file:
                if node_kind:
                    if n.kind == node_kind:
                        ls.append(n)
                else:
                    ls.append(n)
                self.get_all_subnodes(n, node_kind, ls)
        return ls

    def get_calls(self, node):
        ref_list = []

        if node.spelling.startswith("__builtin"):
            return ref_list

        if not node.is_definition():
            node = self.get_function_definition(node.spelling)

        if not node:
            return []

        call_expr = self.get_all_subnodes(node, CursorKind.CALL_EXPR)
        for call in call_expr:
            ref_list.extend(self.get_all_subnodes(call, CursorKind.DECL_REF_EXPR))

        return [call.referenced for call in self.get_unique_nodes(ref_list)
                if call.referenced.kind == CursorKind.FUNCTION_DECL and
                call.referenced.location.file is not None and call.referenced.location.file.name == self.source_file]

    def get_calls_rec(self, node, depth, ref_list=None):
        ref_list = ref_list if ref_list is not None else []

        if depth > 0:
            direct_calls = self.get_calls(node)
            for call in direct_calls:
                self.get_calls_rec(call, depth - 1, ref_list)

            ref_list.extend(direct_calls)

        return ref_list

    def get_function_definition(self, name):
        if not name in self.function_dict:
            for n in self.translation_unit.cursor.get_children():
                if n.spelling == name and n.location.file is not None and n.location.file.name == self.source_file \
                        and n.kind == CursorKind.FUNCTION_DECL and n.is_definition():
                    self.function_dict[name] = n
                    break

        if name in self.function_dict:
            return self.function_dict[name]
        else:
            return None

    def get_external_functions(self):
        results = []
        for n in self.translation_unit.cursor.get_children():
            if n.location.file is not None and n.location.file.name == self.source_file \
                    and n.kind == CursorKind.FUNCTION_DECL and n.linkage == LinkageKind.EXTERNAL and n.is_definition():
                results.append(n)
        return self.get_unique_nodes(results)

    def debug(self):
        for function in self.get_external_functions():
            print('[', function.spelling, ']')
            # call_list.extend(get_calls_rec(function, source_file_path, 10))
            if function.spelling == "uat_load_restart":
                calls = self.get_calls_rec(function, 10)

                for c in calls:
                    print('     ', c.kind, c.spelling)

    def get_entry_points(self):
        call_list = []
        functions = self.get_external_functions()

        for function in functions:
            call_list.extend(self.get_calls_rec(function, 5))

        call_list = [c.spelling for c in self.get_unique_nodes(call_list)]

        for f in functions:
            if f.spelling not in call_list:
                print(f.spelling)


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('base_dir', help='Source code base directory, containing compilation database')
    arg_parser.add_argument('source_file', help='C source file to parse.')
    args = arg_parser.parse_args()

    funky = EntryFunctions(args.base_dir, args.source_file)
    funky.get_entry_points()


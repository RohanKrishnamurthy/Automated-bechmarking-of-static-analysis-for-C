#!/bin/bash

export CLANG_LIBRARY_PATH="/usr/lib/llvm-6.0/lib"
export C_INCLUDE_PATH="/usr/lib/gcc/x86_64-linux-gnu/7/include:/usr/lib/gcc/x86_64-linux-gnu/7/include-fixed:/usr/include/x86_64-linux-gnu:/usr/include"

for entry in `entry_functions.py $1 $2`; do
    echo "[[[ checking $entry ]]]"
    frama-c -machdep x86_64 -c11 -quiet -val -main "$entry" -lib-entry -json-compilation-database $1/compile_commands.json $1/$2
done


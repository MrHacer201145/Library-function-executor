import sys
import cffi
import os

def arg_parser(args):
    obj_file_name = args.pop(0)
    fun_type = args.pop(0)
    fun_name = args.pop(0)

    arg_types = []
    fun_args = []

    cur_num = 0
    for obj in args:
        if obj.isdigit():
            arg_types.append(f'int _{cur_num}')
            fun_args.append(int(obj))
        else:
            arg_types.append(f'char* _{cur_num}')
            fun_args.append(bytes(obj, 'utf-8'))
        cur_num += 1
    
    return obj_file_name, fun_type, fun_name, arg_types, fun_args

def make_function_str(type, name, types) -> str:
    joined_args = ', '.join(types)

    joined = type + ' ' + name + '(' + joined_args + ');'
    return joined

def call_function(object, type, name, types, args):
    ffi = cffi.FFI()

    function_str = make_function_str(
        type, name, types
    )
    ffi.cdef(function_str)

    lib_path = os.path.abspath(object)
    lib = ffi.dlopen(lib_path)
    func = ffi.addressof(lib, name)

    result = func(*tuple(args))

    if type != 'void':
        print(result)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: <library name> <func type> <func name> <other params>")
        print("Example: test.so void test_print 10")
        exit(1)

    lib_name, type, name, types, args = arg_parser(sys.argv[1:])
    call_function(lib_name, type, name, types, args)

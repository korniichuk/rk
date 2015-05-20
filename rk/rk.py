# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from errno import ENOTDIR
from json import dumps, load
from os import getuid, link, listdir, makedirs, remove
from os.path import dirname, exists, isdir, isfile, join
from shutil import rmtree
from sys import argv, exit

from configobj import ConfigObj

module_location = dirname(__file__)
config_rk_abs_path = join(module_location, "config/rk.ini")
argparse = {} # Strings for -h --help
messages = {} # Strings for output

def create_dictionaries():
    """Create "argparse" and "messages" dictionaries"""

    config = ConfigObj(config_rk_abs_path)
    config_argparse_rel_path = config["config_argparse_rel_path"]
    config_argparse_abs_path = join(module_location, config_argparse_rel_path)
    config_messages_rel_path = config["config_messages_rel_path"]
    config_messages_abs_path = join(module_location, config_messages_rel_path)
    with open(config_argparse_abs_path, 'r') as f:
        argparse_list = f.read().splitlines()
    for i in range(0, len(argparse_list), 2):
        argparse[argparse_list[i]] = argparse_list[i+1]
    with open(config_messages_abs_path, 'r') as f:
        messages_list = f.read().splitlines()
    for i in range(0, len(messages_list), 2):
        messages[messages_list[i]] = messages_list[i+1]

def install_all(args):
    """Install all remote jupyter kernels from kernels dict"""

    config = ConfigObj(config_rk_abs_path)
    config_kernels_rel_path = config["config_kernels_rel_path"]
    config_kernels_abs_path = join(module_location, config_kernels_rel_path)
    # Load kernels.json file
    with open(config_kernels_abs_path) as f:
        kernels_dict = load(f)
    # Create kernels list from kernels dict
    kernels_list = [k for k in kernels_dict.keys()]
    # Sort kernels list
    kernels_list.sort()
    # Install remote jupyter kernels
    args.kernel_names = kernels_list
    install_kernel(args)

def install_kernel(args):
    """Install remote jupyter kernel/kernels"""

    def copy_logos(img_location, logo_name_srt, destination):
        """Copy logos"""

        for size in ["32", "64"]:
            logo_abs_path_str = join(join(module_location, img_location),
                                     logo_name_srt)
            logo_abs_path = logo_abs_path_str.format(size)
            logo_name = logo_name_srt.format(size)
            if exists(logo_abs_path) and isfile(logo_abs_path):
                link(logo_abs_path, join(destination, logo_name))

    def create_directory(directory_name):
        """Create directory"""

        try:
            makedirs(directory_name, mode=0o755)
        except OSError as exception: # Python3 NotADirectoryError
            if exception.errno == ENOTDIR:
                 path = directory_name
                 while path != '/':
                     if isfile(path):
                         remove(path)
                     path = dirname(path)
                 makedirs(directory_name, mode=0o755)
            else:
                raise exception

    def create_kernel_json_file(display_name, language, script, interpreter,
                                connection_file, remote_host, destination):
        """Create kernel.json file"""

        kernel_dict = {"argv": [], "display_name": display_name,
                       "language": language}
        kernel_dict["argv"].append(script)
        kernel_dict["argv"].append(interpreter)
        kernel_dict["argv"].append(connection_file)
        kernel_dict["argv"].append(remote_host)
        with open(join(destination, "kernel.json"), 'w') as f:
            f.write(dumps(kernel_dict, indent=1, sort_keys=True))

    if getuid() == 0:
        config = ConfigObj(config_rk_abs_path)
        kernels_location = config["kernels_location"]
        img_location = config["img_location"]
        logo_name_srt = config["logo_name_srt"]
        script = config["script"]
        connection_file = config["connection_file"]
        config_kernels_rel_path = config["config_kernels_rel_path"]
        config_kernels_abs_path = join(module_location,
                                       config_kernels_rel_path)
        kernel_names = args.kernel_names
        if kernel_names == None:
            # Install template of remote kernel
            kernel_name = config["kernel_name"]
            display_name = config["display_name"]
            language = config["language"]
            interpreter = config["interpreter"]
            remote_host = config["remote_host"]
            kernel_abs_path = join(kernels_location, kernel_name)
            if not exists(kernel_abs_path):
                # Create directory
                create_directory(kernel_abs_path)
                # Copy logos
                copy_logos(img_location, logo_name_srt, kernel_abs_path)
                # Create kernel.json
                create_kernel_json_file(display_name, language, script,
                                        interpreter, connection_file,
                                        remote_host, kernel_abs_path)
                print(messages["_installed_template"])
            else:
                print(messages["_delete_template"])
                answer = raw_input()
                answer_lower = answer.lower()
                if ((answer_lower == 'y') or (answer_lower == 'yes') or
                        (answer_lower == 'yep')):
                    uninstall_kernel(args)
                    install_kernel(args)
        else:
            # Install kernel/kernels
            # Load kernels.json file
            with open(config_kernels_abs_path) as f:
                kernels_dict = load(f)
            # Check kernel_names list/
            no_kernel_names = []
            for kernel_name in kernel_names:
                if kernel_name not in kernels_dict:
                    no_kernel_names.append(kernel_name)
            if len(no_kernel_names) != 0:
                if len(no_kernel_names) == 1:
                    print(messages["_error_NoKernel"] % no_kernel_names[0])
                else:
                    print(messages["_error_NoKernels"] %
                            '\' \''.join(no_kernel_names))
                exit(1)
            # /Check kernel_names list
            for kernel_name in kernel_names:
                display_name = kernels_dict[kernel_name]["display_name"]
                language = kernels_dict[kernel_name]["language"]
                interpreter = kernels_dict[kernel_name]["interpreter"]
                remote_host = kernels_dict[kernel_name]["remote_host"]
                kernel_abs_path = join(kernels_location, kernel_name)
                if not exists(kernel_abs_path):
                    # Create directory
                    create_directory(kernel_abs_path)
                    # Copy logos
                    copy_logos(img_location, logo_name_srt, kernel_abs_path)
                    # Create kernel.json
                    create_kernel_json_file(display_name, language, script,
                                            interpreter, connection_file,
                                            remote_host, kernel_abs_path)
                    print(messages["_installed"] % kernel_name)
                else:
                    print(messages["_delete"] % kernel_name)
                    answer = raw_input()
                    answer_lower = answer.lower()
                    if ((answer_lower == 'y') or (answer_lower == 'yes') or
                            (answer_lower == 'yep')):
                        args.kernel_names = [kernel_name]
                        uninstall_kernel(args)
                        install_kernel(args)
    else:
        print(messages["_error_NoRoot"])
        exit(1)

def main():
    """Main function"""

    create_dictionaries()
    args = parse_command_line_args()
    args.function_name(args)

def parse_command_line_args():
    """Parse command line arguments"""

    # Create top parser
    parser = ArgumentParser(prog="rk", description=argparse["_parser"],
                            add_help=True)
    parser.add_argument("-v", "--version", action="version", version="rk 0.2a")
    # Create subparsers for the top parser
    subparsers = parser.add_subparsers(title=argparse["_subparsers"])
    # Create the parser for the "list" subcommand
    parser_list = subparsers.add_parser("list",
            description=argparse["_parser_list"],
            help=argparse["_parser_list"])
    parser_list.set_defaults(function_name=show_kernels_list)
    # Create the parser for the "install" subcommand
    parser_install = subparsers.add_parser("install",
            description=argparse["_parser_install"],
            help=argparse["_parser_install"])
    parser_install.add_argument("kernel_names", action="store", nargs='+',
                                metavar="KERNEL_NAME")
    parser_install.set_defaults(function_name=install_kernel)
    # Create the parser for the "install-template" subcommand
    parser_install_template = subparsers.add_parser("install-template",
            description=argparse["_parser_install_template"],
            help=argparse["_parser_install_template"])
    parser_install_template.set_defaults(function_name=install_kernel,
                                         kernel_names=None)
    # Create the parser for the "install-all" subcommand
    parser_install_all = subparsers.add_parser("install-all",
            description=argparse["_parser_install_all"],
            help=argparse["_parser_install_all"])
    parser_install_all.set_defaults(function_name=install_all)
    # Create the parser for the "uninstall" subcommand
    parser_uninstall= subparsers.add_parser("uninstall",
            description=argparse["_parser_uninstall"],
            help=argparse["_parser_uninstall"])
    parser_uninstall.add_argument("kernel_names", action="store", nargs='+',
                                  metavar="KERNEL_NAME")
    parser_uninstall.set_defaults(function_name=uninstall_kernel)
    # Create the parser for the "uninstall-template" subcommand
    parser_uninstall_template = subparsers.add_parser("uninstall-template",
            description=argparse["_parser_uninstall_template"],
            help=argparse["_parser_uninstall_template"])
    parser_uninstall_template.set_defaults(function_name=uninstall_kernel,
                                           kernel_names=None)
    # Create the parser for the "uninstall-all" subcommand
    parser_uninstall_all = subparsers.add_parser("uninstall-all",
            description=argparse["_parser_uninstall_all"],
            help=argparse["_parser_uninstall_all"])
    parser_uninstall_all.set_defaults(function_name=uninstall_all)
    if len(argv) == 1:
        parser.print_help()
        exit(0) # Clean exit without any errors/problems
    return parser.parse_args()

def show_kernels_list(args):
    """Show list of remote jupyter kernels from kernels dict"""

    config = ConfigObj(config_rk_abs_path)
    config_kernels_rel_path = config["config_kernels_rel_path"]
    config_kernels_abs_path = join(module_location, config_kernels_rel_path)
    # Load kernels.json file
    with open(config_kernels_abs_path) as f:
        kernels_dict = load(f)
    # Create kernels list from kernels dict
    kernels_list = [k for k in kernels_dict.keys()]
    # Sort kernels list
    kernels_list.sort()
    # Print kernels list
    for kernel in kernels_list:
         print("%s (display name: \"%s\")" % (kernel,
                 kernels_dict[kernel]["display_name"]))

def uninstall_all(args):
    """Uninstall all jupyter kernels from kernels location"""

    if getuid() == 0:
        config = ConfigObj(config_rk_abs_path)
        kernels_location = config["kernels_location"]
        kernel_names = []
        for element in listdir(kernels_location):
            element_abs_path = join(kernels_location, element)
            if isdir(element_abs_path):
                rmtree(element_abs_path, ignore_errors=True)
                kernel_names.append(element)
        kernel_names.sort()
        if len(kernel_names) == 0:
            print(messages["_uninstalled_all_zero"])
        elif len(kernel_names) == 1:
            print(messages["_uninstalled_all"] % kernel_names[0])
        else:
            print(messages["_uninstalled_all_multiple"] %
                    '\' \''.join(kernel_names))
    else:
        print(messages["_error_NoRoot"])
        exit(1)

def uninstall_kernel(args):
    """Uninstall remote jupyter kernel/kernels"""

    if getuid() == 0:
        config = ConfigObj(config_rk_abs_path)
        kernels_location = config["kernels_location"]
        kernel_names = args.kernel_names
        if kernel_names == None:
            # Uninstall template of remote kernel
            kernel_name = config["kernel_name"]
            kernel_abs_path = join(kernels_location, kernel_name)
            if exists(kernel_abs_path):
                if isdir(kernel_abs_path):
                    rmtree(kernel_abs_path, ignore_errors=True)
                elif isfile(kernel_abs_path):
                    remove(kernel_abs_path)
                print(messages["_uninstalled_template"])
            else:
                print(messages["_error_NoTemplate"])
                exit(1)
        else:
            # Uninstall kernel/kernels
            # Check kernel_names list/
            no_kernel_names = []
            for kernel_name in kernel_names:
                kernel_abs_path = join(kernels_location, kernel_name)
                if not exists(kernel_abs_path):
                    no_kernel_names.append(kernel_name)
            if len(no_kernel_names) != 0:
                if len(no_kernel_names) == 1:
                    print(messages["_error_NoKernel"] % kernel_name)
                else:
                     print(messages["_error_NoKernels"] %
                             '\' \''.join(no_kernel_names))
                exit(1)
            # /Check kernel_names list
            for kernel_name in kernel_names:
                kernel_abs_path = join(kernels_location, kernel_name)
                if isdir(kernel_abs_path):
                    rmtree(kernel_abs_path, ignore_errors=True)
                elif isfile(kernel_abs_path):
                    remove(kernel_abs_path)
                print(messages["_uninstalled"] % kernel_name)
    else:
        print(messages["_error_NoRoot"])
        exit(1)

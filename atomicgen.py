#!/usr/bin/env python
import os
import re


CURR_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURR_DIR)
PYNE_DIR = os.path.join(ROOT_DIR, "pyne")
MASS_FILE = os.path.join(PYNE_DIR, "dbgen", "mass.mas16")
ABUN_FILE = os.path.join(PYNE_DIR, "dbgen", "abundances.txt")


AUTOGEN_WARNING = """/*
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!! This file has been autogenerated, modify atomicgen.py !!!!!!!!!!
!!!!!!          DO NOT MODIFY THIS FILE BY HAND!!            !!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
*/
"""


def write_if_diff(filename, contents, verbose=True):
    """Only writes the file if it is different. This prevents touching the file needlessly."""
    if not os.path.isfile(filename):
        existing = None
    else:
        with open(filename, "r") as f:
            existing = f.read()
    if contents == existing:
        if verbose:
            print(filename + " generated is the same as existing file, skipping.")
        return
    with open(filename, "w") as f:
        if verbose:
            print("Writing", filename)
        f.write(contents)


def generate_header():
    """Creates the header file."""
    header_file = AUTOGEN_WARNING
    header_file += "/// /file atomic_nuclear_data.h\n"
    header_file += "/// /author Andrew Davis (andrew.davis@wisc.edu)\n"
    header_file += "///\n"
    header_file += (
        "/// /brief Implements all the fundamental atomic & nuclear data data\n"
    )
    header_file += "#include <map>\n"
    header_file += "\n"
    header_file += "namespace pyne\n"
    header_file += "{\n"
    header_file += (
        "  /// main function to be called when you wish to load the nuclide data \n"
    )
    header_file += "  /// into memory \n"
    header_file += "  void _load_atomic_mass_map_memory();\n"
    header_file += "  /// function to create mapping from nuclides in id form\n"
    header_file += "  /// to their atomic masses\n"
    header_file += "  \n"
    header_file += "  void _insert_atomic_mass_map();\n"
    header_file += "  \n"
    header_file += "  /// function to create mapping from nuclides in id form \n"
    header_file += "  /// to their natural abundances\n"
    header_file += "  void _insert_abund_map();\n"
    header_file += "  \n"
    header_file += (
        "  /// Mapping from nuclides in id form to their natural abundances\n"
    )
    header_file += "  extern std::map<int,double> natural_abund_map;\n"
    header_file += "  \n"
    header_file += "  /// Mapping from nuclides in id form to their atomic masses.\n"
    header_file += "  extern std::map<int,double> atomic_mass_map;\n"
    header_file += "  \n"
    header_file += (
        "  /// Mapping from nuclides in id form to the associated error in \n"
    )
    header_file += "  /// abdundance \n"
    header_file += "  extern std::map<int,double> atomic_mass_error_map;\n"
    header_file += "} // namespace pyne\n"
    return header_file


def generate_atomic_mass_errors():
    """Generate the mass errors"""
    atomic_mass_error = ""
    amdc_regex = re.compile(
        "[ \d-]*? (\d{1,3})[ ]{1,4}(\d{1,3}) [A-Z][a-z]? .*? "
        "(\\d{1,3}) ([ #.\d]{5,12}) ([ #.\d]+)[ ]*?$"
    )
    with open(MASS_FILE, "r") as f:
        for line in f:
            m = amdc_regex.search(line)
            if m is None:
                continue
            nuc = (10000000 * int(m.group(1))) + (10000 * int(m.group(2)))
            error = 1e-6 * float(m.group(5).strip().replace("#", ""))
            atomic_mass_error = (
                "  atomic_mass_error[" + str(nuc) + "] = " + str(error) + ";\n"
            )
    return atomic_mass_error


def generate_atomic_mass():
    """Generate atomic masses"""
    atomic_mass = ""
    amdc_regex = re.compile(
        "[ \d-]*? (\d{1,3})[ ]{1,4}(\d{1,3}) [A-Z][a-z]? .*? "
        "(\\d{1,3}) ([ #.\d]{5,12}) ([ #.\d]+)[ ]*?$"
    )
    with open(MASS_FILE, "r") as f:
        for line in f:
            m = amdc_regex.search(line)
            if m is None:
                continue
            nuc = (10000000 * int(m.group(1))) + (10000 * int(m.group(2)))
            mass = float(m.group(3)) + 1e-6 * float(m.group(4).strip().replace("#", ""))
            atomic_mass += "  atomic_mass_map[" + str(nuc) + "] = " + str(mass) + ";\n"
    return atomic_mass


def generate_abundances():
    """Generate abundances"""
    isotopic_abundances = ""
    with open(ABUN_FILE, "r") as f:
        for line in f:
            # tokenise the line
            splitted = line.split(" ")
            tokens = []
            for item in splitted:
                if item != "":
                    tokens.append(item)
                    # ignore the comment line
            if tokens[0] != "#":
                tokens[3] = tokens[3].replace("\n", "")
                isotopic_abundances += (
                    "  natural_abund_map["
                    + str((int(tokens[0]) * 10000000) + (int(tokens[2]) * 10000))
                    + "] = "
                    + str(tokens[3])
                    + ";\n"
                )
    return isotopic_abundances


def generate_cpp():
    """Generates the source file."""
    cpp_file = AUTOGEN_WARNING
    cpp_file += "// Implements basic nuclear data functions.\n"
    cpp_file += "#ifndef PYNE_IS_AMALGAMATED\n"
    cpp_file += '#include "atomic_data.h"\n'
    cpp_file += '#include "nucname.h"\n'
    cpp_file += "#endif\n"
    cpp_file += "  \n"
    cpp_file += "void pyne::_load_atomic_mass_map_memory() { \n"
    cpp_file += "  // header version of atomic weight table data \n"
    cpp_file += "  //see if the data table is already loaded\n"
    cpp_file += "  if(!atomic_mass_map.empty()) {\n"
    cpp_file += "    return;\n"
    cpp_file += "  } else { \n"
    cpp_file += "    _insert_atomic_mass_map();\n"
    cpp_file += "  }\n"
    cpp_file += "  //see if the data table is already loaded\n"
    cpp_file += "  if(!natural_abund_map.empty()) {\n"
    cpp_file += "    return;\n"
    cpp_file += "  } else { \n"
    cpp_file += "    _insert_abund_map();\n"
    cpp_file += "  }\n"
    cpp_file += "  // calculate the atomic_masses of the elements \n"
    cpp_file += "  std::map<int,double> :: iterator it;\n"
    cpp_file += "  \n"
    cpp_file += "  for (int z = 1; z <= 92 ; z++) {\n"
    cpp_file += "  // loop through the natural abundance map\n"
    cpp_file += "  double element_atomic_weight = 0.0;\n"
    cpp_file += "  for (it = natural_abund_map.begin(); it != natural_abund_map.end() ; ++it){\n"
    cpp_file += "   // if the atomic number of the abudance matches the\n"
    cpp_file += "   // that of index\n"
    cpp_file += "   if(pyne::nucname::znum(it->first) == z) {\n"
    cpp_file += "      // take atomic abundance and multiply by mass\n"
    cpp_file += (
        "      // to get the mass of that nuclide / 100 since abundance is in %\n"
    )
    cpp_file += "      element_atomic_weight += (it->second*atomic_mass_map[it->first]/100.0);\n"
    cpp_file += "    }\n"
    cpp_file += "  }\n"
    cpp_file += "  // insert the abundance of the element into the list\n"
    cpp_file += "  atomic_mass_map[z*10000000] = element_atomic_weight;\n"
    cpp_file += " }\n"
    cpp_file += "}\n"
    cpp_file += "\n\n"
    cpp_file += "void pyne::_insert_atomic_mass_map() { \n"
    cpp_file += generate_atomic_mass()
    cpp_file += "}\n"
    cpp_file += "\n\n"
    cpp_file += "void pyne::_insert_abund_map() { \n"
    cpp_file += generate_abundances()
    cpp_file += "}\n"
    return cpp_file


def main(args=()):
    """Entry point for atomic data."""
    header = generate_header()
    source = generate_cpp()
    write_if_diff("atomic_data.h", header)
    write_if_diff("atomic_data.cpp", source)


if __name__ == "__main__":
    main()

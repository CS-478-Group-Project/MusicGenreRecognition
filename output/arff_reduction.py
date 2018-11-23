from __future__ import (absolute_import, division, print_function, unicode_literals)

import random
import math
import numpy as np
import re
import sys
import os
from functools import reduce

class Matrix:
    """
    Copy lol
    """

    data = []
    attr_names = []
    str_to_enum = []        # array of dictionaries
    enum_to_str = []        # array of dictionaries
    dataset_name = "Untitled"
    MISSING = float("infinity")

    features_to_remove = [] # What features we should NOT write out

    def __init__(self, matrix=None, row_start=None, col_start=None, row_count=None, col_count=None, arff=None):
        """
        If matrix is provided, all parameters must be provided, and the new matrix will be
        initialized with the specified portion of the provided matrix.
        """
        if arff:
            self.load_arff(arff)
        elif matrix:
            self.init_from(matrix, row_start, col_start, row_count, col_count)

    def add_feature_to_remove(self, feature):
        if feature < 0 or feature >= len(self.attr_names) - 1:
            raise ValueError("Feature number is out of range! " + str(feature))
        if feature in self.features_to_remove:
            raise ValueError("Feature already set to remove! [{}]".format(str(self.attr_names[feature])))
        if len(self.features_to_remove) >= (len(self.attr_names) - 2):
            raise ValueError("Cannot add feature, must retain at least one feature for output.  Selected to remove: " + str(self.features_to_remove))

        # print("Adding feature [{}] to elimiation list.".format(self.attr_names[feature]))

        self.features_to_remove.append(feature)


    def reset_features_to_remove(self):
        self.features_to_remove = []

    @property
    def rows(self):
        """Get the number of rows in the matrix"""
        return len(self.data)

    @property
    def cols(self):
        """Get the number of columns (or attributes) in the matrix"""
        return len(self.attr_names)

    def get_features_to_remove(self):
        return self.features_to_remove

    def row(self, n):
        """Get the specified row"""
        return self.data[n]

    def col(self, n):
        """Get the specified column"""
        return [row[n] for row in self.data]

    def get(self, row, col):
        """
        Get the element at the specified row and column
        :rtype: float
        """
        return self.data[row][col]

    def get_attr_info(self, attr_index):
        if attr_index < 0 or attr_index >= len(self.attr_names):
            return "Invalid Attribute Number!"
        else:
            return "#{} - [{}]".format(attr_index, self.attr_names[attr_index])


    def load_arff(self, filename):
        """Load matrix from an ARFF file"""
        self.data = []
        self.attr_names = []
        self.str_to_enum = []
        self.enum_to_str = []
        self.features_to_remove = []
        reading_data = False

        rows = []           # we read data into array of rows, then convert into array of columns

        f = open(filename)
        for line in f.readlines():
            line = line.rstrip()
            if len(line) > 0 and line[0] != '%':
                if not reading_data:
                    if line.lower().startswith("@relation"):
                        self.dataset_name = line[9:].strip()
                    elif line.lower().startswith("@attribute"):
                        attr_def = line[10:].strip()
                        if attr_def[0] == "'":
                            attr_def = attr_def[1:]
                            attr_name = attr_def[:attr_def.index("'")]
                            attr_def = attr_def[attr_def.index("'")+1:].strip()
                        else:
                            search = re.search(r'(\w*)\s+({.*}|\w+)', attr_def)
                            attr_name = search.group(1)
                            attr_def = search.group(2)
                            # Remove white space from atribute values
                            attr_def = "".join(attr_def.split())

                        self.attr_names += [attr_name]

                        str_to_enum = {}
                        enum_to_str = {}
                        if not(attr_def.lower() == "real" or attr_def.lower() == "continuous" or attr_def.lower() == "integer"):
                            # attribute is discrete
                            assert attr_def[0] == '{' and attr_def[-1] == '}'
                            attr_def = attr_def[1:-1]
                            attr_vals = attr_def.split(",")
                            val_idx = 0
                            for val in attr_vals:
                                val = val.strip()
                                enum_to_str[val_idx] = val
                                str_to_enum[val] = val_idx
                                val_idx += 1

                        self.enum_to_str.append(enum_to_str)
                        self.str_to_enum.append(str_to_enum)

                    elif line.lower().startswith("@data"):
                        reading_data = True

                else:
                    # reading data
                    row = []
                    val_idx = 0
                    # print("{}".format(line))
                    vals = line.split(",")
                    for val in vals:
                        val = val.strip()
                        if not val:
                            raise Exception("Missing data element in row with data '{}'".format(line))
                        else:
                            row += [float(self.MISSING if val == "?" else self.str_to_enum[val_idx].get(val, val))]

                        val_idx += 1

                    rows += [row]

        f.close()
        self.data=rows



    def value_count(self, col):
        """
        Get the number of values associated with the specified attribute (or columnn)
        0=continuous, 2=binary, 3=trinary, etc.
        """
        return len(self.enum_to_str[col]) if len(self.enum_to_str) > 0 else 0


    def print(self):
        print("\n@RELATION {}".format(self.dataset_name))
        print("- ATTRIBUTES -")

        # Display our attributes
        for i in range(len(self.attr_names) - 1):   # -1 to not print the class
            print(str(i) + ") {}".format(self.attr_names[i]), end="")
            if self.value_count(i) == 0:
                print(" CONTINUOUS")
            else:
                print(" {{{}}}".format(", ".join(self.enum_to_str[i].values())))


    def write_to_file(self, file_name):
        #self.features_to_remove
        with open(file_name, 'w') as fout:
            fout.write("@RELATION {}\n".format(self.dataset_name))

            # Write out the attributes, but only the ones we care about
            for i in range(len(self.attr_names)):
                if i in self.features_to_remove: continue                   # Skip features that we decided to remove
                # Write attribute name
                fout.write("@ATTRIBUTE {}".format(self.attr_names[i]))

                # Print out the values!
                if self.value_count(i) == 0:
                    fout.write(" CONTINUOUS\n")
                else:
                    fout.write(" {{{}}}\n".format(", ".join(self.enum_to_str[i].values())))

            fout.write("@DATA\n")
            for i in range(self.rows):
                r = self.row(i)

                values = []
                for j in range(len(r)):
                    if j in self.features_to_remove: continue               # Same bruh
                    # Determine what we should write for the value
                    if self.value_count(j) == 0:
                        values.append(str(r[j]))
                    else:
                        values.append(self.enum_to_str[j][r[j]])

                fout.write("{}\n".format(", ".join(values)))



def print_commands():
    # Print out the api
    print("\n************************************")
    print(" Arff Feature Reduction")
    print(" ----------------------")
    print(" # #...  - select features to remove")
    print(" w       - quit and write to file")
    print(" x       - quit without writing")
    print(" r/c     - clear selected features ")
    print(" p       - print original arff header")
    print(" h/a     - print commands")
    print("*************************************\n")


if len(sys.argv) < 3:
    print("\n***Not enough arguments supplied... exiting.")
    print("Usage:        python " + __file__ + " source_file destination_file")
    exit()

# We have enough arguments, let's move on
source_file = sys.argv[1]
destination_file = sys.argv[2]

if not os.path.exists(source_file):
    raise ValueError("Source file does not exist! [{}]".format(source_file) )
if not re.search(r'\.arff$', destination_file):
    raise ValueError("Please supply a valid destination filename (ends with .arff)")


original_matrix = Matrix()
original_matrix.load_arff(source_file)

print_commands()

# Print out the original data
original_matrix.print()
print()


# Start main input loop
while True:
    user_input = ""
    # Input loop, waits for valid entry
    while True:
        user_input = input("Please enter an attribute number or command: ")
        user_input = user_input.strip()
        if len(user_input) > 0: break

    # Split pieces (to accommodate multiple feature entries on one line)
    user_input = user_input.split()

    if len(user_input) == 1 and user_input[0].isalpha():    # They entered a command
        user_input = user_input[0]                          # Extract the command

        # Handle API
        user_input = user_input.lower()
        if user_input in "w":
            print("Writing to output file: {}".format(destination_file))
            original_matrix.write_to_file(destination_file)
            print("Finished... Quitting")
            exit()
        elif user_input in "x":
            print("Exiting...")
            exit()
        elif user_input in "rc":
            print("Clearing selected features")
            original_matrix.reset_features_to_remove()
            continue
        elif user_input in "p":
            original_matrix.print()
            continue
        elif user_input in "helpa":
            print_commands()
            continue
        else:
            print("Unrecognized command {}".format(user_input))
            print("Enter \'h\' for help.")
            continue

    # Check to see if they entered all numbers
    if reduce((lambda x, y: x and y.isdigit() and not '.' in y), user_input):
        print()
        # Handle feature removal
        user_input = [int(val) for val in user_input]
        description = [original_matrix.get_attr_info(index) for index in user_input]

        for feature in user_input:
            try:
                original_matrix.add_feature_to_remove(feature)
                print("Removing feature: {}".format(original_matrix.get_attr_info(feature)))
            except ValueError as e:
                print(e)
    else:
        print("Invalid Feature Selection Format!")

    print("Currently Selected Features: " + str(original_matrix.get_features_to_remove()))
    print()

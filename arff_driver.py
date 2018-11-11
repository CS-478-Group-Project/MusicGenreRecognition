import os
import Andrew
import Jacob
import Chandra
import Gibson



def write_header():
    with open(os.path.join(OUTPUT_DIR ,OUTPUT_FILE), 'w') as fout:
        fout.write("% 1. Title: Music database for genre classification.\n%\n%\n%")
        fout.write("@relation music\n\n")
    return


'''
Writes the header information to the destination file
'''
def write_attributes(attributes, output_classes):
    with open(os.path.join(OUTPUT_DIR ,OUTPUT_FILE), 'a') as fout:
        # All attributes are continuous, as far as we've decided... This can easily be modified to accommodate nominal data
        for attribute in attributes:
            fout.write("@attribute ")
            fout.write(attribute)
            fout.write(" continuous\n")

        # Write the output class data
        fout.write("@attribute genre {")
        fout.write(','.join(genres))
        fout.write("}\n\n")

        # Start the data block
        fout.write("@data")

    return


'''
Given a list of instances for a genre, writes the instance data to the output file.
Assumes header data has already been written
'''
def append_instances(instances, genre):
    # Open output file in append mode.
    with open(os.path.join(OUTPUT_DIR ,OUTPUT_FILE), 'a') as fout:
        fout.write(','.join(instances))     # Write the data
        fout.write(',' + genre)             # Give output class
        fout.wrtie('\n')                    # new line

    return


# Define some values
OUTPUT_DIR = 'output'
OUTPUT_FILE = 'music.arff'

# Define genres
genres = ['pop', 'electronic', 'rap', 'folk', 'rock', 'classical']

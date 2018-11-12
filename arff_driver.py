import os
import random
from scipy.io import wavfile
from scipy.fftpack import fft,fftfreq   # Likely won't be needed
from Andrew import Andrew
from Jacob import Jacob
from Chandra import Chandra
from Gibson import Gibson


'''
Writes the header data for the arff file
Most of this header data isn't that important, it's really only for human readability
Nevertheless, we have a cool function here to handle the job
'''
def write_header():
    with open(os.path.join(OUTPUT_DIR ,OUTPUT_FILE), 'w') as fout:
        fout.write("% 1. Title: Music database for genre classification.\n%\n%\n%\n")
        fout.write("@relation music\n\n")
    return


'''
Writes the header information to the destination file
'''
def write_attributes(attributes):
    with open(os.path.join(OUTPUT_DIR ,OUTPUT_FILE), 'a') as fout:
        # All attributes are continuous, as far as we've decided... This can easily be modified to accommodate nominal data
        for attribute in attributes:
            fout.write("@attribute ")
            fout.write(attribute)
            fout.write(" continuous\n")

        # Write the output class data
        fout.write("@attribute genre {")
        fout.write(', '.join(genres))
        fout.write("}\n\n")

        # Start the data block
        fout.write("@data\n")

    return


'''
Given a list of instances for a genre, writes the instance data to the output file.
Assumes header data has already been written
'''
def append_instances(instances, genre):
    # Open output file in append mode.
    with open(os.path.join(OUTPUT_DIR ,OUTPUT_FILE), 'a') as fout:
        for instance in instances:
            fout.write(', '.join(str(feature_val) for feature_val in instance))  # Write the data
            fout.write(', ' + genre + '\n')                                      # Give output class

    return

def output_data(attributes, instance_data, genres):
    # Make sure our output directory is safe
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    write_header()
    write_attributes(attributes)

    # Main output loop
    for genre in genres:
        append_instances(instance_data[genre], genre)

def get_attributes(extraction_modules):
    # Define a list of attributes
    attributes = []

    for module in extraction_modules:
        attributes.extend(str(module).split())  # Add the module-defined attributes to our list

    return attributes


def get_random_sample(data, sample_rate):
    # Find how long the song is in seconds
    total_length = data.shape[0] / sample_rate
    # Pick a random starting time in seconds
    start_time = random.randint(0, int(total_length - SAMPLE_LENGTH))

    # Feed back the data as a sample given our random start time and constant sample length
    return data[start_time * sample_rate:(start_time + SAMPLE_LENGTH) * sample_rate]


def extract_instance(sample, data, sample_rate, extraction_modules):
    features = []

    # For every module
    for module in extraction_modules:
        # Extend our list with the data from each module
        features.extend(module.extract(sample, data))   # Also want to add sample rate here... will be needed for many things

    return features



# Define some values
OUTPUT_DIR = 'output'           # Output directory
OUTPUT_FILE = 'music.arff'      # Specific file name we're writing to

SONG_DIR = ['res', 'songs']     # Where the subfolders for each genre are stored

SAMPLE_LENGTH = 8               # Length of samples to be used
NUM_SAMPLES = 1                 # How many samples should be extracted from each file

# Define genres
genres = ['pop', 'electronic', 'rap', 'folk', 'rock', 'classical']

# Where we'll store all the computed output data
instance_data = dict()


# Let's not forget to grab our labels
# Here we also need to establish the order of extraction
attributes = []
extraction_modules = [Andrew(), Jacob(), Chandra(), Gibson()]

attributes = get_attributes(extraction_modules)


# The following could be refactored a bit more, but I kind of just want to test things

# Feature extraction loop
# Iterate over each genre
for genre in genres:
    current_instances = []

    # Link to the current resource directory
    current_dir = os.path.join(*SONG_DIR, genre)

    if not os.path.isdir(current_dir): continue   # Skip this genre if not defined

    # Loop over every file in the song directory
    for file in os.listdir(current_dir):
        # Read in audio data and sanitize
        sample_rate, data = wavfile.read(os.path.join(*SONG_DIR, genre, file))

        # Convert to mono
        data = data[:,0]

        for i in range(NUM_SAMPLES):
            # Obtain a random sample
            sample = get_random_sample(data, sample_rate)

            # Sanity check on sample length
            assert (sample.shape[0] == (SAMPLE_LENGTH * sample_rate))

            current_instances.append(extract_instance(sample, data, sample_rate, extraction_modules))
        # End sample loop
    # End directory loop

    # Save the data in a cool dictionary
    instance_data[genre] = current_instances


# Time to do some output!
output_data(attributes, instance_data, genres)

# Done lol

# MusicGenreRecognition
Machine learning project on music genre recognition

# Driver
Driver will iterate through all songs. For each song, it will call extract() on each of our classes. It will take the returned features and concatenate them to a list of all features for that song. It will add this list as a row to the .arff file
- The arguments for extract will be (song section, full song, sampling rate)
    - song section: section of current songs .wav file
    - full song: full .wav file for current song
    - sampling rate: integer that corresponds to the number of samples per second of the .wav file
- The driver will extract the features by calling split(",") on the returned string from str(FeatureClassName)

# Feature extraction classes
Each class will include
- extract() function as described above
    - It will return a list of features, each lining up with its corresponding name in the string function below
- __str__() function that returns each feature name separated by commas
    - e.g. "Tempo, Spectral Centroid, RMSE, ..."

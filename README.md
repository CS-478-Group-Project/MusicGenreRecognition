# MusicGenreRecognition
Machine learning project on music genre recognition

# Driver
Driver will iterate through all songs. For each song, it will call execute() on each of our classes. It will take the returned features and concatenate them to a list of all features for that song. It will add this list as a row to the .arff file
- The arguments for execute will be (full song, song section, sampling rate)
- The driver will extract the features by calling split(",") on the returned string from Str(FeatureClassName)

# Feature extraction classes
Each class will include
- execute() function as described above
    - It will return a list of features, each lining up with its corresponding name in the string function below
- __str__() function that returns each feature name separated by commas
    - e.g. "Tempo, Spectral Centroid, RMSE, ..."

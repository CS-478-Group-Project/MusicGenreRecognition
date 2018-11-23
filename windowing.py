import numpy as np

def overlapped_window(data, window_size, overlap_rate):
    X = []
    read_head = 0
    while True:
        # Either read the full window size, or only a portion of the overlap rate
        read_size = window_size if len(X) == 0 else window_size // overlap_rate
        # handle OOB
        if read_head + read_size > len(data):
            raise StopIteration()
        # Read a window into our data :)
        x = data[read_head:(read_head) + read_size]
        # Move the head up
        read_head += read_size
        # Extend our working window to be a full sample
        X.extend(x)
        # produce the value!
        # yield np.array(X)
        yield X

        # Trim for the next iteration
        X = X[window_size//overlap_rate:]

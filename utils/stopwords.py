import numpy as np

def stop_words_en():
    stops = np.loadtxt('./dictionaries/stop_words_en.txt', dtype=str)
    return stops

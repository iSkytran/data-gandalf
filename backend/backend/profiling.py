
import pickle
from backend import config
from pathlib import Path


with open(Path(config.MODEL_PATH), 'rb') as file:
    model = pickle.load(file)
    count = 0
    max_best = 0
    min_best = 1

    min_10 = 1
    max_10 = 0
    for id, list in model.items():
        if list[0][0] > max_best:
            print("ID:", id)
            print(list[:10])
            print("")
        max_best = max(max_best, list[0][0])
        min_best = min(min_best, list[0][0])

        min_10 = min(min_10, list[9][0])
        max_10 = max(max_10, list[9][0])
    print("Max best:", max_best)
    print("Min best:", min_best)

    print("Max 10:", max_10)
    print("Min 10:", min_10)
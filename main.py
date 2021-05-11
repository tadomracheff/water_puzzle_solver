import glob
import os
from threading import Thread
from game import *


if __name__ == '__main__':
    # flasks = game_init([[1, 2], [2, 1]], 1, 2)
    # flasks = game_init([[1, 2, 3], [2, 1, 3], [2, 1, 3]], 2, 3)
    flasks = game_init([[1, 1, 1, 2], [3, 4, 1, 3], [3, 2, 2, 3], [2, 4, 4, 4]], 2, 4)
    # flasks = game_init([[4,12,2,3],[1,9,5,7],[5,11,4,9],[3,11,1,10],[5,8,10,9],[5,12,9,3],[2,12,7,6],[1,6,7,11],[8,8,7,4],[6,10,11,2],[12,4,3,2],[1,10,6,8]], 2, 4)
    # flasks = game_init([[1,2,2,3],[4,2,5,6],[7,8,8,8],[3,7,9,4],[10,1,6,5],[3,9,11,1],[11,12,8,1],[4,12,9,10],[11,4,3,6],[5,2,5,12],[7,7,6,10],[11,12,10,9]], 2, 4)
    # flasks = game_init([[1, 2, 3, 4], [2, 1, 3, 4], [2, 1, 3, 4], [4, 2, 1, 3]], 2, 4)
    # flasks = game_init([[1, 1, 1, 2], [1, 3, 2, 4], [4, 2, 4, 3], [3, 4, 3, 5], [2, 5, 5, 5]], 2, 4)

    files = glob.glob('solution/*')
    for f in files:
        os.remove(f)

    show(flasks)
    root = Tree(flasks)

    set_node(root, flasks)

    threads = list()
    for child in root.children:
        threads.append(Thread(target=do, args=(child,)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


import scipy.spatial as sp
import numpy as np
import cv2

main_colors = [
    (0,0,0),
    (255,255,255),
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (255,255,0),
    (0,255,255),
    (255,0,255),
] 

emojis = [
    ":black_square:",
    ":white_square:",
    ":apple:",
    ":green_salad:",
    ":blueberry:",
    ":sunny:",
    ":mint_heart:",
    ":eggplant:",
]

color_tree = sp.KDTree(main_colors)

# Find the closest RGB vector by way of KDTree
# and map it to the appropriately-colored emoji
def find_emoji(color):
    _, result = color_tree.query(color)
    return emojis[result]

def emojify(path, w=12, h=12):
    im = cv2.imread(path)
    im = cv2.resize(im, size)
    slack_string = ""

    for i in range(0, w - 1):
        for j in range(0, h - 1):
            slack_string += find_emoji(im[i,j])
            slack_string += " "
        slack_string += "\n"

    return slack_string

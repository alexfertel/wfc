#!/usr/bin/python3
import sys
import imageio as im
from ast import literal_eval as make_tuple


def read(path):
    image = im.imread(path)
    # N, M, _ = image.shape

    # colors = []
    # for i in range(N):
    #     for j in range(M):
    #         colors.append(image[i][j])

    # colors = np.lib.arraysetops.unique(colors, axis=0)
    # # print(colors)
    # c2i = {tuple(color): index for index, color in enumerate(colors)}
    # i2c = {index: tuple(color) for index, color in enumerate(colors)}

    # sample = [[0 for _ in range(M)] for _ in range(N)]
    # for i in range(N):
    #     for j in range(M):
    #         sample[i][j] = c2i[tuple(image[i][j])]

    # print('Sample:')
    # pprint(sample)

    return image
    # return sample


def swap(old, new, image):
    N, M, _ = image.shape

    for i in range(N):
        for j in range(M):
            if (image[i][j] == old).all():
                image[i][j] = new

    return image


def save(image, path):
    im.imwrite(path, image)


if len(sys.argv) != 5:
    print(
        "Usage: python swapper.py path/to/image path/to/output old_color new_color \nExample: python swapper.py ../images/Flowers1.png ../images/Flowers2.png (0, 0, 0) (0, 0, 255)")
    exit()

print(sys.argv)

image_path = sys.argv[1]
output_path = sys.argv[2]
old_color = make_tuple(sys.argv[3])
new_color = make_tuple(sys.argv[4])
image = read(image_path)

# print(image)

new_image = swap(old_color, new_color, image)

# print(new_image)
save(new_image, output_path)

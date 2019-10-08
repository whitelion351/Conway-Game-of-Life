import random
from time import sleep
from PIL import Image
import numpy as np
import cv2

born_rules = [3]
survive_rules = [2, 3]
world_size_x = 100
world_size_y = 80
view_zoom = 5
sparsity = 5
max_pixel = 255.0
min_pixel = 0.0


def create_array_for_letter(letter=None):
    if letter is None or len(letter) != 1:
        print("you need to pass a string of length 1 to this method")
        raise TypeError
    else:
        letter = letter.upper()
        i = 255
        if letter == "A":
            return [
                [0, i, i, i, 0],
                [i, 0, 0, 0, i],
                [i, i, i, i, i],
                [i, 0, 0, 0, i],
                [i, 0, 0, 0, i]
            ]
        elif letter == "B":
            return [
                [i, i, i, i, 0],
                [i, 0, 0, 0, i],
                [i, i, i, i, 0],
                [i, 0, 0, 0, i],
                [i, i, i, i, 0]
            ]
        elif letter == "C":
            return [
                [0, i, i, i, 0],
                [i, 0, 0, 0, i],
                [i, 0, 0, 0, 0],
                [i, 0, 0, 0, i],
                [0, i, i, i, 0]
            ]
        elif letter == "E":
            return [
                [i, i, i, i, i],
                [i, 0, 0, 0, 0],
                [i, i, i, i, i],
                [i, 0, 0, 0, 0],
                [i, i, i, i, i]
            ]
        elif letter == "F":
            return [
                [i, i, i, i, i],
                [i, 0, 0, 0, 0],
                [i, i, i, i, i],
                [i, 0, 0, 0, 0],
                [i, 0, 0, 0, 0]
            ]
        elif letter == "H":
            return [
                [i, 0, 0, 0, i],
                [i, 0, 0, 0, i],
                [i, i, i, i, i],
                [i, 0, 0, 0, i],
                [i, 0, 0, 0, i]
            ]
        elif letter == "I":
            return [
                [i, i, i, i, i],
                [0, 0, i, 0, 0],
                [0, 0, i, 0, 0],
                [0, 0, i, 0, 0],
                [i, i, i, i, i]
            ]
        elif letter == "L":
            return [
                [i, 0, 0, 0, 0],
                [i, 0, 0, 0, 0],
                [i, 0, 0, 0, 0],
                [i, 0, 0, 0, 0],
                [i, i, i, i, i]
            ]
        elif letter == "N":
            return [
                [i, 0, 0, 0, i],
                [i, i, 0, 0, i],
                [i, 0, i, 0, i],
                [i, 0, 0, i, i],
                [i, 0, 0, 0, i]
            ]
        elif letter == "O":
            return [
                [0, i, i, i, 0],
                [i, 0, 0, 0, i],
                [i, 0, 0, 0, i],
                [i, 0, 0, 0, i],
                [0, i, i, i, 0]
            ]
        elif letter == "P":
            return [
                [i, i, i, i, 0],
                [i, 0, 0, 0, i],
                [i, i, i, i, 0],
                [i, 0, 0, 0, 0],
                [i, 0, 0, 0, 0]
            ]
        elif letter == "S":
            return [
                [0, i, i, i, i],
                [i, 0, 0, 0, 0],
                [0, i, i, i, 0],
                [0, 0, 0, 0, i],
                [i, i, i, i, 0]
            ]
        elif letter == "T":
            return [
                [i, i, i, i, i],
                [0, 0, i, 0, 0],
                [0, 0, i, 0, 0],
                [0, 0, i, 0, 0],
                [0, 0, i, 0, 0]
            ]
        elif letter == "U":
            return [
                [i, 0, 0, 0, i],
                [i, 0, 0, 0, i],
                [i, 0, 0, 0, i],
                [i, 0, 0, 0, i],
                [0, i, i, i, 0]
            ]
        elif letter == "V":
            return [
                [i, 0, 0, 0, i],
                [i, 0, 0, 0, i],
                [0, i, 0, i, 0],
                [0, i, 0, i, 0],
                [0, 0, i, 0, 0]
            ]
        elif letter == "W":
            return [
                [i, 0, 0, 0, i],
                [i, 0, 0, 0, i],
                [i, 0, i, 0, i],
                [i, 0, i, 0, i],
                [0, i, 0, i, 0]
            ]
        else:
            return [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ]


def create_grid(size_x=5, size_y=5, populate=True, fill_type="random_dots", fill_text=""):
    grid = np.zeros((size_x, size_y))
    if populate is True:
        if fill_type.find("random_dots") >= 0:
            choices = [x for x in range(sparsity)]
            x_center = size_x // 2
            y_center = size_y // 2
            for y in grid[x_center-5:x_center+5, :]:
                for i, x in enumerate(y):
                    if y_center - 5 < i < y_center + 5:
                        if random.choice(choices) == 1:
                            y[i] = max_pixel
        if fill_type.find("text") >= 0:
            if size_x != 5:
                spx = (size_x // 2) - 2
            else:
                spx = 0
            spy = (size_y // 2) - ((len(fill_text) // 2) * 5) - len(fill_text) // 1.35
            spy = int(spy)
            cursor = spy
            for letter in fill_text:
                print("getting array for letter", letter)
                grid[spx:spx+5, cursor:cursor+5] = create_array_for_letter(letter)
                cursor += 6

        return grid


test_text = "hip hop lives"


def next_generation(current):
    new = current.copy()
    still_active = False
    for ix, x in enumerate(current):
        for iy, y in enumerate(x):
            if ix == len(current)-1:
                x_to_check = [ix - 1, ix, 0]
            else:
                x_to_check = [ix - 1, ix, ix + 1]
            if iy == len(x)-1:
                y_to_check = [iy - 1, iy, 0]
            else:
                y_to_check = [iy - 1, iy, iy + 1]
            neighbors = 0
            for cx in x_to_check:
                for cy in y_to_check:
                    if cx == ix and cy == iy:
                        pass
                    elif current[cx, cy] == max_pixel:
                        neighbors += 1
            if current[ix, iy] == min_pixel and neighbors in born_rules:
                new[ix, iy] = max_pixel
                still_active = True
            elif current[ix, iy] == max_pixel and neighbors in survive_rules:
                new[ix, iy] = max_pixel
            else:
                new[ix, iy] = min_pixel
    return new, still_active


def show_generation(grid):
    img = Image.fromarray(grid.astype("uint8"), "L")
    img = img.resize((world_size_x*view_zoom, world_size_y*view_zoom))
    cv2.imshow("env", np.array(img))
    cv2.waitKey(1)


def switch_grid(old_grid, new_grid=None, s_type=None):
    grid = old_grid.copy()
    if s_type == "vertical wipe":
        for i, x in enumerate(grid):
            for i2, y, in enumerate(x):
                grid[i, i2] = 10
            show_generation(grid)
            sleep(0.01)
            for i2, y, in enumerate(x):
                grid[i, i2] = min_pixel if new_grid is None else new_grid[i, i2]
    else:
        return


new_world = create_grid(world_size_y, world_size_x, fill_type="random_dots", fill_text=test_text)
while True:
    world = new_world
    show_generation(world)
    show_generation(world)
    sleep(1)
    generation = 0
    final_generation = 5000
    stable_timer = 0
    stable_array = world.copy()
    while generation < final_generation:
        world, active = next_generation(world)
        show_generation(world)
        if active:
            generation += 1
            stable_timer += 1
            if generation % 100 == 0:
                stable_timer = 0
                stable_array = world.copy()
            if (stable_timer == 2 or stable_timer == 6) and generation > 100:
                if np.array_equal(world, stable_array):
                    generation = final_generation
        else:
            generation = final_generation
    show_generation(world)
    sleep(1)
    new_world = create_grid(world_size_y, world_size_x)
    switch_grid(world, new_world, s_type="vertical wipe")

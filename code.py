from PIL import Image
from random import randint
import numpy
import itertools

TARGET = Image.open("image.png").convert("1")
TARGET_WIDTH, TARGET_HEIGHT = TARGET.size

STARTING_POPULATION = 10

MUTATION_CHANCE = 10
STEPS = 2


def get_random_image():
    array = numpy.random.rand(TARGET_WIDTH, TARGET_HEIGHT)

    for x in numpy.nditer(array, op_flags=['readwrite']):
        if x > 0.5:
            x[...] = 1
        else:
            x[...] = 0

    return Image.fromarray(array)


def fitness(target, population):
    print "fitness"
    fitness_dict = {}

    # return best 10 from pop
    for i, image in enumerate(population):
        right = numpy.logical_and(numpy.array(list(target.getdata())), numpy.array(list(image.getdata())))
        fitness_dict[i] = numpy.sum(right)

    print fitness_dict.keys()
    best = sorted(fitness_dict.items(), key=fitness_dict.get, reverse=True)[:10]
    print best
    return [population[i] for i in best]


def breed(best):
    print "breed"
    # for every combination of pairs, breed 10 new pairs
    new_pop = []

    def all_pairs(lst):
        for p in itertools.permutations(lst):
            i = iter(p)
            yield zip(i, i)

    print best
    print all_pairs(best)
    for i, j in all_pairs(best):
        for y in range(1):
            new_pop.append(breed_pair(i, j))

    return new_pop


def breed_pair(image1, image2):
    # take half of one, half of other, introduce some randomness
    image1 = list(image1.getdata())
    image2 = list(image2.getdata())
    image3 = Image.new("1", (TARGET_WIDTH, TARGET_HEIGHT))

    child = image1[len(image1) / 2:] + image2[:len(image2) / 2]

    #10% chance of mutating every pixel
    for i, pixel in enumerate(child):
        if randint(0, 100) < MUTATION_CHANCE:
            child[i] = 0 if pixel else 1

    return image3.putdata(child)


if __name__ == "__main__":
    population = [get_random_image() for x in range(STARTING_POPULATION)]

    # while(fitness(population[0]) < 0.9):
    for x in range(STEPS):
        population = breed(fitness(TARGET, population))
        fitness(population)[0].show()

    population[0].show()
from PIL import Image
from random import random
import numpy
import itertools
import operator

TARGET = Image.open("image.png").convert("1")
TARGET_WIDTH, TARGET_HEIGHT = TARGET.size

STARTING_POPULATION = 100
PERCENTAGE_BEST = 0.1
NUMBER_OF_CHILDREN = 1

MUTATION_CHANCE = 0.1

REPETITIONS = 2


def get_random_image():
    array = numpy.random.rand(TARGET_WIDTH, TARGET_HEIGHT)

    for x in numpy.nditer(array, op_flags=['readwrite']):
        if x > 0.5:
            x[...] = 1
        else:
            x[...] = 0

    return Image.fromarray(array)


def fitness(target, population):
    fitness_dict = {}

    # return best 10 from pop
    for id, image in enumerate(population):
        right = numpy.logical_and(numpy.array(list(target.getdata())), numpy.array(list(image.getdata())))
        fitness_dict[id] = numpy.sum(right)

    best = sorted(fitness_dict.items(), key=operator.itemgetter(1), reverse=True)[:int(PERCENTAGE_BEST * STARTING_POPULATION)]
    print best
    return [population[i[0]] for i in best]


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
    for image1, image2 in all_pairs(best):
        for child in range(NUMBER_OF_CHILDREN):
            new_pop.append(breed_pair(image1, image2))

            #Lazy way of ensuring constant population size - this might lead to the algorithm favouring one "parent"
            #over all the others, but it'll do for now until we get some output
            if len(new_pop) == STARTING_POPULATION:
                return new_pop


def breed_pair(image1, image2):
    image1 = list(image1.getdata())
    image2 = list(image2.getdata())
    image3 = Image.new("1", (TARGET_WIDTH, TARGET_HEIGHT))

    #Currently takes top half of one image and bottom half of the other
    #In future, it should take a random selection of pixels (which can be extended to give the option of a random
    #amount too)
    child = image1[len(image1) / 2:] + image2[:len(image2) / 2]

    #10% chance of mutating every pixel
    for i, pixel in enumerate(child):
        if random() < MUTATION_CHANCE:
            child[i] = 0 if pixel else 1

    return image3.putdata(child)


if __name__ == "__main__":
    population = [get_random_image() for x in range(STARTING_POPULATION)]

    # while(fitness(population[0]) < 0.9):
    for x in range(REPETITIONS):
        population = breed(fitness(TARGET, population))
        fitness(population)[0].show()

    population[0].show()
import random
import math
import matplotlib.pyplot as plt


# Az egyes csomópontok adatainak betöltése
def loadData():
    node = []
    with open("travelpoints2.txt") as file:
        for line in file:
            node_val = line.split()
            node.append(
                [node_val[0], float(node_val[1]), float(node_val[2])]
            )
    return node

# A távolság kiszámolása
def calcDistance(nodes):
    total_sum = 0
    for i in range(len(nodes) - 1):
        nodeA = nodes[i]
        nodeB = nodes[i + 1]

        d = math.sqrt(
            math.pow(nodeB[1] - nodeA[1], 2) + math.pow(nodeB[2] - nodeA[2], 2)
        )

        total_sum += d

    nodeA = nodes[0]
    nodeB = nodes[-1]
    d = math.sqrt(math.pow(nodeB[1] - nodeA[1], 2) + math.pow(nodeB[2] - nodeA[2], 2))

    total_sum += d

    return total_sum


# Populáció kiválasztása
def selectPopulation(nodes, size):
    population = []

    for i in range(size):
        n = nodes.copy()
        random.shuffle(n)
        distance = calcDistance(n)
        population.append([distance, n])
    fittest = sorted(population)[0]

    return population, fittest


# A genetikus algoritmus
def geneticAlgorithm(population, num_of_nodes, TOURNAMENT_SELECTION_SIZE, MUTATION_RATE, CROSSOVER_RATE, TARGET, iterations=100):
    gen_number = 0
    for i in range(iterations):
        new_population = []
        # A két legjobb populáció kiválasztása
        new_population.append(sorted(population)[0])
        new_population.append(sorted(population)[1])

        for i in range(int((len(population) - 2) / 2)):
            # Keresztezés
            random_number = random.random()
            if random_number < CROSSOVER_RATE:
                parent_chromosome1 = sorted(
                    random.choices(population, k=TOURNAMENT_SELECTION_SIZE)
                )[0]

                parent_chromosome2 = sorted(
                    random.choices(population, k=TOURNAMENT_SELECTION_SIZE)
                )[0]

                point = random.randint(0, num_of_nodes - 1)

                child_chromosome1 = parent_chromosome1[1][0:point]
                for j in parent_chromosome2[1]:
                    if (j in child_chromosome1) == False:
                        child_chromosome1.append(j)

                child_chromosome2 = parent_chromosome2[1][0:point]
                for j in parent_chromosome1[1]:
                    if (j in child_chromosome2) == False:
                        child_chromosome2.append(j)

            # Ha nem történik keresztezés, akkor véletlenszerűen változzon meg a kromoszóma a legjobb populáció segítségével
            else:
                child_chromosome1 = random.choices(population)[0][1]
                child_chromosome2 = random.choices(population)[0][1]

            # Mutáció
            if random.random() < MUTATION_RATE:
                point1 = random.randint(0, num_of_nodes - 1)
                point2 = random.randint(0, num_of_nodes - 1)
                child_chromosome1[point1], child_chromosome1[point2] = (
                    child_chromosome1[point2],
                    child_chromosome1[point1],
                )

                point1 = random.randint(0, num_of_nodes - 1)
                point2 = random.randint(0, num_of_nodes - 1)
                child_chromosome2[point1], child_chromosome2[point2] = (
                    child_chromosome2[point2],
                    child_chromosome2[point1],
                )

            new_population.append([calcDistance(child_chromosome1), child_chromosome1])
            new_population.append([calcDistance(child_chromosome2), child_chromosome2])

        population = new_population

        gen_number += 1

        if gen_number % 10 == 0:
            print(f"Generation: {gen_number}, Cost: {sorted(population)[0][0]}")

        if sorted(population)[0][0] < TARGET:
            break

    bestPopulation = sorted(population)[0]

    return bestPopulation, gen_number


# A térkép kirajzolása a legoptimálisabban bejárt útvonallal
def drawMap(node, population):
    for n in node:
        plt.plot(n[1], n[2], "ro")
        plt.annotate(n[0], (n[1], n[2]))

    for i in range(len(population[1])):
        try:
            first = population[1][i]
            second = population[1][i + 1]

            plt.plot([first[1], second[1]], [first[2], second[2]], "green")
        except:
            continue

    # Első és utolsó pont összekötése
    first = population[1][0]
    second = population[1][-1]
    plt.plot([first[1], second[1]], [first[2], second[2]], "green")

    plt.show()


def main():
    # Kezdeti értékek meghatározása
    POPULATION_SIZE = 2000
    TOURNAMENT_SELECTION_SIZE = 4
    MUTATION_RATE = 0.1
    CROSSOVER_RATE = 0.9
    TARGET = 450.0

    # Az adatok betöltése
    nodes = loadData()
    # A kezdeti populáció meghatározása a legjobb kezdeti fitneszértékkel együtt
    firstPopulation, firstFittest = selectPopulation(nodes, POPULATION_SIZE)
    # A genetikus algoritmus lefutása, amely egy legjobb megoldást és a legjobb megoldás generációját adja vissza
    bestPopulation, genNumber = geneticAlgorithm(
        firstPopulation,
        len(nodes),
        TOURNAMENT_SELECTION_SIZE,
        MUTATION_RATE,
        CROSSOVER_RATE,
        TARGET,
        100
    )

    # Eredmények kiírása
    print("\n----------------------------------------------------------------")
    print("Generation: " + str(genNumber))
    print("Fittest chromosome distance before training: " + str(firstFittest[0]))
    print("Fittest chromosome distance after training: " + str(bestPopulation[0]))
    print("Target distance: " + str(TARGET))
    print("----------------------------------------------------------------\n")

    # Vizualizálás
    drawMap(nodes, bestPopulation)


main()

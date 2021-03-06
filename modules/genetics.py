from Data import Game, Solution, randomWeight
import random
import os.path

def getGuess(solution, data):
    total = 0
    for prop in data.__dict__:
        if prop != "score":
            total += solution.__dict__[prop + "Weight"] * data.__dict__[prop]
    return total

def getFitness(solution, data):
    return 1 / abs(getGuess(solution, data) - data.score)

def mate(sol1, sol2, data):
    random.seed()

    returnSol = Solution()

    for prop in returnSol.__dict__:
        returnSol.__dict__[prop] = sol1.__dict__[prop] if (random.random() % 2 == 0) else sol2.__dict__[prop]
    return returnSol

def mutate(sol, prob = None):
    if prob == None:
        prob = 0.9

    if randomWeight() <= prob / 4:
        for prop in sol.__dict__:
            sol.__dict__[prop] = randomWeight()

    for prop in sol.__dict__:
        if randomWeight() <= prob:
            sol.__dict__[prop] = randomWeight()

    return sol

def rouletteSelect(sols, data):
    weight_sum = 0
    for sol in sols :
        weight_sum += getFitness(sol, data)

    value = randomWeight() * weight_sum

    for sol in sols:
        value -= getFitness(sol, data)
        if value <= 0:
            return sol
    return sols[-1]

def getNewGen(parents, data, doMutate = None):
    if doMutate == None:
        doMutate = True

    children = []
    for i in range(len(parents)):
        parent1 = rouletteSelect(parents, data)
        parent2 = rouletteSelect(parents, data)
        
        child = mate(parent1, parent2, data)

        if doMutate:
            child = mutate(child)

        children.append(child)

    return children

def getSolution(gameList):
    # Create initial random solutions.
    solutions = []

    if os.path.isfile("weight.txt"):
        solutions = read()
    else:
        for i in range(10):
            solutions.append(Solution())

    for i in range(1):
        for j, game in enumerate(gameList):
            solutions = getNewGen(solutions, game)
            print("Round - %s : Game - %s\n" % (i, j))
            write(solutions)

    # Run the algorithm without mutation, so the solutions converge.
    for i in range(2):
        for game in gameList:
            print("Round - %s : Game - %s : No Mutate\n" % (i, j))
            solutions = getNewGen(solutions, game, False)

    # return random of the final solutions.
    random.seed();
    index = random.randint(0, len(solutions)-1)
    return solutions[index]

def write(solutions):
    file = open('weight.txt', 'w+')
    
    for sol in solutions:
        for i in sol.__dict__:
            file.write("{0}:{1}\n".format(i, sol.__dict__[i]))
        file.write('-------------------\n')
                     
def read():
    file = open('weight.txt', 'r+')

    solutions = []
    solution = Solution()

    for line in file:
        if line[0] == '-':
            solutions.append(solution)
            solution = Solution()
            continue
        
        vals = line.split(':')
        solution.__dict__[vals[0]] = float(vals[1])

    return solutions


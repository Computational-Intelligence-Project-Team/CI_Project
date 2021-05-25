from random import random, randint
import numpy as np

from LocalOptimizationFunctions import ExpandClique

# Boolean Particle Swarm Optimization
class BPSO: 

    def __init__(self, numOfParticles, dimensions, fitnessFunc, maxIter, C1 = 0.2, C2 = 0.5, Omega=0.5, particleLocalOptimizationFunc = None, printParticles = False, printGbest = False):
        self.C1 = C1  # Probablity of c1 (cognitive boolean weightage) being 1
        self.C2 = C2  # Probablity of c2 (social boolean weightage) being 1
        # Probablity of omega (inertia boolean weightage)  being 1
        self.Omega = Omega
        self.particlesPosition = self.initializeRandomly(
            numOfParticles, dimensions)
        self.particlesVelocity = self.initializeRandomly(
            numOfParticles, dimensions)
        self.gBest = np.zeros(dimensions, dtype=int)
        self.gBestFitness = 0
        self.pBest = np.zeros((numOfParticles, dimensions,), dtype=int)
        self.pBestFitness = np.zeros(numOfParticles, dtype=int)

        self.numOfParticles = numOfParticles
        self.dimensions = dimensions
        self.fitnessFunc = fitnessFunc
        self.maxIter = maxIter
        self.printParticles = printParticles
        self.printGbest = printGbest

        self.ParticleLocalOptimizationFunc = particleLocalOptimizationFunc

    def initializeRandomly(self, numOfParticles, dimensions):
        return (np.random.randint(2, size=(numOfParticles, dimensions)))
    
    def updateParticle(self, p):
        for d in range(self.dimensions):
            if random() < self.C1:
                c1 = 1
            else:
                c1 = 0
            if random() < self.C2:
                c2 = 1
            else:
                c2 = 0
            if random() < self.Omega:
                omega = 1
            else:
                omega = 0

            x = self.particlesPosition[p][d]
            v = self.particlesVelocity[p][d]
            self.particlesVelocity[p][d] = omega & v | c1 & (
                self.pBest[p][d] ^ x) | c2 & (self.gBest[d] ^ x)
            self.particlesPosition[p][d] = x ^ self.particlesVelocity[p][d]
        
        if self.ParticleLocalOptimizationFunc is not None:
            # print("before",self.particlesPosition[p])
            self.particlesPosition[p] = self.ParticleLocalOptimizationFunc(self.particlesPosition[p])
            # print("after",self.particlesPosition[p])

    def execute(self):
        for i in range(self.maxIter):
            for p in range(self.numOfParticles):
                fitness = self.fitnessFunc(self.particlesPosition[p])
                # Update Personal Best
                if fitness > self.pBestFitness[p]:
                    self.pBestFitness[p] = fitness
                    self.pBest[p] = self.particlesPosition[p]
                # Update Global Best
                if fitness > self.gBestFitness:
                    self.gBestFitness = fitness
                    self.gBest = self.particlesPosition[p]

                self.updateParticle(p)

            if self.printParticles:
                print("Particles Position:")
                print(self.particlesPosition)
                print()
            if self.printGbest:
                print("Global Best Fitness: ", self.gBestFitness)
                print("Global Best: ", self.gBest)
                print()
    
    def benchmark(self):
        avgFitness = []
        bestFitness = []

        for i in range(self.maxIter):
            total = 0
            for p in range(self.numOfParticles):
                fitness = self.fitnessFunc(self.particlesPosition[p])
                # Update Personal Best
                if fitness > self.pBestFitness[p]:
                    self.pBestFitness[p] = fitness
                    self.pBest[p] = self.particlesPosition[p]
                # Update Global Best
                if fitness > self.gBestFitness:
                    self.gBestFitness = fitness
                    self.gBest = self.particlesPosition[p]
                total += fitness

                self.updateParticle(p)

            avgFitness.append(total/self.numOfParticles)
            bestFitness.append(self.gBestFitness)


            if self.printParticles:
                print("Particles Position:")
                print(self.particlesPosition)
                print()
            if self.printGbest:
                print("Global Best Fitness: ", self.gBestFitness)
                print("Global Best: ", self.gBest)
                print()
            
        maxCliqueNodes = []
        for i in range(self.dimensions):
            if self.gBest[i] == 1:
                maxCliqueNodes.append(i+1)
        
        return (avgFitness,bestFitness,maxCliqueNodes,)

    def gBestDimensionPositions(self):
        nodes = []
        for i in range(self.dimensions):
            if self.gBest[i] == 1:
                nodes.append(i+1)
        return nodes

# graph = {
#     1: [2, 3, 4],
#     2: [3, 1],
#     3: [2, 1],
#     4: [3, 1]
# }
  

def maxCliqueFitness(array,graph):
    
    nodes = []
    for i in range(len(array)):
        if array[i] == 1:
            nodes.append(i)

    # print("nodes: ",nodes)
    # for n in nodes:
    #     print(graph[n+1])

    for n1 in nodes:
        for n2 in nodes:
            if n1 != n2:
                if (n2+1) not in graph[n1+1]: # If other selected nodes are not in the neigbourhood of n1
                    return 0
    return len(nodes)

def maxCliqueClosenessFitness(array,graph):
    
    nodes = []
    for i in range(len(array)):
        if array[i] == 1:
            nodes.append(i)

    # print("nodes: ",nodes)
    # for n in nodes:
    #     print(graph[n+1])
    
        
    return len(nodes)

    # for n in nodes:
    #     if all(x+1 in graph[n+1]  for x in nodes if x != n):
    #         T += 1
    #     else:
    #         return 0

    # return T

# print ("maxCliqueFitness",maxCliqueFitness(np.array([1,1,1,0,0])))

# bpso = BPSO(numOfParticles=30, dimensions=5,
#             fitnessFunc=maxCliqueFitness, maxIter=100)
# bpso.execute()

# print(bpso.maxCliqueNodes())

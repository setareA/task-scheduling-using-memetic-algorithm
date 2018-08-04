#!/usr/bin/python

import DNA
import random
import copy
import database


class Population:

    def __init__(self, size_of_pop, rate, size_of_DNA, connection, programs):

        self.population = []  # list to hold current population
        #self.matingPool # ArrayList which we will use for our "mating pool"
        self.generations = 0  # Number of generations
        self.finished = False
        self.mutationRate = rate
        #this.perfectScore = 1;
        #this.best = "";
        self.size_of_pop = size_of_pop
        self.size_of_dna = size_of_DNA
        self.prog = copy.deepcopy(programs)
        self.file = connection

        for i in range(self.size_of_pop):
            new_dna = DNA.DNA(size_of_DNA,connection, programs, 1)
            self.population.append(new_dna)

        # this.matingPool = [];
        # this.calcFitness();
    def print_population(self):
        counter = 1
        for i in range(self.size_of_pop):
            print(counter)
            #self.population[counter-1].print_DNA()
            print(self.population[counter - 1].get_final_fitness())
            counter += 1

    def get_generations(self):
        return self.generations

    def reproduction(self):
        self.normalize_fitness()
        for i in range(self.size_of_pop):
            parent_a = self.select_parent()
            parent_b = self.select_parent()

            index = self.find_worst_dna_index()
            self.population[index] = copy.deepcopy(self.cross_over_and_mutate(parent_a,parent_b))
        self.generations += 1

    def select_parent(self):
        selected_dna_index = 0
        r = random.uniform(0, 1)
        while r > 0 and selected_dna_index < self.size_of_pop:
            r = r - self.population[selected_dna_index].get_n_fitness()
            selected_dna_index += 1
        selected_dna_index -= 1
        return self.population[selected_dna_index]

    def normalize_fitness(self):
        sum_all = 0;
        for i in range(self.size_of_pop):
            sum_all += self.population[i].get_final_fitness()

        for i in range(self.size_of_pop):
            self.population[i].set_n_fitness(self.population[i].get_final_fitness()/sum_all)

    def cross_over_and_mutate(self, a, b):
        new_dna = DNA.DNA(self.size_of_dna, self.file, self.prog,2)
        random_index = random.randint(1,self.size_of_dna-1)
        for i in range(0,self.size_of_dna):
            if i < random_index:
                new_dna.append_genes(a.return_genes(i))
            else:
                new_dna.append_genes(b.return_genes(i))
        self.mutate_dna(new_dna)
        new_dna.calc_fitness()

        return new_dna

    def mutate_dna(self,new_dna):
        for i in range(0, self.size_of_dna):
            if random.uniform(0, 1) < self.mutationRate:
                new_dna.change_gene(i,database.select_random_node())

    def find_worst_dna_index(self):
        minimum = 1.1
        min_index = 0
        for i in range(self.size_of_pop):
            if minimum > self.population[i].get_final_fitness():
                minimum = self.population[i].get_final_fitness()
                min_index = i
        return min_index

    def get_best_dna(self):
        maximum = 0
        max_index = 0
        for i in range(self.size_of_pop):
            if maximum < self.population[i].get_final_fitness():
                maximum = self.population[i].get_final_fitness()
                max_index = i
        return self.population[max_index]


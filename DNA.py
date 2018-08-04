#!/usr/bin/python

import database
import sqlite3
import random
import copy
import math


class DNA:

    def __init__(self, num, filename, programs, mode):

        self.genes = []
        self.n_fitness = 0
        self.num = num
        self.file = filename
        self.program_list = copy.deepcopy(programs)

        if mode == 1:
            for i in range(self.num):
                self.genes.append(database.select_random_node())   # select one of the nodes

            self.calc_fitness()

    def get_final_fitness(self):
        return self.final_fitness

    def get_fitness(self):
        return self.fitness

    def append_genes(self,node):
        self.genes.append(node)

    def change_gene(self, index ,new_node):
        self.genes[index] = new_node

    def return_genes(self, index):
        return self.genes[index]

    def get_genes(self):
        return self.genes

    def set_n_fitness(self, n_fit):
        self.n_fitness = n_fit

    def get_n_fitness(self):
        return self.n_fitness

    def get_empty_genes(self):
        l = []
        for i in range(self.num):
            if self.program_list[i].get_node() == False:
                l.append(i)
        return l

    def print_DNA(self):
        print("DNA")
        cnt = 0
        for i in range(self.num):
            print(self.genes[cnt])
            cnt += 1

    def calc_fitness(self):

        self.fitness = 0
        fit = 0
        ccc = sqlite3.connect(self.file)
        for i in range(self.num):
            prog = self.program_list[i]
            for row in ccc.execute("SELECT * FROM NODES WHERE ID = " + str(self.genes[i])):
                #print(row)
                if row[2] >= prog.get_ram() and row[3] >= prog.get_cpu() and row[4] == prog.get_cpu_type():
                    #print("prog.get_ram() ,cpu ,prog.get_cpu_type()")
                    # print(prog.get_ram())
                    # print(prog.get_cpu())
                    # print(prog.get_cpu_type())
                    #print("okay")
                    prog.set_node()
                    self.fitness += 1
                    fit += 1
                    ccc.execute("UPDATE NODES SET RAM = "+str(row[2]-prog.get_ram())+", CPU = "+str(row[3]-prog.get_cpu())+" WHERE ID = "+str(self.genes[i]))
                    # for r in ccc.execute("SELECT * FROM NODES WHERE ID = " + str(self.genes[i])):
                    #     print(r)
        #print(fit)
        self.local_hillclimbing(ccc)
        ccc.close()

        self.final_fitness = pow((self.fitness/self.num), 4)
        #return pow((self.fitness/self.num), 4)

    def local_hillclimbing(self, conn):

        random_num = random.randint(0, math.floor(self.num))
        #print("hereeeeeeeeeee")

        for i in range(random_num, self.num):
            prog = self.program_list[i]
            if prog.get_node() == False:
                count = 0
                for row in conn.execute("SELECT * FROM NODES WHERE RAM > " + str(prog.get_ram()) + " AND cpu > " + str(prog.get_cpu()) + " AND CPU_TYPE = " + str(prog.get_cpu_type())):
                    if count == 1:
                        break
                    else:
                        self.genes[i] = row[0]
                        self.program_list[i].set_node()
                        self.fitness += 1
                        conn.execute("UPDATE NODES SET RAM = " + str(row[2] - prog.get_ram()) + ", CPU = " + str(row[3] - prog.get_cpu()) + " WHERE ID = " + str(row[0]))
                        count = 1
                if count == 0:
                    break



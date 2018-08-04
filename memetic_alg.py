#!/usr/bin/python

import sys
import database
import sqlite3
import program
import population
import DNA
import random


def main():

    filename = input()
    connection = database.ComputingCenters(filename)
    connection.create_tables()
    connection.insert_db()

    num_of_programs = random.randint(120, 170)
    print("num of programs :")
    print(num_of_programs)
    programs = program.create_list(num_of_programs)

    pop_max = 70
    mutation_rate = 0.01
    new_population = population.Population(pop_max, mutation_rate,num_of_programs  ,filename,programs)
    #new_population.print_population()

    target_fitness = 1
    cnt = 1
    while not new_population.get_best_dna().get_final_fitness() >= target_fitness:
        new_population.reproduction()
        print("number of generations : ")
        num_of_generations = new_population.get_generations()
        print(num_of_generations)

        if num_of_generations == (50 * cnt):
            target_fitness -= 0.1
            cnt += 1

    print("target_fitness :")
    print(target_fitness)
    final_answer_list = new_population.get_best_dna().get_genes()
    empty_genes = new_population.get_best_dna().get_empty_genes()
    print_final_answer(final_answer_list, empty_genes, filename, programs)


def print_final_answer(final_answer_list, empty_genes, filename, programs):

    c = sqlite3.connect(filename)
    cnt = 0
    for node_id in final_answer_list:
        for row in c.execute("SELECT * FROM NODES WHERE ID = " + str(node_id)):
            ram = programs[cnt].get_ram()
            cpu = programs[cnt].get_cpu()
            cpu_type = programs[cnt].get_cpu_type()
            if cnt in empty_genes:
                report = "Processing program -> ram : " + str(ram) + " cpu : " + str(cpu) + " ,cpu_type : " + str(cpu_type) + " -> NOT ENOUGH RESOURCE "
            else:
                report = """Processing program -> ram : """ + str(ram) + """ ,cpu : """ + str(cpu) + " ,cpu_type : " + str(cpu_type) + """\nCOMPUTING_CENTER ->  id : """ \
                         + str(row[1]) + """\nNODE ->  id : """ \
                         + str(node_id) + " ,available ram : """ + str(row[2] - ram) + """ ,available cpu : """ + str(row[3]- cpu) + " ,cpu_type : " + str(cpu_type)

            cnt += 1
            with open('memetic_algorithm.txt', 'a') as out:
                out.write(report + '\n\n' + "#################" + '\n\n')
            c.execute('''UPDATE NODES SET ram = ram - ?, cpu = cpu - ? WHERE id = ?''', (ram, cpu, node_id))
            c.execute('''UPDATE COMPUTING_CENTERS SET ram = ram - ?, cpu = cpu - ? WHERE id = ?''', (ram, cpu, row[1]))

    c.commit()
    c.close()

if __name__ == "__main__":
    main()




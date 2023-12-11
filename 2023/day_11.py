import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools

def day_():
    year = int(os.getcwd().split('\\')[-1][-4:]) 
    day = int(__file__.split('\\')[-1].split('_')[1].split('.')[0])
    puzzle = Puzzle(year=year, day=day) 
    submit_a = "a" in sys.argv
    submit_b = "b" in sys.argv
    example = "e" in sys.argv

    if (submit_a or submit_b) and example:
        print("Cannot submit examples")
        return

    raw_data = puzzle.input_data
    if example:
        print("Using example")
        #use 'aocd year day --example' to get the example data
        with open('example.txt', 'r') as f:
            raw_data = f.read()

            
    start_time = time.perf_counter()
    data = format_data(raw_data)

    time1 = time.perf_counter()

    ans1 = star1(data)
    time2 = time.perf_counter()

    ans2 = star2(data)
    time3 = time.perf_counter()

    load_time = time1 - start_time
    star1_time = time2 - time1
    star2_time = time3 - time2

    if submit_a:
        print("Submitting star 1")
        puzzle.answer_a = ans1
    if submit_b:
        print("Submitting star 2")
        puzzle.answer_b = ans2
    if 1:
        print(f'Load time: {load_time}')
        print(f'Star 1 time: {star1_time}')
        print(f'Star 2 time: {star2_time}')
        print(f'Star 1 answer: {ans1}')
        print(f'Star 2 answer: {ans2}')


def format_data(raw):
    universe = []
    for line in raw.splitlines():
        universe.append([c for c in line])
    return universe
    

def parse_universe(universe):
    rows = len(universe)
    cols = len(universe[0])
    emptyRows = [False] * rows
    for i in range(rows):
        if all([c == '.' for c in universe[i]]):
            emptyRows[i] = True
    emptyCols = [False] * cols
    for i in range(cols):
        if all([row[i] == '.' for row in universe]):
            emptyCols[i] = True

    galaxies = []
    for y in range(rows):
        for x in range(cols):
            if universe[y][x] == '#':
                galaxies.append((x,y))
    return galaxies, emptyRows, emptyCols

def star1(universe):
    
    galaxies, emptyRows, emptyCols = parse_universe(universe)
    pairs = list(itertools.combinations(galaxies, 2))

    ret = 0
    for (g1,g2) in pairs:
        dx = abs(g2[0] - g1[0])
        dy = abs(g2[1] - g1[1])
        dx += len([i for i in range(min(g1[0], g2[0]), max(g1[0], g2[0])) if emptyCols[i] == True])
        dy += len([i for i in range(min(g1[1], g2[1]), max(g1[1], g2[1])) if emptyRows[i] == True])
        ret += dx + dy
    return ret

def star2(universe):
    galaxies, emptyRows, emptyCols = parse_universe(universe)
    pairs = list(itertools.combinations(galaxies, 2))

    ret = 0
    for (g1,g2) in pairs:
        dx = abs(g2[0] - g1[0])
        dy = abs(g2[1] - g1[1])
        dx += (1000000-1)*len([i for i in range(min(g1[0], g2[0]), max(g1[0], g2[0])) if emptyCols[i] == True])
        dy += (1000000-1)*len([i for i in range(min(g1[1], g2[1]), max(g1[1], g2[1])) if emptyRows[i] == True])
        ret += dx + dy
    return ret

def main():
    import cProfile
    import pstats
    with cProfile.Profile() as pr:
        day_()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    day = int(__file__.split('\\')[-1].split('_')[1].split('.')[0]) 
    stats.dump_stats(filename = f'profiling\\profiling{day}.prof')

# run with `py day_n.py -- a b` to submit both stars for day n
if __name__ == '__main__':
    main()
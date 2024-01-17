#!/usr/bin/env python3

import benchmark
from pathlib import Path
import re
import datetime
import time

import domainGenerator

def run(approach, domainFileName, del_all, horizon , timeout):
    (domainPath, approach, reversibleActionName, horizon, timeoutLimit, wallClock, setSize) = benchmark.benchmark(approach, domainFileName, del_all, horizon , timeout)
    print(f"{approach}: {wallClock} seconds")

num_plans_success = 2
print(f"num_plans_success: {num_plans_success}")
length_plans_success = 2
print(f"length_plans_success: {length_plans_success}")
num_plans_dead_end = 31
print(f"num_plans_dead_end: {num_plans_dead_end}")
length_plans_dead_end = 5
print(f"length_plans_dead_end: {length_plans_dead_end}")
domainString = domainGenerator.general_domain_generator(num_plans_success, length_plans_success, num_plans_dead_end, length_plans_dead_end)

# if file already exists, skip
domainFileName = "debug.pddl"
# if not Path("debug.pddl").is_file():
domainFile = open(domainFileName, "w")
domainFile.write(domainString)
domainFile.close()
print(f"created domain file: {domainFileName}")


# prepare execution
horizon = max(length_plans_success, length_plans_dead_end)+1
timeout = 60
del_all = "del-all"

print(f"horizon: {horizon}")
print(f"timeout: {timeout} seconds")

run("dfs", domainFileName, del_all, horizon , timeout)
run("bfs", domainFileName, del_all, horizon , timeout)
run("asp", domainFileName, del_all, horizon , timeout)
print()

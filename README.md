<p align="center">
    <img src="logo.svg" alt="">
    <br>
    <img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="license">
    <br>
    <b>Towards the Evaluation of Action Reversibility in STRIPS using Domain Generators</b>
</p>

<p align="center">
    <a href="#summary">Summary</a>
    •
    <a href="#setup">Setup</a>
    •
    <a href="#usage">Usage</a>
    •
    <a href="#examples">Examples</a>
    •
    <a href="#experiments">Experiments</a>
</p>

## Summary

In planning, the reversibility of actions deals with the question whether the effects of an action can be undone using a reverse plan. This repository provides a prototypical implementation (see [`reversible.py`](reversible.py)) of the action reversibility algorithm proposed by 
M. Morak, L. Chrpa, W. Faber, and D. Fiser in their paper "On the reversibility of actions in planning" (KR 2020) using a depth-first search (`dfs`) and breadth-first search (`bfs`) strategy. This implementation is evaluated following the PDDL domain generator approach of L. Chrpa, W. Faber, D. Fiser, and M. Morak, which they proposed and used in their paper "Determining action reversibility in STRIPS using answer set programming" (ICLP 2020) to evaluate the performance of their answer set programming (`asp`) and (`qasp`) based implementations.

We extended their domain generator template (`singlePath`) to a `multiplePaths` and `multiplePathsDeadEnds` template but also added completely new domain generators: one based on a general approach for domain generation (`generalized`) and two others (`barabasiAlbertLongestShortestPath`, `barabasiAlbertLongestDegree`) based on the Barabási–Albert model (see [`domainGenerator.py`](domainGenerator.py)).

The produced benchmarks (see [`benchmark.py`](benchmark.py)) reveal that even slightly changed parameters in the `singlePath`, `multiplePaths` and `multiplePathsDeadEnds` domain generator templates suffice to introduce a radical bias that either favors the `bfs`, `dfs`, or `asp` approach. Hence, care must be taken when evaluating algorithms for action reversibility using PDDL domains obtained from domain generators. Using the `generalized`, `barabasiAlbertLongestShortestPath`, and `barabasiAlbertLongestDegree` domain generators, more sophisticated domains with diverse characteristics can be created that might serve as a basis for a future action reversibility benchmark.

## Setup

We provide a [`Dockerfile`](Dockerfile) and [`docker-compose.yml`](docker-compose.yml) file that define the required software dependencies and setup instructions. Build the underlying docker image via `docker-compose build` and start a container via `docker-compose run reversible`.

## Usage

We use [google/python-fire](https://github.com/google/python-fire) to automatically generate command line interfaces (CLIs) for the following python scripts:

- [`reversible.py`](./reversible.py) to search for reverse plans of an action in a PDDL domain
- [`domainGenerator.py`](./domainGenerator.py) to generate PDDL domains
- [`benchmark.py`](./benchmark.py) to obtain the performance of a reverse plan search
- [`experiments.py`](./experiments.py) to run the full experiments pipeline

Run `python3 ./<script> --help` where `<script>` is one of the provided python scripts to obtain information on required command line arguments.

## Experiments

To reproduce the results from our papers, execute the [`experiments.py`](experiments.py) script from within the docker container via `python3 ./experiments.py`. The obtained performance results are stored in the `experiments` folder. A single csv file is generated for each approach (`dfs`, `bfs`, `asp`, `qasp`) and domain generator (`singlePath`, `multiplePaths`, `multiplePathsDeadEnds`, `generalized`, `barabasiAlbertLongestShortestPath`, `barabasiAlbertDegree`) combination.

## Further Examples

Generate a single PDDL domain using the `singlePath` template
```
root@f0606f1aec12:/reversibility# python3 ./domainGenerator.py domains 5 5 1 singlePath
Generating singlePath domain for input i = 5 ... done ... and saved as file "domains/singlePath_d005.pddl"
```

Find a reverse plan for action `del-all` in the PDDL domain created above using a `dfs` strategy:
```
root@f0606f1aec12:/reversibility# python3 ./reversible.py domains/singlePath_d005.pddl del-all dfs
Computing a reverse plan for action "del-all" ... I have found the following solutions:
F0:
Fplus: f1, f4, f0, f5, f3, f2
Fminus:
pi: add-f0 -> add-f1 -> add-f2 -> add-f3 -> add-f4 -> add-f5
Path length: 6

I wont look for further solutions, because "findSingleSolution" is enabled
```

Obtain performance benchmark information for the above example using the `asp` approach:
```
root@f0606f1aec12:/reversibility# python3 ./benchmark.py asp domains/singlePath_d005.pddl del-all 6 10
clingo version 5.4.0
Reading from /tools/sequential-horizon.uurev.lp ...
Solving...
Answer: 1
chosen("del-all") plan("add-f0",1) plan("add-f1",2) plan("add-f2",3) plan("add-f3",4) plan("add-f4",5) plan("add-f5",6)
SATISFIABLE

Models       : 1
Calls        : 1
Time         : 0.007s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.004s
```

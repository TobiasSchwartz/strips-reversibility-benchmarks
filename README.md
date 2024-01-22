<p align="center">
    <img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="license">
    <br>
    <b>Domain Generators for the Evaluation of Action Reversibility in STRIPS</b>
</p>

<p align="center">
    <a href="#summary">Summary</a>
    •
    <a href="#setup--usage">Setup & Usage</a>
    •
    <a href="#experiments">Experiments</a>
    •
    <a href="#references">References</a>
    •
    <a href="#license">License</a>
</p>

# Summary

In planning, the reversibility of actions deals with the question whether the effects of an action can be undone using a reverse plan. This repository provides a prototypical implementation (see [`reversible.py`](reversible.py)) of the action reversibility algorithm proposed in [[1]](#references) 
using a depth-first search (`dfs`) and breadth-first search (`bfs`) strategy. This implementation is evaluated following the PDDL domain generator approach proposed and employed in [[2]](#references), which the authors used to assess the performance of their answer set programming (ASP) based implementation. 

We extended their domain generator template (`singlePath`) to a `multiplePaths` and `multiplePathsDeadEnds` template but also added completely new domain generators: one based on a general approach for domain generation (`generalized`) and two others (`barabasiAlbertLongestShortestPath`, `barabasiAlbertLongestDegree`) based on the Barabási–Albert model (see [`domainGenerator.py`](domainGenerator.py)).

We compare our `dfs` and `bfs` strategies with different ASP variants (`asp_simple`, `asp_general`, `qasp`) [[2-4]](#references).

# Setup & Usage

We provide a [`Dockerfile`](Dockerfile) and [`docker-compose.yml`](docker-compose.yml) file that define the required software dependencies and setup instructions. Build the underlying docker image via `docker-compose build` and start a container via `docker-compose run reversible`.

We use [google/python-fire](https://github.com/google/python-fire) to automatically generate command line interfaces (CLIs) for the following python scripts:

- [`experiments.py`](./experiments.py) to run the full experiments pipeline
- [`domainGenerator.py`](./domainGenerator.py) to generate PDDL domains
- [`reversible.py`](./reversible.py) to search for reverse plans of an action in a PDDL domain
- [`benchmark.py`](./benchmark.py) to obtain the performance of a reverse plan search

Run `python3 ./<script> --help` where `<script>` is one of the provided python scripts to obtain information on required command line arguments.

# Experiments

To reproduce the results from our papers, execute the [`experiments.py`](experiments.py) script from within the docker container via `python3 ./experiments.py`. The obtained performance results are stored in the `experiments` folder. A single csv file is generated for each approach (`dfs`, `bfs`, `asp_simple`, `asp_general`, `qasp`) and domain generator (`singlePath`, `multiplePaths`, `multiplePathsDeadEnds`, `generalized`, `barabasiAlbertLongestShortestPath`, `barabasiAlbertDegree`) combination.

The [benchmarks.zip](./benchmarks.zip) file contains the benchmark results used in our AMAI submission.

## Further Examples

Generate a single PDDL domain using the `singlePath` template
```
root@a3e10e5aa9e6:/reversibility# python3 ./domainGenerator.py generateStandardDomains ./domains 5 5 1 singlePath
Generating singlePath domain for input i = 5 ... done ... and saved as file "./domains/0001-singlePath-5.pddl"
```

Find a reverse plan for action `del-all` in the PDDL domain created above using a `dfs` strategy:
```
root@a3e10e5aa9e6:/reversibility# python3 ./reversible.py ./domains/0001-singlePath-5.pddl del-all dfs
Computing a reverse plan for action "del-all" ... I have found the following solutions:
F0:
Fplus: f2, f4, f5, f3, f1, f0
Fminus:
pi: add-f0 -> add-f1 -> add-f2 -> add-f3 -> add-f4 -> add-f5
Path length: 6

I wont look for further solutions, because "findSingleSolution" is enabled
```

Obtain performance benchmark information for the above example using the `asp_simple` approach:
```
root@a3e10e5aa9e6:/reversibility# python3 ./benchmark.py asp_simple ./domains/0001-singlePath-5.pddl del-all 6 10
clingo version 5.4.0
Reading from /tools/sequential-horizon.simple.asp ...
Solving...
Answer: 1
chosen("del-all") plan("add-f0",1) plan("add-f1",2) plan("add-f2",3) plan("add-f3",4) plan("add-f4",5) plan("add-f5",6)
SATISFIABLE

Models       : 1
Calls        : 1
Time         : 0.005s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.003s
Command exited with non-zero status 30
        Command being timed: "/tools/clingo /tools/sequential-horizon.simple.asp -c horizon=6 ./domains/0001-singlePath-5.pddl.lp" 
        User time (seconds): 0.00
        System time (seconds): 0.00
        Percent of CPU this job got: 37%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.00
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 5452
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 237
        Voluntary context switches: 40
        Involuntary context switches: 0
        Swaps: 0
        File system inputs: 0
        File system outputs: 8
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 30
```

# References

[1] M. Morak, L. Chrpa, W. Faber, and D. Fiser. "On the reversibility of actions in planning" (KR 2020)

[2] L. Chrpa, W. Faber, D. Fiser, and M. Morak. "Determining Action Reversibility in STRIPS using Answer Set Programming" (ICLP 2020)

[3] W. Faber, M. Morak, and L. Chrpa. "Determining Action Reversibility in STRIPS Using Answer Set and Epistemic Logic Programming" (TPLP 2022)

[4] W. Faber, M. Morak, and L. Chrpa. "Determining Action Reversibility in STRIPS using Answer Set Programming with Quantifiers" (PADL 2022)

# License

See [LICENSE](./LICENSE)
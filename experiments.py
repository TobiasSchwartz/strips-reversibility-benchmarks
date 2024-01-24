#!/usr/bin/env python3

import benchmark
from pathlib import Path
import datetime
import time
import domainGenerator
import numpy as np


def domainTypeFromDomainFileName(filename):
    if "singlePath" in filename:
        return "singlePath"
    elif "multiplePathsDeadEnds" in filename:
        return "multiplePathsDeadEnds"
    elif "multiplePaths" in filename:
        return "multiplePaths"
    elif "generalized" in filename:
        return "generalized"
    elif "barabasiAlbertLongestShortestPath" in filename:
        m_val = int(filename.split("-")[2])
        return f"barabasiAlbertLongestShortestPath-{(m_val if m_val<= 9 else 'max')}"
    elif "barabasiAlbertDegree" in filename:
        return "barabasiAlbertDegree"


def horizonFromDomainFileName(filename):
    domain_size = int(filename.split("-")[-1].split(".pddl")[0])
    domain_size += 1
    if "singlePath" in filename:
        return (int)(domain_size)
    elif "multiplePathsDeadEnds" in filename:
        return (int)(((domain_size) * (domain_size + 1)) * 0.5)
    elif "multiplePaths" in filename:
        return (int)(((domain_size) * (domain_size + 1)) * 0.5)
    elif "generalized" in filename:
        return int(filename.split("-")[-1].split(".")[0]) + 1
    elif "barabasiAlbertLongestShortestPath" in filename:
        return int(filename.split("-")[-1].split(".")[0]) + 1
    elif "barabasiAlbertDegree" in filename:
        return int(filename.split("-")[-1].split(".")[0]) + 1
    

if __name__ == "__main__":

    # specify the used approach
    approaches = [
        "dfs",
        "bfs",
        "asp_simple",
        # "asp_general"
    ]

    # specify domains of which types are created and evaluated
    domain_types = [
        # "singlePath",
        # "multiplePaths",
        # "multiplePathsDeadEnds",
        # "generalized",
        "barabasiAlbertLongestShortestPath"
    ]

    domains_folder = "domains"

    [f.unlink() for f in Path(domains_folder).glob("*") if f.is_file()]

    ##### Generate singlePath domains
    if "singlePath" in domain_types:
        domainGenerator.generateStandardDomains(domains_folder, 10, 500, 10, "singlePath")

    ##### Generate multiplePaths domains
    if "multiplePaths" in domain_types:
        domainGenerator.generateStandardDomains(domains_folder, 1, 50, 1, "multiplePaths")

    ##### Generate multiplePathsDeadEnds domains
    if "multiplePathsDeadEnds" in domain_types:    
        domainGenerator.generateStandardDomains(domains_folder, 1, 50, 1, "multiplePathsDeadEnds")

    ##### Generate generalized domains
    if "generalized" in domain_types:
        step_range = np.arange(1.0, 101.1, 5.0)

        # Scenario 1
        for factor in step_range:
            domainGenerator.generateGeneralizedDomain(domains_folder, 1,  4,  int(20*factor), 4)

        # # Scenario 2
        for factor in step_range:
            domainGenerator.generateGeneralizedDomain(domains_folder, int(6*factor),  10,  int(4*factor), 10)

        # Scenario 3
        for factor in step_range:
            domainGenerator.generateGeneralizedDomain(domains_folder, 10,  4,  int(2*factor), int(2*factor))

    #### Generate barabasiAlbertLongestShortestPath domains
    if "barabasiAlbertLongestShortestPath" in domain_types:
        for n in range(2000, 6001, 200):
            domainGenerator.generateBarabasiAlbertDomains(domains_folder, n, 1, "barabasiAlbertLongestShortestPath")
        for n in range(2000, 5001, 200):
            domainGenerator.generateBarabasiAlbertDomains(domains_folder, n, 5, "barabasiAlbertLongestShortestPath")
        for n in range(2000, 5001, 200):
            domainGenerator.generateBarabasiAlbertDomains(domains_folder, n, n-1, "barabasiAlbertLongestShortestPath")

    timestamp = time.time()

    #### Generate experiment csv files and write domain_type specific headers
    Path("./experiments/").mkdir(parents=True, exist_ok=True)

    for approach in approaches:
        if "barabasiAlbertLongestShortestPath" in domain_types:
            domain_types.remove("barabasiAlbertLongestShortestPath")
            domain_types.append("barabasiAlbertLongestShortestPath-1")
            domain_types.append("barabasiAlbertLongestShortestPath-5")
            domain_types.append("barabasiAlbertLongestShortestPath-max")
        for domain_type in domain_types:
            with open(f"./experiments/{domain_type}-{approach}-{timestamp}.csv", "a+") as f:
                if domain_type == "singlePath" or domain_type == "multiplePaths" or domain_type == "multiplePathsDeadEnds":
                    f.write("approach,domain_type,horizon,i,path,runtime_seconds,set_size_mb\n")

                elif domain_type == "generalized":
                    f.write("approach,domain_type,horizon,num_plans_success,length_plans_success,length_plans_dead_end,num_plans_dead_end,domain_size,path,runtime_seconds,set_size_mb\n")

                elif "barabasiAlbertLongestShortestPath" in domain_type or domain_type == "barabasiAlbertDegree":
                    f.write("approach,domain_type,horizon,m,n,node_a,node_b,domain_size,path,runtime_seconds,set_size_mb\n")

    #### Run experiments
    timeout = 120
    pathlist = Path(f"./{domains_folder}/").glob(f'*.pddl')

    for path in pathlist:
        path = str(path)

        for approach in approaches:
            domain_type = domainTypeFromDomainFileName(path)
            result_file_path = f"./experiments/{domain_type}-{approach}-{timestamp}.csv"

            # skip domain if run on previous domain already timed out
            # Attention: use only for singlePath, multiplePath, multiplePathsDeadEnds, and generalized as only these will definitely become more difficult
            if domain_type == "singlePath" or domain_type == "multiplePaths" or domain_type == "multiplePathsDeadEnds":
                with open(result_file_path) as f:
                    # find out whether there was timeout
                    if "-1" in f.readlines()[-1].split(",")[-2]:
                        print("Skipped a domain due to previous timeout!")
                        continue

            print(f"***************** Processing {path} using {approach} approach *****************\n")

            # we do not want to give our approaches an edge by aborting early
            # only asp and qasp should know the horizon
            if approach == "asp_simple" or approach == "asp_general" or approach == "qasp":
                horizon = horizonFromDomainFileName(path)
            else:
                horizon = -1

            print(f"Horizon = {horizon}\n")
            (domain_path, approach, reversible_action_name, horizon, timeout_limit, wall_clock, set_size) = benchmark.benchmark(
                approach, path, "del-all", horizon, timeout
            )

            if type(wall_clock) == str:
                strptime = datetime.datetime.strptime(wall_clock, r'%M:%S.%f')
                csv_runtime = (strptime.minute * 60) + strptime.second + \
                    (strptime.microsecond / 1000000)
            else:
                csv_runtime = -1
            csv_set_size = int(set_size) / 1024
            csv_generator_arguments = ",".join(path.split(".pddl")[0].split("-")[2:])

            # append results
            with open(result_file_path, "a+") as f:
                f.write(f"{approach},{domain_type},{horizon},{csv_generator_arguments},{path},{csv_runtime},{csv_set_size}\n")

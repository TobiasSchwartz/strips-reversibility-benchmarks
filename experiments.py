#!/usr/bin/env python3

import benchmark
from pathlib import Path
import re
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
        return "barabasiAlbertLongestShortestPath"
    elif "barabasiAlbertDegree" in filename:
        return "barabasiAlbertDegree"


def horizonFromDomainFileName(filename):
    domain_size = int(re.sub('[^0-9]', '', str(filename)))
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

    # Specifies the used approach
    approaches = [
        "dfs",
        # "bfs",
        # "asp_simple",
        # "asp_general",
        # "qasp",
    ]

    # Specifies domains of which types are created and evaluated
    domain_types = [
        # "singlePath",
        # "multiplePaths",
        # "multiplePathsDeadEnds",
        "generalized",
        # "barabasiAlbertLongestShortestPath",
        # "barabasiAlbertDegree",
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
    # TODO asp_simple and asp_general encodings become UNSATISFIABLE as soon as num_plans_success > 1; probably related to the pre-goal action requiring "and" instead of "or" in the precondition
    if "generalized" in domain_types:
        step_range = np.arange(1.0, 5.3, 0.3)

        # Scenario 1: only one success path, many dead ends, all paths short
        for i in step_range:
            domainGenerator.generateGeneralizedDomain(domains_folder, 1,  4,  int(4*i), 4)

        # Scenario 2: only one success path, few dead ends, all paths long
        for i in step_range:
            domainGenerator.generateGeneralizedDomain(domains_folder, 1,  int(4*i),  int(2*i), int(4*i))

        # Scenario 3: multiple long success paths, no dead ends
        for i in step_range:
            domainGenerator.generateGeneralizedDomain(domains_folder, int(4*i),  int(4*i),  0, 0)

        # Scenario 4: few short success paths, many long dead ends
        for i in step_range:
            domainGenerator.generateGeneralizedDomain(domains_folder, 2,  4,  int(4*i), int(4*i))

        # num_plans_success >> num_plans_dead_end -> bfs faster than dfs
        # multiple long paths leading to the goal -> dfs faster than bfs
        # num_plans_success >> num_plans_dead_end -> dfs ~ bfs

    #### Generate barabasiAlbertLongestShortestPath domains
    if "barabasiAlbertLongestShortestPath" in domain_types:
        domainGenerator.generateBarabasiAlbertDomains(domains_folder, 200, 199, "barabasiAlbertLongestShortestPath")
        domainGenerator.generateBarabasiAlbertDomains(domains_folder, 200, 100, "barabasiAlbertLongestShortestPath")
        domainGenerator.generateBarabasiAlbertDomains(domains_folder, 200, 10, "barabasiAlbertLongestShortestPath")

        # n ~ m -> sometimes bfs, sometimes dfs faster
        # n >> m -> dfs usually faster than bfs
        # n = 2 * m -> dfs has many timeouts; bfs usually faster than dfs

    timestamp = time.time()

    #### Generate experiment csv files and write domain_type specific headers
    Path("./experiments/").mkdir(parents=True, exist_ok=True)

    for approach in approaches:
        for domain_type in domain_types:
            with open(f"./experiments/{domain_type}-{approach}-{timestamp}.csv", "a+") as f:
                if domain_type == "singlePath" or domain_type == "multiplePaths" or domain_type == "multiplePathsDeadEnds":
                    f.write("approach,domain_type,horizon,i,path,runtime_seconds,set_size_mb\n")

                elif domain_type == "generalized":
                    f.write("approach,domain_type,horizon,num_plans_success,length_plans_success,length_plans_dead_end,num_plans_dead_end,max_path_length,path,runtime_seconds,set_size_mb\n")

                elif domain_type == "barabasiAlbertLongestShortestPath" or domain_type == "barabasiAlbertDegree":
                    f.write("approach,domain_type,horizon,n,m,node_a,node_b,path_length,path,runtime_seconds,set_size_mb\n")

    #### Run experiments
    timeout = 60
    pathlist = Path(f"./{domains_folder}/").glob(f'*.pddl')

    for path in pathlist:
        path = str(path)

        for approach in approaches:
            domain_type = domainTypeFromDomainFileName(path)
            result_file_path = f"./experiments/{domain_type}-{approach}-{timestamp}.csv"
            
            # # skip domain if run on previous domain already timed out
            # # Attention: use only for singlePath, multiplePath, multiplePathsDeadEnds, and generalized as only these will definitely become more difficult
            # if domain_type == "singlePath" or domain_type == "multiplePaths" or domain_type == "multiplePathsDeadEnds" or domain_type == "generalized":
            #     with open(result_file_path) as f:
            #         if ",-1," in f.readlines()[-1]:
            #             continue

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
            csv_generator_arguments = path.split(f"{domain_type}-")[1].split(".pddl")[0].replace("-", ",")

            # append results
            with open(result_file_path, "a+") as f:
                f.write(f"{approach},{domain_type},{horizon},{csv_generator_arguments},{path},{csv_runtime},{csv_set_size}\n")

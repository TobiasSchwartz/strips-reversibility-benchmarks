#!/usr/bin/env python3

def domainTypeFromDomainFileName(filename):
    if "singlePath" in filename:
        return "singlePath"
    elif "multiplePathsDeadEnds" in filename:
        return "multiplePathsDeadEnds"
    elif "multiplePaths" in filename:
        return "multiplePaths"
    elif "generalApproach" in filename:
        return "generalApproach"
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
    elif "generalApproach" in filename:
        return int(filename.split("-")[-1].split(".")[0]) + 1
    elif "barabasiAlbertLongestShortestPath" in filename:
        return int(filename.split("-")[-1].split(".")[0]) + 1
    elif "barabasiAlbertDegree" in filename:
        return int(filename.split("-")[-1].split(".")[0]) + 1
    

if __name__ == "__main__":
    import benchmark
    from pathlib import Path
    import re
    import datetime
    import time
    import domainGenerator

    timeout = 60

    approaches = [
        "dfs",
        "bfs",
        "asp-simple",
        # "asp-general",
        # "qasp",
    ]

    domain_types = [
        # "singlePath",
        # "multiplePaths",
        # "multiplePathsDeadEnds",
        "generalApproach",
        # "barabasiAlbertLongestShortestPath",
        # "barabasiAlbertDegree",
    ]

    domains_folder = "domains"

    [f.unlink() for f in Path(domains_folder).glob("*") if f.is_file()]

    ##### Generate singlePath, multiplePaths, multiplePathsDeadEnds, domains
    # domainGenerator.generateStandardDomains(domains_folder, 10, 500, 10, "singlePath")
    # domainGenerator.generateStandardDomains(domains_folder, 1, 50, 1, "multiplePaths")
    # domainGenerator.generateStandardDomains(domains_folder, 1, 50, 1, "multiplePathsDeadEnds")

    # TODO asp-simple and asp-general encodings become UNSATISFIABLE as soon as num_plans_success > 1; probably related to the pre-goal action requiring "and" instead of "or" in the precondition

    ##### Generate generalApproach domains
    # Scenario 1: only one success path, many dead ends, all paths short
    for i in [x / 10.0 for x in range(10, 50)]:
        domainGenerator.generateGeneralApproachDomain(domains_folder, 1,  4,  int(4*i), 4)

    # Scenario 2: only one success path, few dead ends, all paths long
    # for i in [x / 10.0 for x in range(10, 50)]:
    #     domainGenerator.generateGeneralApproachDomain(domains_folder, 1,  int(4*i),  int(2*i), int(4*i))

    # # Scenario 3: multiple long success paths, no dead ends
    # for i in [x / 10.0 for x in range(10, 50)]:
    #     domainGenerator.generateGeneralApproachDomain(domains_folder, int(4*i),  int(4*i),  0, 0)

    # # Scenario 4: few short success paths, many long dead ends
    # for i in [x / 10.0 for x in range(10, 50)]:
    #     domainGenerator.generateGeneralApproachDomain(domains_folder, 2,  4,  int(4*i), int(4*i))

    # num_plans_success >> num_plans_dead_end -> bfs faster than dfs
    # multiple long paths leading to the goal -> dfs faster than bfs
    # num_plans_success >> num_plans_dead_end -> dfs ~ bfs

    ##### Generate barabasiAlbertLongestShortestPath domains
    # n ~ m -> sometimes bfs, sometimes dfs faster
    # domainGenerator.generateBarabasiAlbertDomains(domains_folder, 200, 199, "barabasiAlbertLongestShortestPath")

    # n = 2 * m -> dfs has many timeouts; bfs usually faster than dfs
    # domainGenerator.generateBarabasiAlbertDomains(domains_folder, 200, 100, "barabasiAlbertLongestShortestPath")

    # n >> m -> dfs usually faster than bfs
    # domainGenerator.generateBarabasiAlbertDomains(domains_folder, 200, 10, "barabasiAlbertLongestShortestPath")

    time = time.time()
    Path("./experiments/").mkdir(parents=True, exist_ok=True)
    for approach in approaches:
        for domain_type in domain_types:
            with open(f"./experiments/experiment-{domain_type}-{approach}-{time}.csv", "a+") as f:
                f.write("approach,domain,generatorArgument,path,runtimeInseconds,setSizeInmb\n")

    pathlist = Path(f"./{domains_folder}/").glob(f'*.pddl')

    # Sorts pathlist and therefore csv lines correctly
    def key_func(s):
        return [int(part) if part.isdigit() else part for part in str(s).split('-')[3:8]]

    # Sort the list using the custom key function
    sorted_list = sorted(pathlist, key=key_func)

    for path in sorted_list:
        path = str(path)

        for approach in approaches:

            domain_type = domainTypeFromDomainFileName(path)
            result_file_path = f"./experiments/experiment-{domain_type}-{approach}-{time}.csv"

            # skip domain if it is commented out
            if domain_type not in domain_types:
                continue
            
            # skip domain if run on previous domain already timed out
            # Attention: use only for singlePath, multiplePath, multiplePathsDeadEnds, and generalApproach as only these will definitely become more difficult
            if domain_type == "singlePath" or domain_type == "multiplePaths" or domain_type == "multiplePathsDeadEnds" or domain_type == "generalApproach":
                with open(result_file_path) as f:
                    if ",-1," in f.readlines()[-1]:
                        continue

            print(f"***************** Processing {path} using {approach} approach *****************\n")

            # we do not want to give our approaches an edge by aborting early
            # only asp and qasp should know the horizon
            if approach == "asp-simple" or approach == "asp-general" or approach == "qasp":
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

            if domain_type == "singlePath" or domain_type == "multiplePaths" or domain_type == "multiplePathsDeadEnds":
                csv_i_value = re.sub('[^0-9]', '', path)
            else:
                csv_i_value = "not applicable"

            # append results
            with open(result_file_path, "a+") as f:
                f.write(f"{approach},{domain_type},{csv_i_value},{path},{csv_runtime},{csv_set_size}\n")

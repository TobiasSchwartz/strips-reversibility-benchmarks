#!/usr/bin/env python3

def domainFromDomainFileName(filename):
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
        # "dfs",
        "bfs",
        # "asp",
        # "qasp",
    ]

    domains = [
        # "singlePath",
        "multiplePaths",
        # "multiplePathsDeadEnds",
        # "generalApproach",
        # "barabasiAlbertLongestShortestPath",
        # "barabasiAlbertDegree",
    ]

    domainsFolder = "domains"

    [f.unlink() for f in Path(domainsFolder).glob("*") if f.is_file()]

    # Generate singlePath, multiplePaths, multiplePathsDeadEnds, domains
    # domainGenerator.generateStandardDomains(domainsFolder, 10, 500, 10, "singlePath")
    domainGenerator.generateStandardDomains(domainsFolder, 1, 50, 1, "multiplePaths")
    # domainGenerator.generateStandardDomains(domainsFolder, 1, 50, 1, "multiplePathsDeadEnds")

    # Generate domains based on the general approach
    domainGenerator.generateGeneralApproachDomain(domainsFolder, 2, 2, 30, 5)

    # Generate domains using Barabasi-Albert Longest Shortest Path method
    # n ~ m -> sometimes bfs, sometimes dfs faster
    # domainGenerator.generateBarabasiAlbertDomains(domainsFolder, 200, 199, "barabasiAlbertLongestShortestPath")

    # n = 2 * m -> dfs has many timeouts; bfs usually faster than dfs
    # domainGenerator.generateBarabasiAlbertDomains(domainsFolder, 200, 100, "barabasiAlbertLongestShortestPath")

    # n >> m -> dfs usually faster than bfs
    # domainGenerator.generateBarabasiAlbertDomains(domainsFolder, 200, 10, "barabasiAlbertLongestShortestPath")

    time = time.time()
    Path("./experiments/").mkdir(parents=True, exist_ok=True)
    for approach in approaches:
        for domain in domains:
            with open(f"./experiments/experiment-{domain}-{approach}-{time}.csv", "a+") as f:
                f.write("approach,domain,generatorArgument,path,runtimeInseconds,setSizeInmb\n")

    pathlist = Path(f"./{domainsFolder}/").glob(f'*.pddl')

    for path in pathlist:
        path = str(path)

        for approach in approaches:
            
            print(f"***************** Processing {path} using {approach} approach *****************\n")

            domain = domainFromDomainFileName(path)
            resultFilePath = f"./experiments/experiment-{domain}-{approach}-{time}.csv"

            # skip domain if it is commented out
            if domain not in domains:
                print("Skipped because domain type is commented out!")
                continue
            
            # skip domain if run on previous domain already timed out
            # Attention: use only for singlePath, multiplePath, and multiplePathsDeadEnds, as only these will definitely become more difficult
            if domain == "multiplePaths" or domain == "multiplePaths" or domain == "multiplePaths":
                with open(resultFilePath) as f:
                    if ",-1," in f.readlines()[-1]:
                        print("Skipped because run with previous domain timed out!")
                        continue

            # we do not want to give our approaches an edge by aborting early
            # only asp and qasp should know the horizon
            if approach == "asp" or approach == "qasp":
                horizon = horizonFromDomainFileName(path)
            else:
                horizon = -1

            print(f"Horizon = {horizon}\n")
            (domainPath, approach, reversibleActionName, horizon, timeoutLimit, wallClock, setSize) = benchmark.benchmark(
                approach, path, "del-all", horizon, timeout
            )

            if type(wallClock) == str:
                strptime = datetime.datetime.strptime(wallClock, r'%M:%S.%f')
                csvRuntime = (strptime.minute * 60) + strptime.second + \
                    (strptime.microsecond / 1000000)
            else:
                csvRuntime = -1
            csvSetSize = int(setSize) / 1024
            csvIvalue = re.sub('[^0-9]', '', path)

            # append results
            with open(resultFilePath, "a+") as f:
                f.write(f"{approach},{domain},{csvIvalue},{path},{csvRuntime},{csvSetSize}\n")

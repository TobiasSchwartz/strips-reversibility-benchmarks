#!/usr/bin/env python3

def domainFromDomainFileName(filename):
    if "singlePath" in filename:
        return "singlePath"
    elif "multiplePathsDeadEnds" in filename:
        return "multiplePathsDeadEnds"
    elif "multiplePaths" in filename:
        return "multiplePaths"
    elif "generalApproach" in filename:
        return "multiplePaths"
    elif "barabasiAlbertLongestShortestPath" in filename:
        return "barabasiAlbertLongestShortestPath"
    elif "barabasiAlbertDegree" in filename:
        return "barabasiAlbertDegree"

def horizonForDomainFileName(filename):
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
        "asp",
        "qasp",
    ]
    domains = [
        "singlePath",
        "multiplePaths",
        "multiplePathsDeadEnds",
        "generalApproach",
        "barabasiAlbertLongestShortestPath",
        "barabasiAlbertDegree",
    ]
    domainsFolder = "domains"

    [f.unlink() for f in Path(domainsFolder).glob("*") if f.is_file()]

    # Generate singlePath, multiplePaths, multiplePathsDeadEnds, domains
    # start = 10
    # limit = 50
    # step = 10

    # domainGenerator.generateStandardDomains(domainsFolder, start, limit, step, "singlePath")
    # domainGenerator.generateStandardDomains(domainsFolder, start, limit, step, "multiplePaths")
    # domainGenerator.generateStandardDomains(domainsFolder, start, limit, step, "multiplePathsDeadEnds")

    # Generate domains using Barabasi-Albert Longest Shortest Path method
    # n ~ m -> sometimes bfs, sometimes dfs faster
    # domainGenerator.generateBarabasiAlbertDomains(domainsFolder, 200, 199, "barabasiAlbertLongestShortestPath")

    # n = 2 * m -> dfs has many timeouts; bfs usually faster than dfs
    # domainGenerator.generateBarabasiAlbertDomains(domainsFolder, 200, 100, "barabasiAlbertLongestShortestPath")

    # n >> m -> dfs usually faster than bfs
    # domainGenerator.generateBarabasiAlbertDomains(domainsFolder, 200, 10, "barabasiAlbertLongestShortestPath")

    # domainGenerator.generateBarabasiAlbertDomains(domainsFolder, 1000, 999, "barabasiAlbertLongestShortestPath")
    # domainGenerator.generateBarabasiAlbertDomains(domainsFolder, 1000, 500, "barabasiAlbertLongestShortestPath")
    # domainGenerator.generateBarabasiAlbertDomains(domainsFolder, 1000, 50, "barabasiAlbertLongestShortestPath")

    # Generate domains based on the general approach
    domainGenerator.generateGeneralApproachDomain(domainsFolder, 2, 2, 31, 5)

    # Generate domains using Barabasi-Albert Degree method
    # n ~ m -> for some reason, no domains generated
    # domainGenerator.generateBarabasiAlbertDomains(domainsFolder, 200, 199, "barabasiAlbertDegree") 

    # n = 2 * m -> dfs usually faster than bfs; also not all domains generated
    # domainGenerator.generateBarabasiAlbertDomains(domainsFolder, 200, 100, "barabasiAlbertDegree")

    # n >> m -> dfs usually faster than bfs
    # domainGenerator.generateBarabasiAlbertDomains(domainsFolder, 200, 10, "barabasiAlbertDegree")

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
            domain = domainFromDomainFileName(path)
            csvIvalue = re.sub('[^0-9]', '', path)

            if approach == "bfs" and domain =="multiplePaths" and int(csvIvalue) > 15:
                continue

            # we do not want to give our approaches an edge by aborting early
            # only asp and qasp should know the horizon
            if approach == "asp" or approach == "qasp":
                horizon = horizonForDomainFileName(path)
            else:
                horizon = -1

            print(f"***************** Processing {path} using {approach} approach *****************\n")

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

            # append results
            with open(f"./experiments/experiment-{domain}-{approach}-{time}.csv", "a+") as f:
                f.write(f"{approach},{domain},{csvIvalue},{path},{csvRuntime},{csvSetSize}\n")

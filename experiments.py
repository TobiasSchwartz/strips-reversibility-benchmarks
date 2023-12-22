#!/usr/bin/env python3

def domainFromDomainFileName(filename):
    if "singlePath" in filename:
        return "singlePath"
    elif "multiplePathsDeadEnds" in filename:
        return "multiplePathsDeadEnds"
    elif "multiplePaths" in filename:
        return "multiplePaths"
    elif "barabasiAlbert" in filename:
        return "barabasiAlbert"

def horizonForDomainFileName(filename):
    import re
    domain_size = int(re.sub('[^0-9]', '', str(filename)))
    domain_size += 1
    if "singlePath" in filename:
        return (int)(domain_size)
    elif "multiplePathsDeadEnds" in filename:
        return (int)(((domain_size) * (domain_size + 1)) * 0.5)
    elif "multiplePaths" in filename:
        return (int)(((domain_size) * (domain_size + 1)) * 0.5)
    elif "barabasiAlbert" in filename:
        return (int)(filename.split("barabasiAlbert_")[1].split("-")[0])


if __name__ == "__main__":
    import benchmark
    from pathlib import Path
    import re
    import datetime
    import time

    import domainGenerator

    timeout = 60*10
    approaches = [
        "dfs",
        "bfs",
        # "asp"
    ]
    domains = [
        # "singlePath",
        # "multiplePaths",
        # "multiplePathsDeadEnds",
        "barabasiAlbert"
    ]
    domainsFolder = "domains"

    [f.unlink() for f in Path(domainsFolder).glob("*") if f.is_file()] 

    # domainGenerator.generateDomains(domainsFolder, 10, 500+10, 10, "singlePath")
    # domainGenerator.generateDomains(domainsFolder, 1, 36, 1, "multiplePaths")
    # domainGenerator.generateDomains(domainsFolder, 1, 36, 1, "multiplePathsDeadEnds")
    domainGenerator.generateDomains(domainsFolder, -1, -1, -1, "barabasiAlbert")

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
            

            print(f"***************** Processing {path} using {approach} approach *****************\n")
            horizon = horizonForDomainFileName(path)
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

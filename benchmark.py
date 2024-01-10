#!/usr/bin/env python3
import subprocess
import math
import time 
import re

def eval_domain_theirs(filename, horizon, timeoutLimit):
    
    c0 = f"mkdir -p artif_examples/"
    subprocess.run([c0], text=True, capture_output=True, shell=True)
    c1 = f"./plasp translate {filename} > ./artif_examples/{filename}.lp"
    subprocess.run(c1, text=True, capture_output=True, shell=True)
    c2 = f"/usr/bin/time -v ./clingo sequential-horizon.simple.elp -c horizon={horizon} artif_examples/{filename}.lp"
    try:
        output = subprocess.run(c2, text=True, capture_output=True, shell=True, timeout=timeoutLimit)
        print(output)

        wallClock = re.findall(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (.*?)\\n", str(output))[0]
        print(wallClock)
        setSize = re.findall(r"Maximum resident set size \(kbytes\): (.*?)\\n", str(output))[0]
        print(setSize)

        print(f"filename: {filename}")
        print(f"wallClock: {wallClock}")
        print(f"setSize: {setSize}")
        return (filename, wallClock, setSize)

    except TimeoutError:
        return (filename, -1, -1)

def eval_domain_ours(filename, strategy, horizon, timeoutLimit):
    try:
        c0 = f"/usr/bin/time -v ../reversible.py {filename} {strategy} {horizon}"
        output = subprocess.run(c0, text=True, capture_output=True, shell=True, timeout=timeoutLimit)
        print(output)
        wallClock = re.findall(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (.*?)\\n", str(output))[0]
        print(wallClock)
        setSize = re.findall(r"Maximum resident set size \(kbytes\): (.*?)\\n", str(output))[0]
        print(setSize)

        print(f"filename: {filename}")
        print(f"wallClock: {wallClock}")
        print(f"setSize: {setSize}")
        return (filename, wallClock, setSize)
    except TimeoutError:
        return (filename, -1, -1)

# TODO: deprecate? isn't called anywhere
def foo():
    from pathlib import Path

    path = "."

    # test_set = "singlePath"
    # test_set = "multiplePaths"
    test_set = "multiplePathsDeadEnds"


    time = time.time()
    with open(f"./benchmarks/benchmark-{test_set}-theirs-{time}.csv", "a+") as f:
            f.write("domain,seconds,mb\n")
    with open(f"./benchmarks/benchmark-{test_set}-ours-bfs-{time}.csv", "a+") as f:
            f.write("domain,seconds,mb\n")
    with open(f"./benchmarks/benchmark-{test_set}-ours-dfs-{time}.csv", "a+") as f:
            f.write("domain,seconds,mb\n")

    pathlist = Path(path).glob(f'../artif_examples/{test_set}_d*.pddl')
    for path in pathlist:
        print(path)   
        path_in_str = str(path)
        # find reverse plan for all domain definitions in specified folder
        print(f"***************** Processing {path_in_str} using their implementation *****************\n")

        domain_size = int(re.sub('[^0-9]', '', path_in_str))
        # for manyPreconditions
        # horizon = math.factorial(domain_size) + 1
        # for default/randomized
        # horizon = domain_size + 1
        # for quadratic (|D| * (|D|+1)) / 2
        horizon = (int) (((domain_size + 1) * (domain_size + 2)) / 2) + 1
        print(f"Horizon = {horizon}\n")

        (filename, wallClock, setSize) = eval_domain_theirs(path_in_str, horizon)
        filenameCSV = re.sub('[^0-9]', '', filename)
        import datetime
        foo  = datetime.datetime.strptime(wallClock, r'%M:%S.%f')
        wallClockCSV = (foo.minute * 60) + foo.second + (foo.microsecond / 1000000)
        setSizeCSV = int(setSize) / 1024

        # append results
        with open(f"./benchmarks/benchmark-{test_set}-theirs-{time}.csv", "a+") as f:
            f.write(f"{filenameCSV},{wallClockCSV},{setSizeCSV}\n")

        print(f"***************** Processing {path_in_str} using our implementation in bfs mode *****************\n")
        (filename, wallClock, setSize) = eval_domain_ours(path_in_str, "bfs", horizon)
        filenameCSV = re.sub('[^0-9]', '', filename)
        import datetime
        foo  = datetime.datetime.strptime(wallClock, r'%M:%S.%f')
        wallClockCSV = (foo.minute * 60) + foo.second + (foo.microsecond / 1000000)
        setSizeCSV = int(setSize) / 1024

        # append results
        with open(f"./benchmarks/benchmark-{test_set}-ours-bfs-{time}.csv", "a+") as f:
            f.write(f"{filenameCSV},{wallClockCSV},{setSizeCSV}\n")

        print(f"***************** Processing {path_in_str} using our implementation in dfs mode *****************\n")
        (filename, wallClock, setSize) = eval_domain_ours(path_in_str, "dfs", horizon)
        filenameCSV = re.sub('[^0-9]', '', filename)
        import datetime
        foo  = datetime.datetime.strptime(wallClock, r'%M:%S.%f')
        wallClockCSV = (foo.minute * 60) + foo.second + (foo.microsecond / 1000000)
        setSizeCSV = int(setSize) / 1024

        # append results
        with open(f"./benchmarks/benchmark-{test_set}-ours-dfs-{time}.csv", "a+") as f:
            f.write(f"{filenameCSV},{wallClockCSV},{setSizeCSV}\n")


def parseWallClock(output):
    return re.findall(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (.*?)\\n", str(output))[0]


def parseSetSize(output):
    return re.findall(r"Maximum resident set size \(kbytes\): (.*?)\\n", str(output))[0]


def benchmark(approach, domainPath, reversibleActionName, horizon, timeoutLimit):
    if approach == "bfs" or approach == "dfs":
        try:
            command = f"/usr/bin/time -v python3 ./reversible.py {domainPath} {reversibleActionName} {approach} {horizon} True"
            output = subprocess.run(command, text=True, capture_output=True, shell=True, timeout=timeoutLimit)
            print(output.stdout)
            wallClock = parseWallClock(output)
            setSize = parseSetSize(output)
            return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, wallClock, setSize)
        except (TimeoutError, subprocess.TimeoutExpired):
            print(f"TimeoutError after {timeoutLimit} seconds")
            return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, -1, -1)
    elif approach == "asp":
        c1 = f"/tools/plasp translate {domainPath} > {domainPath}.lp"
        subprocess.run(c1, text=True, capture_output=True, shell=True)

        c2 = f"/usr/bin/time -v /tools/clingo /tools/sequential-horizon.uurev.lp -c horizon={horizon} {domainPath}.lp"
        try:
            output = subprocess.run(c2, text=True, capture_output=True, shell=True, timeout=timeoutLimit)
            print(output.stdout)
            wallClock = parseWallClock(output)
            setSize = parseSetSize(output)
            return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, wallClock, setSize)
        except (TimeoutError, subprocess.TimeoutExpired):
            print(f"TimeoutError after {timeoutLimit} seconds")
            return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, -1, -1)
    else:
        print(f"The provided approach \"{approach}\" is not valid.")

if __name__ == "__main__":
    import fire
    fire.Fire(benchmark)
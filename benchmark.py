#!/usr/bin/env python3
import subprocess
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
        
    elif approach == "asp_simple":
        c1 = f"/tools/plasp translate {domainPath} > {domainPath}.lp"
        subprocess.run(c1, text=True, capture_output=True, shell=True)

        c2 = f"/usr/bin/time -v /tools/clingo /tools/sequential-horizon.simple.asp -c horizon={horizon} {domainPath}.lp"
        try:
            output = subprocess.run(c2, text=True, capture_output=True, shell=True, timeout=timeoutLimit)
            print(output.stdout)
            # print(" - ".join(output.stdout.split("\n")[4:6]))
            wallClock = parseWallClock(output)
            setSize = parseSetSize(output)
            return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, wallClock, setSize)
        except (TimeoutError, subprocess.TimeoutExpired):
            print(f"TimeoutError after {timeoutLimit} seconds")
            return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, -1, -1)
        
    elif approach == "asp_general":
        c1 = f"/tools/plasp translate {domainPath} > {domainPath}.lp"
        subprocess.run(c1, text=True, capture_output=True, shell=True)

        # use --opt-mode=optN to get all optimal plans
        c2 = f"/usr/bin/time -v /tools/clingo /tools/sequential-horizon.general.alt.asp -c horizon={horizon} {domainPath}.lp"
        try:
            output = subprocess.run(c2, text=True, capture_output=True, shell=True, timeout=timeoutLimit)
            print(" - ".join(output.stdout.split("\n")[4:6]))
            wallClock = parseWallClock(output)
            setSize = parseSetSize(output)
            return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, wallClock, setSize)
        except (TimeoutError, subprocess.TimeoutExpired):
            print(f"TimeoutError after {timeoutLimit} seconds")
            return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, -1, -1)
        
    elif approach == "qasp":
        c1 = f"python3 /tools/run-pddl-horizon.py {domainPath} {horizon} > {domainPath}.qasp"
        subprocess.run(c1, text=True, capture_output=True, shell=True)

        c2 = f"/usr/bin/time -v java -jar /tools/qasp-0.1.2.jar -mn 1 {domainPath}.qasp"
        try:
            output = subprocess.run(c2, text=True, capture_output=True, shell=True, timeout=timeoutLimit)
            # retrieve plan from output
            plan = re.findall(r'occurs\("(.*?)",', str(output.stdout))
            print(output.stdout.split("\n")[0])
            print(f"Plan: {'->'.join(plan[1:])}")
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

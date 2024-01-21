#!/usr/bin/env python3
import os
import signal
import subprocess
import re
import tempfile

def parseWallClock(output):
    return re.findall(r"\s*Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (.*?)\s*\n", output)[0]


def parseSetSize(output):
    return re.findall(r"\s*Maximum resident set size \(kbytes\): (.*?)\s*\n", output)[0]


def benchmark(approach, domainPath, reversibleActionName, horizon, timeoutLimit):
    if approach == "bfs" or approach == "dfs":
        try:
            command = f"/usr/bin/time -v python3 ./reversible.py {domainPath} {reversibleActionName} {approach} {horizon} True"
            with tempfile.TemporaryFile() as tempf:
                process = subprocess.Popen(command, stdout=tempf, stderr=tempf, shell=True, preexec_fn=os.setsid)
                try:
                    process.wait(timeout=timeoutLimit)
                except subprocess.TimeoutExpired:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    print(f"TimeoutError after {timeoutLimit} seconds")
                    return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, -1, -1)
                
                tempf.seek(0)
                output = tempf.read().decode('utf-8')
                # print(output)
                wallClock = parseWallClock(output)
                setSize = parseSetSize(output)
                process.terminate()
                print(f"Time: {wallClock} sec., Memory: {int(setSize)/1014:.2f} MB.")
                return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, wallClock, setSize)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, -1, -1)
        
    elif approach == "asp_simple":
        c1 = f"/tools/plasp translate {domainPath} > {domainPath}.lp"
        subprocess.run(c1, text=True, capture_output=True, shell=True)

        c2 = f"/usr/bin/time -v /tools/clingo /tools/sequential-horizon.simple.asp -c horizon={horizon} {domainPath}.lp"
        try:
            with tempfile.TemporaryFile() as tempf:
                process = subprocess.Popen(c2, stdout=tempf, stderr=tempf, shell=True, preexec_fn=os.setsid)
                try:
                    process.wait(timeout=timeoutLimit)
                except subprocess.TimeoutExpired:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    print(f"TimeoutError after {timeoutLimit} seconds")
                    return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, -1, -1)
                
                tempf.seek(0)
                output = tempf.read().decode('utf-8')
                print(output)
                wallClock = parseWallClock(output)
                setSize = parseSetSize(output)
                process.terminate()
                return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, wallClock, setSize)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, -1, -1)
        
    elif approach == "asp_general":
        c1 = f"/tools/plasp translate {domainPath} > {domainPath}.lp"
        subprocess.run(c1, text=True, capture_output=True, shell=True)

        # use --opt-mode=optN to get all optimal plans
        c2 = f"/usr/bin/time -v /tools/clingo /tools/sequential-horizon.general.alt.asp -c horizon={horizon} {domainPath}.lp"
        try:
            with tempfile.TemporaryFile() as tempf:
                process = subprocess.Popen(c2, stdout=tempf, stderr=tempf, shell=True, preexec_fn=os.setsid)
                try:
                    process.wait(timeout=timeoutLimit)
                except subprocess.TimeoutExpired:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    print(f"TimeoutError after {timeoutLimit} seconds")
                    return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, -1, -1)
                
                tempf.seek(0)
                output = tempf.read().decode('utf-8')
                # print(output)
                wallClock = parseWallClock(output)
                setSize = parseSetSize(output)
                return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, wallClock, setSize)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, -1, -1)
        
    elif approach == "qasp":
        c1 = f"python3 /tools/run-pddl-horizon.py {domainPath} {horizon} > {domainPath}.qasp"
        subprocess.run(c1, text=True, capture_output=True, shell=True)

        c2 = f"/usr/bin/time -v java -jar /tools/qasp-0.1.2.jar -mn 1 {domainPath}.qasp"
        try:
            with tempfile.TemporaryFile() as tempf:
                process = subprocess.Popen(c2, stdout=tempf, stderr=tempf, shell=True, preexec_fn=os.setsid)
                try:
                    process.wait(timeout=timeoutLimit)
                except subprocess.TimeoutExpired:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    print(f"TimeoutError after {timeoutLimit} seconds")
                    return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, -1, -1)
                
                tempf.seek(0)
                output = tempf.read().decode('utf-8')
                # retrieve plan from output
                plan = re.findall(r'occurs\("(.*?)",', output)
                # print(output.split("\n")[0])
                # print(f"Plan: {'->'.join(plan[1:])}")
                wallClock = parseWallClock(output)
                setSize = parseSetSize(output)
                process.terminate()
                return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, wallClock, setSize)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return (domainPath, approach, reversibleActionName, horizon, timeoutLimit, -1, -1)

    else:
        print(f"The provided approach \"{approach}\" is not valid.")

if __name__ == "__main__":
    import fire
    fire.Fire(benchmark)

#!/usr/bin/env python3

import networkx as nx
import random
import matplotlib.pyplot as plt

def singlePath(i):
    """
    Generates a PDDL domain where there exists only a single reverse plan for action del-all of length i.

    :param i: length of the single reverse plan
    :return: the PDDL doamin in string format
    """

    predicates = [f"(f{j})" for j in range(0, i+1)]

    not_predicates = [f"(not {p})" for p in predicates]

    newline = "\n"

    actions = [f"""
    (:action add-f{j}
    :precondition (f{j-1})
    :effect (f{j}))
    """ for j in range(1, i+1)]

    domain = f"""
    (define (domain rev-{i})
    (:requirements :strips)
    (:predicates {" ".join(predicates)})

    (:action del-all
    :precondition (and {" ".join(predicates)})
    :effect (and {" ".join(not_predicates)})
    )

    (:action add-f0
    :effect (f0))

    {newline.join(actions)}
    )
    """

    return domain


def multiplePaths(i):
    """
    Generates a PDDL domain with multiple reverse plans for action del-all of length 0.5 * i * (i+1).

    :param i: length of the single reverse plan
    :return: the PDDL doamin in string format
    """

    predicates = [f"(f{j})" for j in range(0, i+1)]

    not_predicates = [f"(not {p})" for p in predicates]

    newline = "\n"

    actions = [f"""
    (:action add-f{j}
    :precondition (f{j-1})
    :effect (and (f{j}) {' '.join([f'(not (f{i}))' for i in range(j)])}))
    """ for j in range(1, i+1)]

    domain = f"""
    (define (domain quadratic-{i})
    (:requirements :strips)
    (:predicates {" ".join(predicates)})

    (:action del-all
    :precondition (and {" ".join(predicates)})
    :effect (and {" ".join(not_predicates)}))

    (:action add-f0
    :effect (f0))

    {newline.join(actions)})
    """

    return domain


def multiplePathsDeadEnds(i):
    """
    Generates a PDDL domain with multiple reverse plans and possible dead ends for action del-all of length 0.5 * i * (i+1).

    :param i: length of the single reverse plan
    :return: the PDDL domain in string format
    """

    predicates = [f"(f{j})" for j in range(0, i+1)]

    not_predicates = [f"(not {p})" for p in predicates]

    newline = "\n"

    actions = [f"""
    (:action add-f{j}
    :precondition (f{j-1})
    :effect (and (f{j}) {' '.join([f'(not (f{i}))' for i in range(j)])}))
    """ for j in range(1, i+1)]

    domain = f"""
    (define (domain quadratic-{i})
    (:requirements :strips)
    (:predicates {" ".join(predicates + ["(token)"])})

    (:action del-all
    :precondition (and {" ".join(predicates + ["(token)"])})
    :effect (and {" ".join(not_predicates)}))

    (:action add-f0
    :effect (f0))

    {newline.join(actions)}

    (:action consume
    :precondition (token)
    :effect (not (token))))
    """

    return domain

def barabasiAlbert(m, n):
    """
    Generates a PDDL domain based on Barabasi-Albert graphs. Multiple test instances are returned for a domain. Only the ten node pairs with highest hop distance are considered.

    :param i: length of the single reverse plan
    :return: the PDDL domain in string format
    """

    seed = random.seed(246)

    from itertools import combinations

    G = nx.barabasi_albert_graph(m, n, seed=seed)
    shortest_paths = nx.all_pairs_shortest_path(G)
    G = nx.to_directed(G)

    shortest_paths = [list(paths.values()) for _, paths in shortest_paths]
    shortest_paths = [item for sublist in shortest_paths for item in sublist]
    longest_shortest_paths = sorted(shortest_paths, key=lambda x: len(x), reverse=True)[:10]

    for path in longest_shortest_paths:

        node_a = path[0]
        node_b = path[-1]

        predicates = [f"(f{j})" for j in G.nodes]

        not_predicates = [f"(not {p})" for p in predicates]

        newline = "\n"

        actions = [f"""
        (:action add-f{u}-f{v}
        :precondition (f{u})
        :effect (f{v}))
        """ for (u, v) in G.edges]

        domain = f"""
        (define (domain barabasiAlbert_{m}-{n}-{node_a}-{node_b})
        (:requirements :strips)
        (:predicates {" ".join(predicates)})

        (:action del-all
        :precondition (and {" ".join([f"(f{node})" for node in path])})
        :effect (and {" ".join(not_predicates)})
        )

        (:action add-f{node_a}
        :effect (f{node_a}))

        {newline.join(actions)}
        )
        """

        yield (f"barabasiAlbert_{m}-{n}-{node_a}-{node_b}", domain)

        # nx.draw(G, with_labels=True)
        # plt.savefig("graph_visualization.png", format="png")
        # nx.draw(G)
        # break


def generateDomains(folder, start, limit, step, domain):
    """
    Generates domains for the specified domain name using the provided domain function following the range for the i value.
    Start and limit specify the upper and lower bound of the argument i for the to be generated domains, step the increment at each step.
    Currently the highest possible value for limit is 999.

    :param folder: folder in which the PDDL domains shall be written to
    :param start: start value of argument i
    :param limit: limit of argument i
    :param step: step increment of argument i
    :param domain: domain type to be created ("singlePath", "multiplePaths", or "multiplePathsDeadEnds")
    """

    from pathlib import Path
    Path(folder).mkdir(parents=True, exist_ok=True)

    if domain == "barabasiAlbert":
         # generate barabasi-albert domains (multiple test cases per domain)
        n, m = (5, 2)

        for (test_case_name, test_case) in barabasiAlbert(n, m):
            print(f"Generating {test_case_name} domain ... ")

            filename = f"{folder}/{test_case_name}.pddl"
            with open(filename, "w") as f:
                f.write(test_case)
                f.close()
            print(f"and saved as file \"{filename}\"", end="")
            print("")

    else:
        # generate singlePath, multiplePath, and multiplePathsDeadEnds domains
        if limit >= 1000:
            print("The limit is only supported up to a value of 999.")
            return
        domainFunctions = [singlePath, multiplePaths, multiplePathsDeadEnds]
        
        if domain not in [f.__name__ for f in domainFunctions]:
            print(f"The provided domain \"{domain}\" does not have a corresponding domain function.")
            return
        domainFunction = [f for f in domainFunctions if f.__name__ == domain][0]

        for i in range(start, limit+1, step):
            print(f"Generating {domain} domain for input i = {i} ... ", end="")
            domainString = domainFunction(i)
            print(f"done ... ", end="")
            filename = f"{folder}/{domain}_d{str(i).zfill(3)}.pddl"
            with open(filename, "w") as f:
                f.write(domainString)
                f.close()
            print(f"and saved as file \"{filename}\"", end="")
            print("")

    
if __name__ == "__main__":
    import fire
    fire.Fire(generateDomains)

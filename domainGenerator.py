#!/usr/bin/env python3

import networkx as nx
import random

global domain_id
domain_id = 0

def generate_domain_id():
    global domain_id
    domain_id += 1

    return str(domain_id).zfill(4)

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


def generalApproach(num_plans_success, length_plans_success, num_plans_dead_end, length_plans_dead_end):
    """
    Generates a PDDL domain with a fixed number of plans of length i leading to the same goal state,
    and a fixed number of plans of length i leading to a dead end.

    :param num_plans_success: number of plans leading to the goal state
    :param length_plans_success: length of the plans leading to the goal state
    :param num_plans_dead_end: number of plans leading to a dead end
    :param length_plans_dead_end: length of the plans leading to a dead end
    :return: the PDDL domain in string format
    """

    total_states = num_plans_success * (length_plans_success-1) + num_plans_dead_end * length_plans_dead_end + 2
    print(f"total_states: {total_states}")

    predicates = [f"(f{j})" for j in range(0, total_states)]

    not_predicates = [f"(not {p})" for p in predicates]

    newline = "\n"

    goal = f"(f{total_states-1})"
    next_state = 1
    to_goal = []

    # first generate all plans leading to the goal state
    actions = []

    for _ in range(num_plans_success):
        actions.append(f"""
    (:action add-f0-f{next_state}
    :precondition (f0)
    :effect (and (f{next_state})))
        """)

        for _ in range(1,length_plans_success-1):
            next_state += 1
            actions.append(f"""
    (:action add-f{next_state-1}-f{next_state}
    :precondition (f{next_state-1})
    :effect (and (f{next_state})))
            """)

        actions.append(f"""
    (:action add-f{next_state}-goal
    :precondition (f{next_state})
    :effect (and {goal} (not (f{next_state}))))
        """)
        to_goal.append(f"(f{next_state})")
        next_state += 1

    # then generate all plans leading to a dead end
    for _ in range(num_plans_dead_end):
        actions.append(f"""
    (:action add-f0-f{next_state}
    :precondition (f0)
    :effect (and (f{next_state}) ))
        """)

        for _ in range(1,length_plans_dead_end):
            next_state += 1
            # (not (f{next_state-1}))
            actions.append(f"""
    (:action add-f{next_state-1}-f{next_state}
    :precondition (f{next_state-1})
    :effect (and (f{next_state})))
            """)
        next_state += 1

    domain = f"""
    (define (domain benchmark-{num_plans_success}-{length_plans_success}-{num_plans_dead_end}-{length_plans_dead_end})
    (:requirements :strips)
    (:predicates {" ".join(predicates)})

    (:action del-all
    :precondition (and {goal} {" ".join([f"(not {p})" for p in predicates if p != goal])})
    :effect (and (f0) {" ".join([p for p in not_predicates if p != "(not (f0))"])}))

    (:action pre-goal
    :precondition (and {" ".join(to_goal)})
    :effect (and {goal} {" ".join([f"(not {p})" for p in predicates if p != goal])}))

    {newline.join(actions)}
    )
    """

    return domain


def barabasiAlbertLongestShortestPath(n, m):
    """
    Generates ten PDDL domains based on Barabasi-Albert graph with the provided parameters. Only the ten node pairs with highest hop distance are considered.

    :param i: length of the single reverse plan
    :return: the PDDL domain in string format
    """

    seed = random.seed(246)

    G = nx.barabasi_albert_graph(m=m, n=n, seed=seed)
    shortest_paths = nx.all_pairs_shortest_path(G)
    G = nx.to_directed(G)

    shortest_paths = [list(paths.values()) for _, paths in shortest_paths]
    shortest_paths = [item for sublist in shortest_paths for item in sublist]
    longest_shortest_paths = sorted(shortest_paths, key=len, reverse=True)[:10]

    for path in longest_shortest_paths:

        path_length = len(path) - 1
        node_a = path[0]
        node_b = path[-1]

        node_a_pred = f"(f{node_a})"
        node_b_pred = f"(f{node_b})"

        predicates = [f"(f{j})" for j in G.nodes]

        not_predicates = [f"(not {p})" for p in predicates]

        newline = "\n"

        actions = [f"""
        (:action add-f{u}-f{v}
        :precondition (f{u})
        :effect (and (f{v}) (not (f{u}))))
        """ for (u, v) in G.edges]

        domain = f"""
        (define (domain barabasiAlbert_{m}-{n}-{node_a}-{node_b}-{path_length})
        (:requirements :strips :negative-preconditions)
        (:predicates {" ".join(predicates)})

        (:action del-all
        :precondition (and {node_b_pred} {" ".join([f"(not {p})" for p in predicates if p != node_b_pred])})
        :effect (and {" ".join(not_predicates)})
        )

        (:action add-f{node_a}
        :effect {node_a_pred})

        {newline.join(actions)}
        )
        """
        yield (f"{generate_domain_id()}-barabasiAlbertLongestShortestPath-{m}-{n}-{node_a}-{node_b}-{path_length}", domain)


def barabasiAlbertDegree(n, m):
    """
    Generates a PDDL domain based on Barabasi-Albert graphs. Multiple test instances are returned for a domain. Only the ten node pairs with highest hop distance are considered.

    :param i: length of the single reverse plan
    :return: the PDDL domain in string format
    """

    seed = random.seed(246)

    G = nx.barabasi_albert_graph(m=m, n=n, seed=seed)
    G = nx.to_directed(G)

    # sort nodes by degree
    sorted_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)

    # start at most connected node
    node_a = sorted_nodes[0][0]
    
    node_pairs = []
    for i in range(1, len(sorted_nodes)):
        node_b = sorted_nodes[i][0]
        shortest_path_length = nx.shortest_path_length(G, node_a, node_b)
        if shortest_path_length > 1:
            node_pairs.append((node_a, node_b, shortest_path_length))
            if len(node_pairs) == 10:
                break

    for node_a, node_b, path_length in node_pairs:

        node_a_pred = f"(f{node_a})"
        node_b_pred = f"(f{node_b})"

        predicates = [f"(f{j})" for j in G.nodes]
        not_predicates = [f"(not {p})" for p in predicates]

        newline = "\n"

        actions = [f"""
        (:action add-f{u}-f{v}
        :precondition (f{u})
        :effect (and (f{v}) (not (f{u}))))
        """ for (u, v) in G.edges]

        domain = f"""
        (define (domain barabasiAlbert_{m}-{n}-{node_a}-{node_b}-{path_length})
        (:requirements :strips :negative-preconditions)
        (:predicates {" ".join(predicates)})

        (:action del-all
        :precondition (and {node_b_pred} {" ".join([f"(not {p})" for p in predicates if p != node_b_pred])})
        :effect (and {" ".join(not_predicates)})
        )

        (:action add-f{node_a}
        :effect {node_a_pred})

        {newline.join(actions)}
        )
        """

        yield (f"{generate_domain_id()}-barabasiAlbertDegree-{m}-{n}-{node_a}-{node_b}-{path_length}", domain)


def generateStandardDomains(folder, start, limit, step, domain):
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

        filename = f"{folder}/{generate_domain_id()}-{domain}-{i}.pddl"
        with open(filename, "w") as f:
            f.write(domainString)
            f.close()
        print(f"and saved as file \"{filename}\"", end="")
        print("")


def generateGeneralApproachDomain(folder, num_plans_success, length_plans_success, num_plans_dead_end, length_plans_dead_end):
    """
    Generates a domain based on the general approach for generating domains.

    :param num_plans_success: number of plans leading to the goal state
    :param length_plans_success: length of the plans leading to the goal state
    :param num_plans_dead_end: number of plans leading to a dead end
    :param length_plans_dead_end: length of the plans leading to a dead end
    """

    from pathlib import Path
    Path(folder).mkdir(parents=True, exist_ok=True)

    path_length = max(length_plans_success, length_plans_dead_end)

    domain_name = f"{generate_domain_id()}-generalApproach-{num_plans_success}-{length_plans_success}-{num_plans_dead_end}-{length_plans_dead_end}-{path_length}"

    print(f"Generating {domain_name} domain ... ")

    domain = generalApproach(num_plans_success, length_plans_success, num_plans_dead_end, length_plans_dead_end)

    filename = f"{folder}/{domain_name}.pddl"
    with open(filename, "w") as f:
        f.write(domain)
        f.close()
    print(f"and saved as file \"{filename}\"", end="")
    print("")


def generateBarabasiAlbertDomains(folder, n, m, domain):
    """
    Generates domains based on Barabasi-Albert networks.

    :param folder: folder in which the PDDL domains shall be written to
    :param n: number of nodes
    :param m: number of nodes to be linked to new node with respect to p_i
    :param domain: domain type to be created ("barabasiAlbertLongestShortestPath" or "barabasiAlbertDegree")
    """

    from pathlib import Path
    Path(folder).mkdir(parents=True, exist_ok=True)

    if domain == "barabasiAlbertLongestShortestPath":
         # generate barabasiAlbertLongestShortestPath domains (multiple test cases per domain, currently 10)

        for (test_case_name, test_case) in barabasiAlbertLongestShortestPath(n, m):
            print(f"Generating {test_case_name} domain ... ")

            filename = f"{folder}/{test_case_name}.pddl"
            with open(filename, "w") as f:
                f.write(test_case)
                f.close()
            print(f"and saved as file \"{filename}\"", end="")
            print("")

    if domain == "barabasiAlbertDegree":
         # generate barabasiAlbertDegree domains (multiple test cases per domain, currently 2)

        for (test_case_name, test_case) in barabasiAlbertDegree(n, m):
            print(f"Generating {test_case_name} domain ... ")

            filename = f"{folder}/{test_case_name}.pddl"
            with open(filename, "w") as f:
                f.write(test_case)
                f.close()
            print(f"and saved as file \"{filename}\"", end="")
            print("")

    
if __name__ == "__main__":
    import fire
    fire.Fire(generateStandardDomains, generateGeneralApproachDomain, generateBarabasiAlbertDomains)

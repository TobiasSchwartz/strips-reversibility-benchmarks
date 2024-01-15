#!/usr/bin/env python3

from typing import Type

from action import Action
from PDDL import PDDL_Parser


class State:
    def __init__(self, Fplus, Fminus, F0, pi):
        super().__init__()
        self.Fplus = Fplus
        self.Fminus = Fminus
        self.F0 = F0
        self.pi = pi

    def isEquiv(self, otherState):
        """Two states are considered equivalent if their share the same Fplus, Fminus, and F0 values.
        Note that the path pi is not considered during this check.
        """
        if self.Fplus != otherState.Fplus:
            return False
        if self.Fminus != otherState.Fminus:
            return False
        if self.F0 != otherState.F0:
            return False
        return True

    def print(self):
        print(f"F0: {', '.join([str(elem[0]) for elem in self.F0])}")
        print(f"Fplus: {', '.join([str(elem[0]) for elem in self.Fplus])}")
        print(f"Fminus: {', '.join([str(elem[0]) for elem in self.Fminus])}")
        print(f"pi: "+" -> ".join([str(p.name) for p in self.pi]))
        print(f"Path length: {str(len(self.pi))}")


def pre_a(action):
    # return action.negative_preconditions.union(action.positive_preconditions)
    return action.positive_preconditions


def del_a(action):
    return action.del_effects


def add_a(action):
    return action.add_effects


def algorithm(action, actions, strategy, maxPathLimit=-1):
    """
    This function follows the definition of Algorithm 1 from the paper
    
    M. Morak, L. Chrpa, W. Faber, and D. Fiser,
    "On the reversibility of actions in planning"
    in Proceedings of the 17th International Conference on
    Principles of Knowledge Representation and Reasoning, KR 2020,
    Rhodes, Greece, September 12-18, 2020,
    D. Calvanese, E. Erdem, and M. Thielscher, Eds.,
    2020, pp. 652–661.

    :param action: the to be reversed action
    :param actions: all actions present in the domain
    :param strategy: "dfs" for depth-first search or "bfs" for breadth-first search
    :param maxPathLimit: -1 for no limit, otherwise the algorithm wont explore paths exceeding this limit
    :return: a generator, which yields states that resemble valid reverse plans.
    """
    ongoing = []
    visited = []

    Fplus = (pre_a(action).difference(del_a(action))).union(add_a(action))
    Fminus = del_a(action)
    F0 = set()
    pi = []
    initState = State(Fplus, Fminus, F0, pi)
    ongoing.append(initState)

    while ongoing:
        if strategy == "bfs":
            state = ongoing.pop(0)
        elif strategy == "dfs":
            state = ongoing.pop()

        state = state  # type: State

        visited.append(state)

        if pre_a(action).issubset(state.Fplus) and len(state.F0.intersection(state.Fminus)) == 0:
            yield state
            continue

        possibleActions = []
        for aa in actions:
            aa = aa  # type: Action
            if len(pre_a(aa).intersection(state.Fminus)) == 0:
                possibleActions.append(aa)

        for aa in possibleActions:

            newState = State(
                Fplus=(state.Fplus.difference(del_a(aa))).union(add_a(aa)),
                Fminus=(state.Fminus.difference(add_a(aa))).union(del_a(aa)),
                F0=state.F0.union(pre_a(aa).difference(state.Fplus)),
                pi=(state.pi + [aa])
            )

            # do not consider actions that do not modify the current state
            if newState.F0 == state.F0 and newState.Fplus == state.Fplus and newState.Fminus == state.Fminus:
                continue

            # do not explore paths exceeding the provided maxPathLimit
            if maxPathLimit != -1 and len(newState.pi) > maxPathLimit:
                continue

            # only add a new state if it has not been explored so far
            existsAlready = False
            for s in ongoing + visited:
                if s.isEquiv(newState):
                    existsAlready = True
                    break
            if not existsAlready:
                ongoing = ongoing + [newState]


def find_rev(domainPathStr, reversibleActionName, strategy, maxPathLimit=-1, findSingleSolution=True):
    """
    Wrapper for the above algorithm function for computing the reversibility.

    :param domainPathStr: Path to the PDDL domain file
    :param strategy: "dfs" for depth-first search or "bfs" for breadth-first search
    :param maxPathLimit: -1 for no limit, otherwise the algorithm wont explore paths exceeding this limit
    :param reversibleActionName: name of the action to be reversed
    :param findSingleSolution: whether a single solution or all solutions should be computed
    """
    parser = PDDL_Parser()

    try:
        parser.parse_domain(domainPathStr)

        actionFound = False
        for action in parser.actions:
            if action.name != reversibleActionName:
                continue
            actionFound = True
            print(f"Computing a reverse plan for action \"{reversibleActionName}\" ... ", end="")

            generator = algorithm(
                action,
                parser.actions,
                strategy,
                maxPathLimit=maxPathLimit
            )
            print("I have found the following solutions:")
            for state in generator:
                state.print()
                print()
                if findSingleSolution:
                    print("I wont look for further solutions, because \"findSingleSolution\" is enabled")
                    break
    except Exception as e:
        print(
            f"Computation aborted due to problems encountered while parsing domain {domainPathStr}!")
        print(e)

    if not actionFound:
        print(
            f"Could not find action \"\{reversibleActionName}\" in domain {domainPathStr}")


if __name__ == "__main__":
    import fire
    fire.Fire(find_rev)

# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # DFS used stack to store the nodes for finding the deepest nodes
    # in the search tree

    # initialize
    fringe = util.Stack()
    visitedNode = set()

    # push the starting point into the stack
    fringe.push((problem.getStartState(), []))

    # while the stack is not empty
    while not fringe.isEmpty():
        # pop out the point
        t = fringe.pop()  # t[0] = currNode ,t[1] = action ,t[2] = cost
        if t[0] not in visitedNode:
            visitedNode.add(t[0])

            if (problem.isGoalState(t[0]) != False):
                return t[1]
            successor = problem.getSuccessors(t[0])  # get the point's successors for the loop
            for son in successor:
                # The successor has not been visited so push it into stack
                if son[0] not in visitedNode and son[0] not in fringe.list:
                    # son[0] = nextNode ,son[1] = action ,son[2] = cost
                    fringe.push((son[0], t[1] + [son[1]]))

    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # initialize
    fringe = util.Queue()
    visitedNode = set()
    # push the starting point into the queue
    fringe.push((problem.getStartState(), []))

    while not fringe.isEmpty():
        # pop out the point
        t = fringe.pop()  # t[0] = currNode ,t[1] = action ,t[2] = cost
        # there is the goal point
        if (problem.isGoalState(t[0]) != False):
            return t[1]

        # Add currNode to Explored List
        if t[0] not in visitedNode:
            visitedNode.add(t[0])
            # The successor has not been visited so push it into queue
            successor = problem.getSuccessors(t[0])
            for son in successor:
                # son[0] = nextNode ,son[1] = action ,son[2] = cost
                if son[0] not in visitedNode:
                    fringe.push((son[0], t[1] + [son[1]]))  # push in the queue
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # initialize
    fringe = util.PriorityQueue()
    visitedNode = set()

    # push the starting point with priority number
    fringe.push((problem.getStartState(), [], 0), 0)
    while not fringe.isEmpty():
        t = fringe.pop()
        # currNode = t[0]  ,action = t[1]  ,cost = t[2]
        if (problem.isGoalState(t[0]) != False):
            return t[1]

        if t[0] not in visitedNode:
            visitedNode.add(t[0])

            successor = problem.getSuccessors(t[0])
            for son in successor:
                # child_Node = son[0], child_Path = son[1], child_Cost = son[2]
                if son[0] not in visitedNode:
                    fringe.push((son[0], t[1] + [son[1]], t[2] + son[2]), t[2] + son[2])
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue()
    # push the starting point with priority number
    fringe.push((problem.getStartState(), [], 0), 0)
    visitedNode = []
    while not fringe.isEmpty():
        t = fringe.pop()
        # currentNode=t[0]  ,actions = t[1]  ,prevCost=t[2]
        if t[0] not in visitedNode:
            visitedNode.append(t[0])

            if (problem.isGoalState(t[0]) != False):
                return t[1]

            successor = problem.getSuccessors(t[0])

            for son in successor:
                if son[0] not in visitedNode:
                    # nextNode = son[0] ,action = son[1] ,cost = son[2]
                    fringe.push((son[0], t[1] + [son[1]], t[2] + son[2]),
                                t[2] + son[2] + heuristic(son[0], problem))
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

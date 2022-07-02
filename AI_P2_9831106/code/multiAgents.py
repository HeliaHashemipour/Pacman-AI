# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        # there is two situation for getting score
        score = 0
        foodDist = [util.manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]

        if len(foodDist) > 0:
            score += float(1 / min(foodDist))
        else:
            score += 1

        for ghost in newGhostStates:
            distance = abs(newPos[0] - ghost.getPosition()[0]) + abs(newPos[1] - ghost.getPosition()[1])
            if distance > 1:  # there is not ghost & check the new position
                score += float(1 / distance)
            # return large negative value
            elif distance == 1:
                return -1000

        score += successorGameState.getScore()
        return score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        ghostsNumbers = gameState.getNumAgents()

        def maximumValue(gameState, depth):
            maxValue = float('-inf')
            depth = depth - 1  # reduce the size of depth
            # Returns a list of legal actions for an agent & ghosts are >= 1
            print(depth)
            legalActions = gameState.getLegalActions(0)

            # conditions for end
            if depth == 0:
                return self.evaluationFunction(gameState)
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)  # Returns the minimax action from the current gameState

            # get the max value from all its successor
            for action in legalActions:
                # Returns the successor game state after an agent takes an action
                maxValue = max(maxValue, minimumValue(gameState.generateSuccessor(0, action), depth, 1))
            return maxValue

        def minimumValue(gameState, depth, agentIndex):
            minValue = float('inf')
            legalActions = gameState.getLegalActions(agentIndex)

            if gameState.isWin() or gameState.isLose():  # the conditions for end
                return self.evaluationFunction(gameState)  # Returns the minimax action from the current gameState

            for action in legalActions:
                if agentIndex < (ghostsNumbers - 1):
                    minValue = min(minValue,
                                   minimumValue(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1))
                else:
                    minValue = min(minValue, maximumValue(gameState.generateSuccessor(agentIndex, action), depth))
            return minValue

        def result():
            maxValue = float('-inf')
            res = 0

            for action in gameState.getLegalActions(0):
                Action = self.depth
                actionValue = minimumValue(gameState.generateSuccessor(0, action), Action,
                                           1)  # Returns the minimax action from the current gameState
                if actionValue > maxValue:
                    maxValue = actionValue
                    res = action
            return res

        return result()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        ghostsNumbers = gameState.getNumAgents()

        def maximumValue(gameState, depth, Alpha, Beta):
            legalActions = gameState.getLegalActions(0)
            depth = depth - 1
            actionValue = float('-inf')  # max value

            # conditions for end
            if depth == 0:
                return self.evaluationFunction(gameState)

            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            for action in legalActions:
                actionValue = max(actionValue,
                                  minimumValue(gameState.generateSuccessor(0, action), depth, 1, Alpha, Beta))
                if actionValue > Beta:
                    return actionValue
                Alpha = max(Alpha, actionValue)
            return actionValue

        def minimumValue(gameState, depth, agentIndex, Alpha, Beta):
            actionValue = float('inf')  # minValue
            legalActions = gameState.getLegalActions(agentIndex)

            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            for action in legalActions:
                if agentIndex < (ghostsNumbers - 1):
                    actionValue = min(actionValue, minimumValue(gameState.generateSuccessor(agentIndex, action), depth,
                                                                agentIndex + 1, Alpha, Beta))
                else:
                    actionValue = min(actionValue,
                                      maximumValue(gameState.generateSuccessor(agentIndex, action), depth, Alpha, Beta))
                if actionValue < Alpha:
                    return actionValue
                Beta = min(Beta, actionValue)
            return actionValue

        def result():
            res = 0
            maxValue = float('-inf')
            Alpha = float('-inf')
            Beta = float('inf')
            legalActions = gameState.getLegalActions(0)

            for action in legalActions:
                Action = self.depth
                actionValue = minimumValue(gameState.generateSuccessor(0, action), Action, 1, Alpha, Beta)
                if actionValue > Alpha:
                    res = action
                    Alpha = actionValue
            return res

        return result()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        ghostsNumbers = gameState.getNumAgents()

        def maximumValue(gameState, depth):
            depth = depth - 1
            legalActions = gameState.getLegalActions(0)
            maxValue = float('-inf')
            # conditions for end
            if depth == 0:
                return self.evaluationFunction(gameState)

            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            for action in legalActions:
                maxValue = max(maxValue, getExpectation(gameState.generateSuccessor(0, action), depth, 1))
            return maxValue

        def getExpectation(gameState, depth, agentIndex):
            sum = 0
            result = 0
            legalActions = gameState.getLegalActions(agentIndex)
            num_actions = len(gameState.getLegalActions(agentIndex))

            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            for action in legalActions:
                if agentIndex < (ghostsNumbers - 1):
                    expValue = getExpectation(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
                else:
                    expValue = maximumValue(gameState.generateSuccessor(agentIndex, action), depth)
                sum += expValue
                result = float((sum) / (num_actions))
            return result

        def result():
            maxValue = float('-inf')
            res = 0

            for action in gameState.getLegalActions(0):
                Action = self.depth
                actionValue = getExpectation(gameState.generateSuccessor(0, action), Action, 1)
                if actionValue > maxValue:
                    res = action
                    maxValue = actionValue
            return res

        return result()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    score = 0
    newGhostStates = currentGameState.getGhostPositions()

    # Feature 1: food positions
    foodDist = [util.manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]

    if len(foodDist) > 0:
        score += float(1 / min(foodDist))
    else:
        score += 1

    ghostsDis = 1
    ghostsNear = 0
    # Feature 2:  distances from ghosts if exists
    for ghost in newGhostStates:
        distance = util.manhattanDistance(newPos, ghost)
        ghostsDis += util.manhattanDistance(newPos, ghost)
        score -= float(1 / (ghostsDis))
        if distance <= 1:
            ghostsNear += 1
        elif distance == 1:
            return -10000
    # Feature 3: capsules positions
    numberOfCapsules = len(currentGameState.getCapsules())

    score = score + currentGameState.getScore() - 2 * ghostsNear - 20 * numberOfCapsules
    return score


# Abbreviation
better = betterEvaluationFunction

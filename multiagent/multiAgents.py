# multiAgents.py 
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
import itertools
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
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    ##print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    if (action == Directions.STOP):
      return -float("inf") 
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    enemyLs = [ghost.configuration.pos for ghost in newGhostStates if ghost.scaredTimer == 0]
    posDist = lambda other: util.manhattanDistance(other, newPos)
    foodList = oldFood.asList()
    minFoodDist = 0
    minEnemyDist = 0
    if foodList:
      minFoodDist = min(map(posDist, oldFood.asList()))
      if minFoodDist == 0:
        minFoodDist = -10

    if enemyLs:
      minEnemyDist = min(map(posDist, enemyLs)) 
      if minEnemyDist == 0:
        return -float("inf")


    return 0.75*minEnemyDist - 1.75*minFoodDist

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  ans = currentGameState.getScore()
  ##print(ans)
  return ans

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

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
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

      c:
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    PACMAN = 0
    
    numSharp = gameState.getNumAgents()


  #Inner-function----------------------------------------------------START
    def other_helper(gameState, agent):
      if gameState.isLose() or gameState.isWin() or agent//numSharp == self.depth:
        return (None, self.evaluationFunction(gameState))

      agentNum = agent%numSharp
      currentState = None
      action = None

      val =  -float("inf") if agentNum == PACMAN else float("inf")
      comp = (lambda x,y: x > y)  if agentNum == PACMAN else (lambda x,y: x < y)

      if agentNum == PACMAN:
        options = [option for option in  gameState.getLegalActions(agentNum) if option != Directions.STOP ] 
      else:
        options = gameState.getLegalActions(agentNum)

      for option in options:
        currentState = gameState.generateSuccessor(agentNum, option)
        currentVal = other_helper(currentState, agent + 1)[1]
        if comp(currentVal, val):
          val = currentVal
          action = option
      if action is None:
        action = random.choice(options)
      return (action, val)

    action = other_helper(gameState, PACMAN)
    # print(action)

    return action[0]
    #Inner-function----------------------------------------------------END

      




  



class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    PACMAN = 0
    
    numSharp = gameState.getNumAgents()


  #Inner-function----------------------------------------------------START
    def alpha_helper(gameState, agent, alpha, beta):
      if gameState.isLose() or gameState.isWin() or agent//numSharp == self.depth:
        return (None, self.evaluationFunction(gameState))

      agentNum = agent%numSharp
      currentState = None
      action = None

      val =  -float("inf") if agentNum == PACMAN else float("inf")
      comp = (lambda x,y: x > y)  if agentNum == PACMAN else (lambda x,y: x < y)

      if agentNum == PACMAN:
        options = [option for option in  gameState.getLegalActions(agentNum) if option != Directions.STOP ] 
      else:
        options = gameState.getLegalActions(agentNum)

      for option in options:
        currentState = gameState.generateSuccessor(agentNum, option)
        currentVal = alpha_helper(currentState, agent + 1, alpha, beta)[1]
        if comp(currentVal, val):
          val = currentVal
          action = option
        if agentNum == PACMAN:
          if val > beta:
            break
          alpha = max(alpha, val)
        else:
          if(val < alpha):
            break
          beta = min(beta, val)
      if action is None:
        action = random.choice(options)
      return (action, val)

    action = alpha_helper(gameState, PACMAN, -float("inf"),float("inf"))
    # print(action)

    return action[0]
    #Inner-function----------------------------------------------------END

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
    PACMAN = 0
    
    numSharp = gameState.getNumAgents()


    #Inner-function----------------------------------------------------START
    def random_helper(gameState, agent):
      if gameState.isLose() or gameState.isWin() or agent//numSharp == self.depth:
        return (None, self.evaluationFunction(gameState))

      agentNum = agent%numSharp
      currentState = None
      action = None

      val = -float("inf") 

      if agentNum == PACMAN:
        options = [option for option in  gameState.getLegalActions(agentNum) if option != Directions.STOP ] 
      else:
        options = gameState.getLegalActions(agentNum)

      valMorgolis = []
      for option in options:
        currentState = gameState.generateSuccessor(agentNum, option)
        currentVal = random_helper(currentState, agent + 1)[1]
        if(agentNum != PACMAN):
          valMorgolis.append(currentVal)
        if currentVal > val:
          val = currentVal
          action = option
      val = val if agentNum == PACMAN  else sum(valMorgolis)/len(valMorgolis) 
      if action is None:
        action = random.choice(options)
      return (action, val)
    #Inner-function----------------------------------------------------END
    action = random_helper(gameState, PACMAN)
    # print(action)

    return action[0]
    


def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: We calculated the following metrics:
      a) Metrics we want to maximize:
        * Distance to the closest scary ghost (minEnemyDist)
        * The score of the current game state (currentGameState.getScore())
      b) Metrics we want to minimize:
        * Distance to the closest food palet (minFoodDist)
        * Number of capsules (length of capsules list)
        * Number of scary ghosts (length of enemyLs list)
    Some of these metrics are more inportant than others, hence we factored them by multiplying 
    by 75 and 20 (capsules and scary ghosts respectively).
  """
  if currentGameState.isLose():
    return -float("inf")
  elif currentGameState.isWin():
    return float("inf")
    
  newPos = currentGameState.getPacmanPosition()
  oldFood = currentGameState.getFood()
  newGhostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

  enemyLs = [ghost.configuration.pos for ghost in newGhostStates if ghost.scaredTimer == 0]
  posDist = lambda other: util.manhattanDistance(other, newPos)
  foodList = oldFood.asList()
  minFoodDist = 0
  minEnemyDist = 0

  if foodList:
    minFoodDist = min(map(posDist, oldFood.asList()))
    if minFoodDist == 0:
      minFoodDist = -10

  if enemyLs:
      minEnemyDist = min(map(posDist, enemyLs)) 


  capsules = currentGameState.getCapsules()

          #factors we want to maximize-------------------factors we want to minimize  
  return (minEnemyDist + currentGameState.getScore()) - (minFoodDist  + 75*len(capsules) + 20*( len(enemyLs))) 

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()





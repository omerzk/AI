# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
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
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print("Start:", problem.getStartState())
  print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
  print("Start's successors:", problem.getSuccessors(problem.getStartState()))
  """
  frontier = util.Stack()
  startState = problem.getStartState();
  visited = {}
  cameFrom = dict([(startState, None)])
  frontier.push((startState,))
  current = None
  while(not frontier.isEmpty()):
    current = frontier.pop()
    if (current[0] in visited):
      continue
    visited[current[0]] = True
    if problem.isGoalState(current[0]):
      break
    for successor in problem.getSuccessors(current[0]):
      if(successor[0] not in visited):
        cameFrom[successor[0]] = (current[0], successor[1])
        frontier.push(successor)
  
  path = []
  current = current[0]
  while (current != startState):
    path.append(cameFrom[current][1])
    current = cameFrom[current][0]
  path.reverse();
  return path;


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  frontier = util.Queue()
  startState = problem.getStartState();
  cameFrom = dict([(startState, None)])#added startstate
  frontier.push((startState,))
  current = None
  while(not frontier.isEmpty()):
    current = frontier.pop()
    if problem.isGoalState(current[0]):
      break
    for successor in problem.getSuccessors(current[0]):
      if(successor[0] not in cameFrom):
        cameFrom[successor[0]] = (current[0], successor[1])
        frontier.push(successor)
    
  path = []
  current = current[0]
  while (current != startState):
    path.append(cameFrom[current][1])
    current = cameFrom[current][0]
  path.reverse();
  return path;
  


def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  startState = problem.getStartState();
  cameFrom = dict([(startState , (None,None, 0))])#added startstate
  PriorityFunc = lambda state: cameFrom[state[0]][2] if len(state) > 2  else  0
  frontier = util.PriorityQueueWithFunction(PriorityFunc)
  frontier.push((startState,))
  current = None
  while(not frontier.isEmpty()):
    current = frontier.pop()
    if problem.isGoalState(current[0]):
      break
    for successor in problem.getSuccessors(current[0]):
      if(successor[0] not in cameFrom or cameFrom[successor[0]][2] > successor[2] + cameFrom[current[0]][2]):
        cameFrom[successor[0]] = (current[0], successor[1], successor[2] + cameFrom[current[0]][2])
        frontier.push(successor)
      
  path = []
  current = current[0]
  while (current != startState):
    path.append(cameFrom[current][1])
    current = cameFrom[current][0]
  path.reverse();
  return path;




def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  cameFrom = {}
  costSoFar = {}
  frontier = util.PriorityQueue()
  startState = problem.getStartState();
  costSoFar[startState] = 0
  frontier.push((startState,), 0)
  current = None
  while(not frontier.isEmpty()):
    current = frontier.pop()
    if problem.isGoalState(current[0]):
      break
    for successor in problem.getSuccessors(current[0]):
      cost = costSoFar[current[0]] + successor[2]
      if successor[0] not in costSoFar or cost < costSoFar[successor[0]]:
        costSoFar[successor[0]] = cost
        cameFrom[successor[0]] = (current[0], successor[1])
        frontier.push(successor, cost + heuristic(successor[0], problem))
  
  path = []
  current = current[0]
  while (current != startState):
    path.append(cameFrom[current][1])
    current = cameFrom[current][0]
  path.reverse();
  return path;
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
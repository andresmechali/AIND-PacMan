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

import time
from collections import OrderedDict

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

		This method returns the total cost of a particular sequence of actions.	 The sequence must
		be composed of legal moves
		"""
		util.raiseNotDefined()
		   

def tinyMazeSearch(problem):
	"""
	Returns a sequence of moves that solves tinyMaze.	 For any other
	maze, the sequence of moves will be incorrect, so only use this for tinyMaze
	"""
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return	[s,s,w,s,w,w,s,w]

class Node:
	def __init__(self, position, parent, action):
		self.position = position # (x, y)
		self.parent = parent # of class Node
		self.action = action # of class Directions
	
def depthFirstSearch(problem):
	
	# Get start position
	start = Node(problem.getStartState(), None, None)
	
	# Initialize frontier
	frontier = util.Stack()
	frontier.push(start)
	
	# Initialize empty explored stack
	explored = util.Stack()
	
	# Both lists are for checking easier if a position has already been explored
	exploredPos = []
	frontierPos = []
	
	# Initialize path
	path = []
	
	while not frontier.isEmpty():
		
		# Get last element from the frontier
		next = frontier.pop()

		# Check if it is the goal
		if problem.isGoalState(next.position):
			# Add every action needed to the path
			while next.parent is not None:
				path.append(next.action)
				next = next.parent
			# Reverse the path
			path = path[::-1]
		
		# Add Node to explored list
		explored.push(next)
		
		# Add position to explored and frontier list for checking
		exploredPos.append(next.position)
		frontierPos.append(next.position)
		
		# Get posible actions
		actions = problem.getSuccessors(next.position)
		
		# Add the new actions to the frontier
		for action in actions:
			if action[0] not in exploredPos and action[0] not in frontierPos:
				frontier.push(Node(action[0], next, action[1]))
		
	return path

def breadthFirstSearch(problem):
	"""
	Search the shallowest nodes in the search tree first.
	[2nd Edition: p 73, 3rd Edition: p 82]
	"""
	"*** YOUR CODE HERE ***"
	
	start = Node(problem.getStartState(), None, None)
	
	frontier = util.Queue()
	frontier.push(start)
	
	explored = util.Stack()
	
	exploredPos = []
	frontierPos = []
	
	path = []
	
	while not frontier.isEmpty():
		
		next = frontier.pop()
		
		explored.push(next)
		
		# Add position to explored and frontier list for checking
		exploredPos.append(next.position)
		frontierPos.append(next.position)
		
		actions = problem.getSuccessors(next.position)
		
		for action in actions:
			if action[0] not in exploredPos and action[0] not in frontierPos:
				if problem.isGoalState(action[0]):
					next = Node(action[0], next, action[1])
					# Add every action needed to the path
					while next.parent is not None:
						path.append(next.action)
						next = next.parent
					# Reverse the path
					path = path[::-1]
					return path
				frontier.push(Node(action[0], next, action[1]))

	  
def uniformCostSearch(problem):
	"Search the node of least total cost first. "
	
	# Starting state
	start = Node(problem.getStartState(), None, None)
	
	# Initialize frontier and push start, with cost 0
	frontier = util.PriorityQueue()
	frontier.push(start, 0)
	
	#Initialize empty explored set
	explored = util.Stack()
	
	# Initialize empty list of explored positions, for checking later
	exploredPos = []
	
	# Initialize path
	path = []
	
	# Check if there are items in the frontier
	while not frontier.isEmpty():
	
		# Take from the frontier the node with the least cost
		next = frontier.pop()
		
		# If goal reached, terminate and return path
		if problem.isGoalState(next.position):
			while next.parent is not None:
				path.insert(0, next.action)
				next = next.parent
			return path
			
		# Add the th explored set
		explored.push(next)
		exploredPos.append(next.position) # This one is a list of explored positions, for easier comparison
		
		# Add current node to the frontier, for later checking
		frontierPos = [i[1].position for i in frontier.heap] + [next.position]
		
		# Get available next actions
		actions = problem.getSuccessors(next.position)
		
		for action in actions:
			child = Node(action[0], next, action[1]) # Action in Node format
			if action[0] not in exploredPos and action[0] not in frontierPos: # If not in explored or frontier...
				frontier.push(child, problem.costFn(action[0])) # Add to the frontier, with the corresponding cost
			elif action[0] in frontierPos: # If it was already in the frontier...
				try:
					for i in range(len(frontier.heap)):
						if frontier.heap[i][1].position == child.position: # If the cost is smaller, replace in the heap
							if problem.costFn(action[0]) < frontier.heap[i][0]:
								frontier.heap[i] = (problem.costFn(action[0]), child)
				except:
					print 'except'
	
	

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.	 This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"Search the node that has the lowest combined cost and heuristic first."
	"*** YOUR CODE HERE ***"
	util.raiseNotDefined()
	
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

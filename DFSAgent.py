class DFSAgent(Agent):

	# Initialization Function: Called one time when the game starts
		# Initialization Function: Called one time when the game starts
	def registerInitialState(self, state):
		return ;

	def getAction(self, state):
		# get all legal actions for pacman
		legal = state.getLegalPacmanActions()

		#Successors is the queue in my program.I am going to pop out the last element each time
		#Successors-(state, action, depth of the node which initially will be 1)
		successors = [(state.generatePacmanSuccessor(action), [action], 1) for action in legal]
		visitedstates=[]	#visited states
		leaf=[]				#consists of leaf-node states(state,originaldirection at begining, nodescore(depth+heuristic))
		while successors:
			#get the last element of the stack
			currentstate=successors.pop()
			depth=currentstate[2]
			if currentstate[0] not in visitedstates:
				if currentstate[0].isWin():
					nodescore=depth+admissibleHeuristic(currentstate[0])
					leaf.append([currentstate[0],currentstate[1],nodescore])
				elif currentstate[0].isLose():
					continue
				else:
					legal=currentstate[0].getLegalPacmanActions()
					l1=[]		#to insert first successor at last position of stack later in the list "successor" outside of the loop
					for action in legal:
						newsuccessors=currentstate[0].generatePacmanSuccessor(action)
						if newsuccessors is not None and not newsuccessors.isLose():
							l1.insert(0,(newsuccessors,currentstate[1],depth+1))
						else:
							nodescore=depth+admissibleHeuristic(currentstate[0])
							if (currentstate[0],currentstate[1],nodescore) not in leaf:
								leaf.append((currentstate[0],currentstate[1],nodescore))
					for x in l1:
						successors.append(x)
					
					visitedstates.append(currentstate[0])

		if len(leaf)>0:
			action_to_return=min(leaf,key=lambda x: x[2])[1]
			if type(action_to_return)==list:		#In case there are multiple same values it returns list else string
				return str(action_to_return[0])
			else:
				return str(action_to_return)



				
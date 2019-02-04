class BFSAgent(Agent):

	# Initialization Function: Called one time when the game starts
	def registerInitialState(self, state):
		return ;

	# GetAction Function: Called with every frame
	def getAction(self, state):
		# TODO: write BFS Algorithm instead of returning Directions.STOP
		legal = state.getLegalPacmanActions()

		#Successors is the queue in my program.I am going to pop out the 0th element each time
		#Successors-(state,action, depth of the node which initially will be 1)
		successors = [(state.generatePacmanSuccessor(action), [action],1) for action in legal]

		allstates=[]	#visited states
		leaf=[]			#consists of leaf-node states(state,originaldirection at begining, nodescore(depth+heuristic))
		while successors:
			#get the first element of the stack
			currentstate=successors.pop(0)
			depth=currentstate[2]
			if currentstate[0] not in allstates:
				if currentstate[0].isWin():
					return currentstate[1]
				elif currentstate[0].isLose():
					continue
				else:
					legal=currentstate[0].getLegalPacmanActions()
					for action in legal:
						newsuccessors=currentstate[0].generatePacmanSuccessor(action)
						if newsuccessors is not None and not newsuccessors.isLose():
							successors.append((newsuccessors,currentstate[1],depth+1))
						else:
							nodescore=depth+admissibleHeuristic(currentstate[0])
							if (currentstate[0],currentstate[1],nodescore) not in leaf:
								leaf.append((currentstate[0],currentstate[1],nodescore))
					allstates.append(currentstate)
		if len(leaf)>0:
			action_to_return=min(leaf,key=lambda x: x[2])[1]
			if type(action_to_return)==list:				#In case there are multiple same values it returns list else string
				return str(action_to_return[0])
			else:
				return str(action_to_return)


				
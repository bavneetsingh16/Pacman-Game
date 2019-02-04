class Node:
	def __init__(self, state, parent, actionList, children,visited,score,action):
		self.parent = parent
		self.actionList = actionList
		self.children = children
		self.state = state
		self.visited=visited
		self.score=score
		self.action=action


class MCTSAgent(Agent):
	
	# Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    total=0


    def traverse_choice(self,node):
        len_actionList=len(node.actionList)
        r=random.randint(0, len_actionList-1)
        random_choice=node.actionList[r]
        node.actionList.pop(r)
        child_state=node.state[0].generatePacmanSuccessor(random_choice)
        if child_state is None:
            return None
        if child_state.isWin() or child_state.isLose():
            child_actionList=[]
    	else:
        	child_actionList=child_state.getLegalPacmanActions()
        s=node.state
        s.append(random_choice)    #always storing the root and all actions leading to this node

        #child.score value is initially assigned 1 and later updated
        child=Node(s, node,child_actionList,[],1,1,random_choice)   #visited node here is assigned 1 and is not considered during update
        child.score=self.rollout(child,child_state)    #child.score value is updated correctly
        
        self.update(child)
        node.children.append(child)
        return;

    def rollout(self,node,current_state):
        possible=node.actionList
        maximum_value=-1 * float('inf')
        for i in range(5):
        	if len(possible)>1:
        		current_state=current_state.generatePacmanSuccessor(possible[random.randint(0, len(possible)-1)])
        	elif len(possible)==1:
        		current_state=current_state.generatePacmanSuccessor(possible[0])

        	else:
        		try:
        			current_state=current_state.generatePacmanSuccessor(possible[random.randint(0, len(possible)-1)])
        		except:
        			return 0

        	if current_state is None or current_state.isLose():
        		return 0
        	else:
        		possible=current_state.getLegalPacmanActions()
        		score=gameEvaluation(node.state[0], current_state)
        return score

#backpropagation and updation of nodes
    def update(self,node):
    	while node.parent is not None:
    		node = node.parent
    		node.visited+=1
    		node.score+=node.score
    		self.total=node.visited
    		
#To compare children of nodes to give back the best node
    def compare(self,node):
    	c=1
    	maximum_value=-1 * float('inf')                #-(infinity) is the initial value of maximum_value
    	if len(node.children)>0:
	    	for i in node.children:
	    		val = (i.score/i.visited) + 1 * math.sqrt(2*math.log(self.total)/float(i.visited))
	    		if val>maximum_value:
	    			maximum_value=val
	    			selected_child=i
	    	return selected_child
    	return None




    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        node=Node([state], None, state.getLegalPacmanActions(),[],0,0,Directions.STOP)
        root=node
    	flag=0

    	#Proper traversal of nodes
    	while True:
    		if node is None:
    			flag=1
    			break
    		if len(node.actionList)>0:
    			while len(node.actionList)>0:
    				self.traverse_choice(node)
    			flag=2
    		else:
	    		node=self.compare(node)
	    	if flag==2:
	    		node=root
	    		flag=0

	    #To give most visited node
        max_value=0
        for i in root.children:
        	if i.visited>=max_value:
        		max_value=i.visited

        ans=[]
        for i in root.children:
        	if i.visited==max_value:
        		ans.append(i.action)

        if len(ans)>0:
        	return ans[random.randint(0,len(ans)-1)]

        return Directions.STOP


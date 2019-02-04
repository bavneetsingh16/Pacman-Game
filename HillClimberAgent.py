class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        possible=state.getAllPossibleActions()
        actionList=range(5)
        for i in range(0,len(actionList)):
            actionList[i] = possible[random.randint(0,len(possible)-1)]
        sequencescore=[]
        visitedactions=[]
        temp = []
        while True:
            flag=0
            temp_actionList=[]
            tempList=actionList[:]
            finalstate=state
            while len(actionList)!=0:
                action=actionList.pop(0)
                temp_actionList.append(action)
                finalstate=finalstate.generatePacmanSuccessor(action)
                if finalstate is None:
                    flag=1
                    break
                elif finalstate.isWin():
                    break
                elif finalstate.isLose():
                    flag=2
                    break
            if flag==1:
                break
            else:
                if flag!=2:
                    score=gameEvaluation(state,finalstate)
                    if len(sequencescore)==0:
                        sequencescore=(tempList[0],score)
                    else:
                        if score>sequencescore[1]:
                            sequencescore=(tempList[0],score)
 
            for i in range(0,len(temp_actionList)):
                r=random.uniform(0,1)
                if r>=0.5:
                    temp_actionList[i] = possible[random.randint(0,len(possible)-1)]

            actionList=temp_actionList[:]


            
        if sequencescore:
            return sequencescore[0]
        else:
            return Directions.STOP
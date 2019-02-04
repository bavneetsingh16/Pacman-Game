class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    def ranking(self, state,chromosome):
        while len(chromosome)!=0:
            actionList=chromosome.pop(0)
            temp=actionList[:]
            finalstate=state
            flag=0
            while len(actionList)!=0:
                action=actionList.pop(0)
                finalstate=finalstate.generatePacmanSuccessor(action)
                if finalstate is None:
                    flag=1
                    break
                elif finalstate.isWin():
                    break
                elif finalstate.isLose():
                    break
            if flag==1:
                break
            else:
                score=gameEvaluation(state,finalstate)
                self.sequencescore.append((temp,score))
        if flag!=1:
            self.sequencescore=sorted(self.sequencescore,key=lambda x:x[1])
            for i in range(1,len(self.sequencescore)+1):
                self.sequencescore[i-1]=(i,self.sequencescore[i-1][1],self.sequencescore[i-1][0])
            return self.sequencescore,flag
        else:
            return self.sequencescore,1

    def probability(self):
        n=len(self.sequencescore)
        ranksum=float(((n)*(n+1))/2)
        for i in range(0,len(self.sequencescore)):
            self.sequencescore[i]=(self.sequencescore[i][0],self.sequencescore[i][0]/ranksum,self.sequencescore[i][1],self.sequencescore[i][2])
        return self.sequencescore

    def parentSelection(self):
        parentList=[]
        flag=0
        while len(parentList)<2:
            random_num=random.uniform(0,1)
            i=0
            while len(self.sequencescore)!=0 and i<len(self.sequencescore):
                prob=self.sequencescore[i][1]
                if prob>=random_num:
                    parentList.append(self.sequencescore[i][3])
                    self.sequencescore.pop(i)
                    if len(parentList)==2:
                        flag=1
                        break

                i+=1
            if flag==1:
                break
        return parentList

    def crossover(self,first_parent,second_parent):
        cross=[]
        for i in range(0,len(first_parent)):
            r=random.randint(0,10)
            if r<5:
                cross.append(first_parent[i])
            else:
                cross.append(second_parent[i])
        return cross

    def mutation(self,state,new_generation):
        possible=state.getAllPossibleActions()
        for i in range(0, len(new_generation)):
            r = random.randint(0,10)
            if r <= 1:
                rand = random.randint(0,4)
                action = possible[random.randint(0, len(possible) - 1)]
                new_generation[i][rand] = action
        return new_generation


#performs both crossover and mutation
    def cross_mutation(self,state,parentList):
        rand=random.randint(0,10)
        a,b=parentList
        new_generation=[]
        if rand<7:
            new_generation.append(self.crossover(a,b))
            new_generation.append(self.crossover(b,a))
        else:
            new_generation.append(a)
            new_generation.append(b)
        new_chromosomes=self.mutation(state,new_generation)
        return new_chromosomes



    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Genetic Algorithm instead of returning Directions.STOP
        possible=state.getAllPossibleActions()
        actionList=range(5)
        chromosome=[]
        for i in range(0, 8):
            actionList = []
            for j in range(0, 5):                           # 5= lenActionList
                actionList.append(possible[random.randint(0, len(possible)-1)])
            chromosome.append(list(actionList))
        self.sequencescore=[]
        max_value=[0,""]
        while(True):
            new_generation=[]
            self.sequencescore,flag=self.ranking(state,chromosome)
            if flag==1:
                break
            #To check value against max_value
            if self.sequencescore[len(self.sequencescore)-1][1]>max_value[0]:
                max_value=(self.sequencescore[len(self.sequencescore)-1][1],self.sequencescore[len(self.sequencescore)-1][2][0])

            self.sequencescore=self.probability()
            while(len(self.sequencescore)!=0):
                parentList=self.parentSelection()
                cross_mutationList=self.cross_mutation(state,parentList)
                for i in cross_mutationList:
                    new_generation.append(i)

            chromosome=new_generation[:]

        return max_value[1]
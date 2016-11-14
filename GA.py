import __future__
import random
import copy
import time
import heapq
from numpy import random as nr
import numpy as np
import FeatureCombination as FC


class Ga(self):
    def __init__(self,MutationPropability,popsize,codesize,weight_file,num_of_one,f_dict):
        self.yourcode=[[]]
        self.BestCode=[]
        self.BestEvaluation=[]
        self.popsize=popsize
        self.codesize=codesize
        self.MutationPropability=MutationPropability
        self.evaluations=[0 for i in range(popsize)]
        self.weightfile=weight_file
        self.probability=[0 for i in range(codesize)]
        self.num_of_one=num_of_one
        self.f_dict=f_dict

    def CreateOneCode(self,probability):
        random_p=nr.uniform(0,1,self.codesize)
        multi=random_p*probability
        max_N_multi=heapq.nlargest(self.num_of_one,multi)
        code=[1 if multi[r] in max_N_multi else 0 for r in range(self.codesize)]
        return code
    
    def CreateCodes(self):
        for last in open(self.weightfile):
            pass
        last=last.split()
        probability=[0 for i in range(codesize)]
        for i in range(1,len(probability)-1):
            pair = last[i].split(":")
            probability[int(pair[0])-1] = float(pair[1])
        probability=np.array(probability)
        for _ in range(self.codesize):
            yourcodes.append(self.CreateOneCode(probability))
        return yourcodes

    def Crossmotion(self,fater,mother):
        a=random.randint(0,len(father)/2-1)
        b=random.randint(len(father)/2,len(mother)-1)
        s=father[0:a]+mother[a:b]+father[b:]
        son=[]
        for i in s:
            if i not in son:
                son.append(i)
        return son
    def Mutation(self):
        for i in range(len(self.yourcode)):
            if random.uniform(0,1)<self.MutationPropability:
                code=self.Mutationmotion(self.yourcode[i])
                while self.Constrain(code)==false:
                    code=self.Mutationmotion(self.yourcode[i])
                self.yourcode[i]=code
    def Crossover(self):
        code=[[0 for i in range(len(self.yourcode[0]))] for j in range(len(self.yourcode))]
        for i in range(len(self.yourcode)):
            code[i]=self.Crossmotion(self.yourcode[i],self.yourcode[random.randint(0,len(self.yourcode))])
            while self.Constrain(code[i])==false:
                code[i]=self.Crossmotion(self.yourcode[i],self.yourcode[random.randint(0,len(self.yourcode))])
        selectpropability=self.Selectpropability(code)
        for j in range(len(code)):
            if random.uniform(0,1)<selectpropability[j]:
                self.yourcode[j]=code[j]

    def Mutationmotion(self,father):
        a=random.randint(0,len(father))
        b=random.randint(0,len(father))
        c=father[a]
        father[a]=father[b]
        father[b]=c
        return father

    def Constration(self,code):
        #if you have constration,add your constration
        return true

    def Evaluate(self,codes):
        evaluation = []
        for code in codes:
            new_num = 0
            true_num = 0
            new_with_true = 0
            n_feature=FC.GetNewFeature(self.f_dict , code)
            for hint in n_feature:
                new_num += 1
                true_num += 1
                if n_feature[hint][0]==1 and n_feature[hint][1]==1:
                    new_with_true += 1
            eva=new_with_true/(new_num+true_num)
            evaluation.append(eva)
        return evaluation

    def SelectPropability(self,code):
        self.evaluations=self.Evaluate(code)
        selectpropability=[self.evaluations[i]/sum(self.evaluations) for i in range(len(self.evaluations))]
        return selectpropability

    def SaveBest(self,evaluation,featuredict):
        return

    #包括两种更新方式，使用非线性分布概率选择
    def UpdateCodes(self,codes):
        return update_codes

    def main(self):
        codes = self.CreateCodes() #得到初始种群
        init_evaluation = self.Evaluate(codes)
        for _ in range(self.generation):
            self.SaveBest(init_evaluation )
            codes=self.UpdateCodes(codes)
            u_evaluation=self.Evaluate(codes)
            '''
            self.BestEvaluation.append(max(self.evaluations))
            maxindex=self.evaluations.index(max(self.evaluations))
            self.BestCode.append(self.yourcode[maxindex])
            '''
        besteva=max(self.evaluations)
        bestcode=self.Bestcode[besteva]
        return besteva,bestcode




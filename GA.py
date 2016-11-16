import __future__
import random
import copy
import time
import heapq
from numpy import random as nr
import numpy as np
from collections import defaultdict
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

    def RandomCrossmotion(self,fater,mother):
        new_code=[]
        for i in range(self.codesize):
            new_code.append(random.choice([fater[i] , mother[i]]))
        while sum(new_code) < self.num_of_one:
            a=random.randint(0,self.codesize)
            new_code[a] = 1
        return new_code

    def ProbabilityCrossmotion(self,f_code,m_code,f_evaluation,m_evaluation):
        pf=f_evaluation/(f_evaluation+m_evaluation)
        new_code=[]
        for i in range(self.codesize):
            if random.random() > pf:
                new_code.append(m_code[i])
            else:
                new_code.append(f_code[i])
        while sum(new_code) < self.num_of_one:  #暂时使用随机补全
            a=random.randint(0,self.codesize)
            new_code[a] = 1
        return new_code

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
    
    #暂时使用随机选择
    def SelectCodes(self,codes,u_evaluation):
        f_evaluation = random.choice(u_evaluation)
        f_code = codes[u_evaluation.index(f_evaluation)]
        m_evaluation = random.choice(u_evaluation)
        m_code = codes[u_evaluation.index(f_evaluation)]
        return (f_code,m_code,f_evaluation,m_evaluation)

    def SaveBest(self,evaluation,codes):
        max_eva=max(evaluation)
        best_code=codes[evaluation.index(max_eva)]
        f=open('best_code.txt','a')
        f.write(i for i in best_code)
        f.close()
        print ("evaluation : " , max_eva)
    
    def UpdateProbability(self,s_p,eva):
        c=0
        beta1=0.5
        beta2=0.5
        PN=[]
        sum_p=0
        up=sorted(eva , reverse=True)
        p1=c/self.popsize
        pm=(2-c)/self.popsize
        PN.append(pm)
        for i in range(1,self.popsize-1):
            pi=pm+(self.popsize-i)*(pm-1)/(self.popsize-1)
            PN.append(pi)
        PN.append(p1)
        mean_eva=sum(up)/len(up)
        for i in range(self.popsize):
            if up[i]>mean_eva:
                sum_p+=PN[i]
        if sum_p > 0.75:
            s_p=s_p+beta1*s_p*(1-s_p)
        elif sum_p < 0.35:
            s_p=s_p-beta2*s_p*(1-s_p)
        return s_p

    #包括两种更新方式，使用非线性分布概率选择
    def UpdateCodes(self,codes,s_p,u_evaluation):
        c_d=defaultdict(list)
        eva=[]
        update_codes=[]
        for i in range(self.codesize):
            r=random.random()
            if r <= s_p:
                (f_code,m_code,f_evaluation,m_evaluation) = self.SelectCodes(codes,u_evaluation)
                new_code = self.RandomCrossmotion(f_code,m_code)
                c_d['random'].append(new_code)
            else:
                (f_code,m_code,f_evaluation,m_evaluation) = self.SelectCodes(codes,u_evaluation)
                new_code = self.ProbabilityCrossmotion(f_code,m_code,f_evaluation,m_evaluation)
                c_d['probability'].append(new_code)
            update_codes.append(new_code)
        eva=self.Evaluate(c_d['probability'])
        s_p = self.UpdateProbability(s_p,eva)
        return (update_codes , c_d , s_p)

    def main(self):
        codes = self.CreateCodes() #得到初始种群
        u_evaluation = self.Evaluate(codes)
        select_probability=0.5
        for _ in range(self.generation):
            self.SaveBest(u_evaluation , codes)
            (codes , codes_distribution , select_probability)=self.UpdateCodes(codes , select_probability , u_evaluation)
            u_evaluation=self.Evaluate(codes)
            '''
            self.BestEvaluation.append(max(self.evaluations))
            maxindex=self.evaluations.index(max(self.evaluations))
            self.BestCode.append(self.yourcode[maxindex])
            '''
        besteva=max(self.evaluations)
        bestcode=self.Bestcode[besteva]
        return besteva,bestcode




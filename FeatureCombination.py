from collections import defaultdict
import json
import GA

feature_inputfile="feature_hint.tsv"
label_inputfile="target_hint.tsv"
MutationPropability=0
popsize=0
codesize=0
weight_file=0
num_of_one=0

def GetNewFeature(f_dict , code):
    new_feature={}
    for hint in f_dict:
        l=f_dict[hint][0]
        new_feature[hint]=[1 if code[l[r]]==1 else 0 for r in range(len(l))]
    return new_feature

def UseGA(f_dict):
    ga=GA.Ga(MutationPropability,popsize,codesize,weight_file,num_of_one) # need add value
    best=ga.main(f_dict)
    return


if __name__ == "__main__":
    feature_dict=defaultdict(list)
    for line in open(feature_inputfile):
        line = line.strip().split('\t')
        if line[1] != '{}':
            feature_dict[line[0]].append(set(json.loads(i) for i in line[1].strip('{').strip('}').strip(" ").split(',')))
        else:
            feature_dict[line[0]].append(set({}))
    for line in open(label_inputfile):
        line = line.strip().split('\t')
        feature_dict[line[1]].append(int(line[2]))
    UseGA(feature_dict)


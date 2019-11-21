from Graph import *
import matplotlib.pyplot as plt
import numpy as np

def plotAgeGroups():
    actors = g.getActors()
    ageMapping = {}
    for actor in actors:
        if actor["age"] == None:
            continue
        age = int(actor["age"])
        if age not in ageMapping:
            ageMapping[age] = 1
        else:
            ageMapping[age] += 1
    plt.bar(ageMapping.keys(), ageMapping.values(), 10, color='g')
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Ages')
    plt.ylabel('Frequency')
    plt.title('Age Histogram')
    plt.show()

def plotAgeGroupsAndMoney():
    actors = g.getActors()
    ageMapping = {}
    for actor in actors:
        if actor["age"] == None or actor["total_gross"] == None:
            continue
        age = int(actor["age"])
        gross = float(actor["total_gross"])
        if age not in ageMapping:
            ageMapping[age] = gross
        else:
            ageMapping[age] += gross
    plt.bar(ageMapping.keys(), ageMapping.values(), 10, color='b')
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Ages')
    plt.ylabel('Money Generated')
    plt.title('Revenue by Age-group Histogram')
    plt.show()

def plotHubActors():
    actors = g.getActors()
    mapping = {}
    for actor in actors:
        if actor["movies"] == None or len(actor["movies"]) == 0:
            continue
        for movie in actor["movies"]:
            mNode = g.getMnode(movie)
            if mNode != None:
                if actor["name"] not in mapping:
                    mapping[actor["name"]] = len(mNode.getActors()) - 1
                else:
                    mapping[actor["name"]] += len(mNode.getActors()) - 1
    data = sorted(mapping.items(), key = lambda tup : tup[1], reverse=True)[0:15]
    people = [tup[0] for tup in data]
    freq = [tup[1] for tup in data]
    indexes = np.arange(len(people))
    width = 0.7
    plt.bar(indexes, freq, width)
    plt.xticks(indexes + width * 0.5, people)
    plt.xticks(rotation=90)
    plt.ylabel("Connections")
    plt.title("Actors ranked by connections with other actors")
    plt.show() 


if __name__ == "__main__":
    g = Graph("data.json")
    plotAgeGroups()
    plotAgeGroupsAndMoney()
    plotHubActors()
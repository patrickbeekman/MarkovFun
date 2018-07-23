import numpy as np
import random

# https://www.datacamp.com/community/tutorials/markov-chains-python-tutorial
class DataCampEx:

    def __init__(self):
        self.states = []
        self.transitionName =[]
        self.transitionMatrix = []

    def main(self):
        # The statespace
        self.states = ["Sleep", "Icecream", "Run"]

        # Possible sequences of events
        self.transitionName = [["SS", "SR", "SI"], ["RS", "RR", "RI"], ["IS", "IR", "II"]]

        # Probabilities matrix (transition matrix)
        self.transitionMatrix = [[0.2, 0.6, 0.2], [0.1, 0.6, 0.3], [0.2, 0.7, 0.1]]

    # A function that implements the Markov model to forecast the state/mood.
    def activity_forecast(self, days):
        # Choose the starting state
        activityToday = "Sleep"
        print("Start state: " + activityToday)
        # Shall store the sequence of states taken. So, this only has the starting state for now.
        activityList = [activityToday]
        i = 0
        # To calculate the probability of the activityList
        prob = 1
        while i != days:
            if activityToday == "Sleep":
                change = np.random.choice(self.transitionName[0],replace=True,p=self.transitionMatrix[0])
                if change == "SS":
                    prob = prob * 0.2
                    activityList.append("Sleep")
                    pass
                elif change == "SR":
                    prob = prob * 0.6
                    activityToday = "Run"
                    activityList.append("Run")
                else:
                    prob = prob * 0.2
                    activityToday = "Icecream"
                    activityList.append("Icecream")
            elif activityToday == "Run":
                change = np.random.choice(self.transitionName[1],replace=True,p=self.transitionMatrix[1])
                if change == "RR":
                    prob = prob * 0.5
                    activityList.append("Run")
                    pass
                elif change == "RS":
                    prob = prob * 0.2
                    activityToday = "Sleep"
                    activityList.append("Sleep")
                else:
                    prob = prob * 0.3
                    activityToday = "Icecream"
                    activityList.append("Icecream")
            elif activityToday == "Icecream":
                change = np.random.choice(self.transitionName[2],replace=True,p=self.transitionMatrix[2])
                if change == "II":
                    prob = prob * 0.1
                    activityList.append("Icecream")
                    pass
                elif change == "IS":
                    prob = prob * 0.2
                    activityToday = "Sleep"
                    activityList.append("Sleep")
                else:
                    prob = prob * 0.7
                    activityToday = "Run"
                    activityList.append("Run")
            i += 1
        print("Possible states: " + str(activityList))
        print("End state after "+ str(days) + " days: " + activityToday)
        print("Probability of the possible sequence of states: " + str(prob))


dc = DataCampEx()
dc.main()
#!/usr/bin/env python3

import argparse
import sys
import numpy as np
import math

sys.path.insert(0, "../ChironCore/")
from irhandler import *
from ChironAST.builder import astGenPass
import csv


def fitnessScore(IndividualObject):
    """
    Parameters
    ----------
    IndividualObject : Individual (definition of this class is in ChironCore/sbfl.py)
        This is a object of class Individual. The Object has 3 elements
        1. IndividualObject.individual : activity matrix.
                                    type : list, row implies a test
                                    and element of rows are components.
        2. IndividualObject.fitness : fitness of activity matix.
                                    type : float
        3. Indivisual.fitness_valid : a flag used by Genetic Algorithm.
                                    type : boolean
    Returns
    -------
    fitness_score : flaot
        returns the fitness-score of the activity matrix.
        Note : No need to set/change fitness and fitness_valid attributes.
    """
    # Design the fitness function
    fitness_score = 0
    activity_mat = np.array(IndividualObject.individual, dtype="int")
    activity_mat = activity_mat[:, : activity_mat.shape[1] - 1]
    # print(activity_mat)
    
    total_sum = sum(sum(row) for row in activity_mat)
    
    # Step 2: Calculate the size of the matrix
    num_rows = len(activity_mat)
    num_columns = len(activity_mat[0])
    size_of_matrix = num_rows * num_columns

    density = total_sum / size_of_matrix
   
    transposed_matrix = [[activity_mat[j][i] for j in range(len(activity_mat))] for i in range(len(activity_mat[0]))]
    unique_columns = set(tuple(column) for column in transposed_matrix)
    Uniqueness =  len(unique_columns)

    #print("uniq", Uniqueness)

    # Use 'activity_mat' to compute fitness of it.
    # ToDo : Write your code here to compute fitness of test-suite

    def club_same_rows(matrix):
        unique_rows = {}
        
        for i, row in enumerate(matrix):
            row_tuple = tuple(row)
            
            if row_tuple in unique_rows:
                unique_rows[row_tuple].append(i)
            else:
                unique_rows[row_tuple] = [i]
        
        unique_matrices = []
        for indices in unique_rows.values():
            unique_matrix = [matrix[i] for i in indices]
            unique_matrices.append(unique_matrix)
        
        return unique_matrices
    
    def calculate_expression(unique_matrices, num_rows):
        total_sum = 0
        
        for matrix in unique_matrices:
            nk = len(matrix)
            total_sum += nk * (nk - 1)

        result = 0  
        if (num_rows * (num_rows - 1)) != 0: 
            result = total_sum / (num_rows * (num_rows - 1))
    
        return result

    
    unique_matrices = club_same_rows(activity_mat)
    num_rows = len(activity_mat)

    result = calculate_expression(unique_matrices, num_rows)
    
    diversity = 1 - result

    density = 1 - abs(1 - 2*density)

    fitness_score = density*diversity*Uniqueness

    return -1*fitness_score


# This class takes a spectrum and generates ranks of each components.
# finish implementation of this class.
class SpectrumBugs:
    def __init__(self, spectrum):
        self.spectrum = np.array(spectrum, dtype="int")
        self.comps = self.spectrum.shape[1] - 1
        self.tests = self.spectrum.shape[0]
        self.activity_mat = self.spectrum[:, : self.comps]
        self.errorVec = self.spectrum[:, -1]

    def getActivity(self, comp_index):
        """
        get activity of component 'comp_index'
        Parameters
        ----------
        comp_index : int
        """
        return self.activity_mat[:, comp_index]

    def suspiciousness(self, comp_index):
        """
        Parameters
        ----------
        comp_index : int
            component number/index of which you want to compute how suspicious
            the component is. assumption: if a program has 3 components then
            they are denoted as c0,c1,c2 i.e 0,1,2
        Returns
        -------
        sus_score : float
            suspiciousness value/score of component 'comp_index'
        """
        act_mat = self.activity_mat
        errorVec = self.errorVec

        col = [row[comp_index] for row in act_mat]

        nf = np = cf = cp = 0
    
        for ind in range(len(col)):
            if col[ind] == errorVec[ind] == 1:
                cf += 1
            elif col[ind] == errorVec[ind] == 0:
                np += 1
            elif col[ind] == 1 and errorVec[ind] == 0:
                cp += 1
            elif col[ind] == 0 and errorVec[ind] == 1:
                nf += 1
        
        ochiai = 0
        if math.sqrt((cf + nf)*(cf + cp)) != 0:
            ochiai = cf / math.sqrt((cf + nf)*(cf + cp))
        sus_score = ochiai
        
        return sus_score

    def getRankList(self):
        """
        find ranks of each components according to their suspeciousness score.

        Returns
        -------
        rankList : list
            ranList will contain data in this format:
                suppose c1,c2,c3,c4 are components and their ranks are
                1,2,3,4 then rankList will be :
                    [[c1,1],
                     [c2,2],
                     [c3,3],
                     [c4,4]]
        """
        act_mat = self.activity_mat
        comps = len(act_mat[0])
       
        rank_list_dict = {}
       
        for i in range(comps) :
            
            sus_score = self.suspiciousness(i)
            rank_list_dict['c' + str(i+1)] = sus_score
        
        rank_list_pairs = [(key, value) for key, value in rank_list_dict.items()]
        rankList = sorted(rank_list_pairs, key=lambda x: x[1])
        rankList = [[key, value] for key, value in rankList]
        rankList.reverse()
        temp = rankList 

        cnt = 0
        prev = -1
        for i in range(len(rankList)):
            
            temp[i][0] = rankList[i][0]
            
            if(prev != rankList[i][1]):
                cnt += 1
                prev = rankList[i][1]
            
            temp[i][1] = cnt

        print(temp)
        rankList = temp
        return rankList


# do not modify this function.
def computeRanks(spectrum, outfilename):
    """
    Parameters
    ----------
    spectrum : list
        spectrum
    outfilename : str
        components and their ranks.
    """
    S = SpectrumBugs(spectrum)
    rankList = S.getRankList()
    with open(outfilename, "w") as file:
        writer = csv.writer(file)
        writer.writerows(rankList)

import random
from kast import kachuaAST
import sys
from z3 import *
sys.path.insert(0, "KachuaCore/interfaces/")
from interfaces.fuzzerInterface import *
sys.path.insert(0, '../KachuaCore/')
import numpy as np

# Each input is of this type.
#class InputObject():
#    def __init__(self, data):
#        self.id = str(uuid.uuid4())
#        self.data = data
#        # Flag to check if ever picked
#        # for mutation or not.
#        self.pickedOnce = False
        
class CustomCoverageMetric(CoverageMetricBase):
    # Statements covered is used for
    # coverage information.
    def __init__(self):
        super().__init__()

    # TODO : Implement this
    def compareCoverage(self, curr_metric, total_metric):
        # must compare curr_metric and total_metric
        # True if Improved Coverage else False
        print("compareCoverage ",curr_metric,total_metric)
        new_coverage = set(curr_metric) - set(total_metric)
        return bool(new_coverage)

    # TODO : Implement this
    def updateTotalCoverage(self, curr_metric, total_metric):
        # Compute the total_metric coverage and return it (list)
        # this changes if new coverage is seen for a
        # given input.
        print("updateTotalMetric    ",curr_metric,total_metric)
        updated_total_metric = list(set(total_metric + curr_metric))
        return updated_total_metric
        

class CustomMutator(MutatorBase):
    def __init__(self):
        pass

    # TODO : Implement this
    def mutate(self, input_data, coverageInfo, irList):
        
        # Mutate the input data and return it
        # coverageInfo is of type CoverageMetricBase
        # Don't mutate coverageInfo
        # irList : List of IR Statments (Don't Modify)
        # input_data.data -> type dict() with {key : variable(str), value : int}
        # must return input_data after mutation.
                # Mutate the input data and return it
        # coverageInfo is of type CoverageMetricBase
        # Don't mutate coverageInfo
        # irList : List of IR Statments (Don't Modify)
        # input_data.data -> type dict() with {key : variable(str), value : int}
        # must return input_data after mutation.
        """input_data.data[':a']=input_data.data[':a']+np.random.rand()*100
        
        return input_data
"""

        mutated_data = input_data.data.copy()  # Create a copy of the input data to mutate
        
        for variable, value in mutated_data.items():
            # Example of bitwise mutation: Flipping a bit
            mutated_data[variable] = value ^ 1  # XOR with 1 to flip the least significant bit
        
        for variable, value in mutated_data.items():
        # Flip random 3 bits
            for _ in range(3):
                bit_position = random.randint(0, 31)  # Assuming 32-bit integer, adjust if needed
                value ^= (1 << bit_position)  # Flip the bit at bit_position
                mutated_data[variable] = value

        
        # Example of swapping mutation: Swap values of two variables
        """if len(mutated_data) >= 2:
            variables = list(mutated_data.keys())
            variable1, variable2 = random.sample(variables, 2)
            mutated_data[variable1], mutated_data[variable2] = mutated_data[variable2], mutated_data[variable1]"""
        
        # You can add more mutation techniques here
        print("Mutator")
        print(mutated_data)
        input_data.data = mutated_data 
        print("Mutator=")
        #print(input_data.data[':a'],"\n")
        return input_data

        

# Reuse code and imports from
# earlier submissions (if any).

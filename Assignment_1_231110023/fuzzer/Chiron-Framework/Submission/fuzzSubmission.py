from kast import kachuaAST
import sys
import random
from z3 import *
sys.path.insert(0, "KachuaCore/interfaces/")
from interfaces.fuzzerInterface import *
sys.path.insert(0, '../KachuaCore/')

# Each input is of this type.
#class InputObject():
#    def _init_(self, data):
#        self.id = str(uuid.uuid4())
#        self.data = data
#        # Flag to check if ever picked
#        # for mutation or not.
#        self.pickedOnce = False
        
class CustomCoverageMetric(CoverageMetricBase):
    # Statements covered is used for
    # coverage information.
    def _init_(self):
        super()._init_()

    # TODO : Implement this
    def compareCoverage(self, curr_metric, total_metric):
        # must compare curr_metric and total_metric
        # True if Improved Coverage else False
        for i in range(0,len(curr_metric)):
            if(curr_metric[i] not in total_metric):
                return True
        # True if Improved Coverage else False
        return False

    # TODO : Implement this
    def updateTotalCoverage(self, curr_metric, total_metric):
        # Compute the total_metric coverage and return it (list)
        # this changes if new coverage is seen for a
        # given input.
        total_metric = list(set(total_metric) | set(curr_metric))
        print("updated total is ::: ",total_metric)
        return total_metric

class CustomMutator(MutatorBase):
    def _init_(self):
        pass
    def mutate_add(self, input_data):
            for key in input_data.data:
                # Ensure the new value is between 1 and 200
                new_value = random.randint(1, 100)
                input_data.data[key] = new_value
            return input_data

    def mutate_subtract(self, input_data):
            for key in input_data.data:
                # Ensure the new value is between 1 and 75
                new_value = random.randint(1, 50)
                input_data.data[key] = new_value
            return input_data
    # TODO : Implement this
    def mutate(self, input_data, coverageInfo, irList):
        # Mutate the input data and return it
        # coverageInfo is of type CoverageMetricBase
        # Don't mutate coverageInfo
        # irList : List of IR Statments (Don't Modify)
        # input_data.data -> type dict() with {key : variable(str), value : int}
        # must return input_data after mutation.
        # TODO : Implement this
           
        
        random_number = random.randint(1,50)
        if(random_number<30):
            self.mutate_add(input_data)
        else:
            self.mutate_subtract(input_data)
        return input_data


# Reuse code and imports from
# earlier submissions (if any).
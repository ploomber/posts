import numpy as np 
import pandas as pd

def generate_data(seed, obs, std_dev, eligibility_threshold, treatment_effect, 
                positive_slope = True, after_cutoff = True):

    """
    This function generates spoofed data for our example. Although the running variable and target
    variables we test can be modified for specific purposes,they must be continuous.

    We generate our running variables values utilizing a uniform random variable. We then
    choose to treat if the running variable's valuesfall below the cutoff point We can change
    the sign based on the application. After this point, we choose to generate the data.

    INPUTS
    ------
    - seed: random state value included for reproducability
    - obs: integer representing number of observations
    - std_dev: constant that represents change between pre/post test values
    - treatment_effect: constant representing the base level of change

    OUTPUT
    ------
    spoofed_data: pandas dataframe containing the independent and target variables,
    as well as a binary indicator for treatment status
    """


    # initialize random state, generate data
    random_state = np.random.default_rng(seed) 
    running_variable = random_state.normal(loc = eligibility_threshold, size=obs) 

    #There are four cases:

    #Case 1: Positive Slope, Treatment Above the Cutoff 

    if (positive_slope == True) & (after_cutoff == True):
        # Apply Treatment above Cutoff
        treat = np.where(running_variable > eligibility_threshold, True, False)
        
        # Treatment Effect Discontinuity
        value_error = random_state.normal(0, std_dev, obs) + (treatment_effect * treat)
        y = running_variable + value_error

        # RETURN Pandas DF
        spoofed_data = pd.DataFrame(
            {
                "X": running_variable,
                "treatment": treat,
                "Y":y,
            }
        )
        return spoofed_data
    
    # Case 2: Positive Slope, Treatment Below Cutoff 

    elif (positive_slope == True) & (after_cutoff == False):
        # Apply Treatment above Cutoff
        treat = np.where(running_variable < eligibility_threshold, True, False)
        
        # Treatment Effect Discontinuity
        value_error = random_state.normal(0, std_dev, obs) + (treatment_effect * treat)
        y = running_variable + value_error

        # RETURN Pandas DF
        spoofed_data = pd.DataFrame(
            {
                "X": running_variable,
                "treatment": treat,
                "Y":y,
            }
        )
        return spoofed_data

    # Case 3: Negatove Slope, Treatment Above Cutoff    

    elif (positive_slope == False) & (after_cutoff == True):
        # Apply Treatment above Cutoff
        treat = np.where(running_variable > eligibility_threshold, True, False)
        
        # Treatment Effect Discontinuity
        value_error = random_state.normal(0, std_dev, obs) + (treatment_effect * treat)
        y = - running_variable + value_error

        # RETURN Pandas DF
        spoofed_data = pd.DataFrame(
            {
                "X": running_variable,
                "treatment": treat,
                "Y":y,
            }
        )
        return spoofed_data

    elif (positive_slope == False) & (after_cutoff == False):
        # Apply Treatment above Cutoff
        treat = np.where(running_variable < eligibility_threshold, True, False)
        
        # Treatment Effect Discontinuity
        value_error = random_state.normal(0, std_dev, obs) + (treatment_effect * treat)
        y = - running_variable + value_error

        # RETURN Pandas DF
        spoofed_data = pd.DataFrame(
            {
                "X": running_variable,
                "treatment": treat,
                "Y":y,
            }
        )
        return spoofed_data
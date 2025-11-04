# FBDD

A repository containing code and testing during my self-training of FBDD skills.

# FBDD.ipyb
This notebook contains three functions

 - get_descriptors
   
   This function takes a list of molecules as input and calculates the molecular descriptors for each molecule in the list
   The resulting list can be easily saved to a dataframe for input into the model function
   
 - train_fragment_model
   
   This function takes a dataframe and trains it using a neural network model.
   The output is a model and the test data as tensors
   
 - evaluate_model
   
   This function takes a model and test tensor data as input.
   The output is a dictionary of metrics.

import numpy as np


#********************************************************

def ann_flex_tester(samples,  weights, biases):
  
  predictions = [ann_flex_predictor(s, weights, biases) for s in samples] #an array of arrays
  
  return predictions

#********************************************************

def ann_flex_predictor(sample, weights, biases):
  fsig = np.vectorize(sigmoid)
  
  #do forward propogation
  raw = sample.dot(weights)
  full_raw = np.add(raw, biases)
  final_output = fsig(full_raw) #an array of values for output nodes

  return final_output

#********************************************************

def from_scratch_flex(samples, labels, hypers):
  
  input_n = samples.shape[1]
  output_n = labels.shape[1]
  
  #reset weights to initial values. Seed of 42 guarantees same random values
  np.random.seed(42)
  weights = .2*np.random.rand(input_n,output_n) - .1
  biases = np.random.rand(output_n)
  
  return ann_flex(samples, labels, weights, biases, hypers)

#********************************************************

def ann_flex(all_samples, all_labels, weights, biases, hypers={}):
  
    '''
    Can build an ANN with n input nodes and m output nodes.
    Uses sigmoid and mse.
    '''
  
    input_n = all_samples.shape[1]  #number of inputs in each sample
    output_n = all_labels.shape[1]      #number of outputs in each label

    assert weights.shape == (input_n,output_n), 'weights needs to have same shape as sample'
    assert all_samples.shape[0] >= 1, 'all_samples must represent 1 or more samples'
    assert biases.shape == (output_n,) , 'a bias weight for each output node'
    assert all_labels.shape[0] == all_samples.shape[0], 'labels must match up with samples'

    hyper_keys = [*hypers]  #fails on 2.7
    target_set = set(['epochs', 'cost-reporting', 'learning-rate'])  #might add more later
    diff_set = set(hyper_keys) - target_set
    if diff_set: print('WARNING: unrecognized hyper parameters ' + str(diff_set))

    max_epochs = hypers['epochs'] if 'epochs' in hypers else 100
    cost_reporting = hypers['cost-reporting'] if 'cost-reporting' in hypers else 100  #how often to report epoch cost
    alpha = hypers['learning-rate'] if 'learning-rate' in hypers else .05

    cost_accumulator = [0, 0]  #[count, sum] use to print out costs now and then

    for i in range(max_epochs):
        
        #Go through each sample forward and backward
        
        for j in range(len(all_samples)):
            
            #do forward propogation
            sample = np.expand_dims(all_samples[j], axis=1) #transform to match up with weight shape
            
            #print(weights.shape)
            #print(sample.shape)
            
            sample = sample.reshape((weights.shape[0],))
            
            raw = sample.dot(weights)
            full_raw = np.add(raw, biases)
            fsig = np.vectorize(sigmoid)
            zv = fsig(full_raw)
            
            #compute error
            costs = np.array([mse(a,b) for (a,b) in zip(zv, all_labels[j])])# TODO all_labels[j]? #all_labels?
            cost_accumulator[0] += 1  #use to print out
            cost_accumulator[1] += costs  #use to print out
            
            
            #back propogation
            mse_deriv_values = np.array([mse_der(a,b) for (a,b) in zip(zv, all_labels[j])])
            fsig_der = np.vectorize(sigmoid_der) #using numpy built-in mapping function
            sigmoid_deriv_values = fsig_der(full_raw)
            z_deltas = np.multiply(mse_deriv_values, sigmoid_deriv_values)
            weight_changes = [sample*z_deltas[i] for i in range(len(z_deltas))]
            wt = np.transpose(weight_changes)
            weights = np.subtract(weights, wt)
            biases = np.subtract(biases, z_deltas)
            
        #print ith cost value
        if i%cost_reporting == 0:
            average_cost = cost_accumulator[1]/cost_accumulator[0]  #really mse where n is cost_reporting epochs
            
            total_cost = np.sum(average_cost)
            
            print((i,total_cost))
            cost_accumulator = [0, 0]  #reset
    #end epoch loop
    if cost_accumulator[0]:
        average_cost = cost_accumulator[1]/cost_accumulator[0]  #really mse where n is cost_reporting epochs
        
        total_cost = np.sum(average_cost)
        
        print((max_epochs,total_cost))
    return (weights,biases)  

#********************************************************

def sigmoid(x):  
    return 1/(1+np.exp(-x))

#********************************************************

def mse(z,y):
  return (z-y)**2

#********************************************************

def mse_der(z,y):
  return z-y

#********************************************************

def sigmoid_der(x):  
    return sigmoid(x)*(1-sigmoid(x))

#********************************************************

def ann_simple(all_samples, labels, weights, bias, hypers={}):
  
  '''
  Can build an ANN with n input nodes and one output node.
  Uses sigmoid and mse.
  '''
  
  input_n = all_samples.shape[1]  #number of inputs in each sample
  
  assert weights.shape == (input_n,1), 'weights needs to have same shape as sample'
  assert all_samples.shape[0] >= 1, 'all_samples must represent 1 or more samples'
  assert bias.shape == (1,) , 'a single bias weight for output node'
  assert labels.shape[1] == 1, 'actual value for the 1 output node'
  assert labels.shape[0] == all_samples.shape[0], 'labels must match up with samples'
  
  hyper_keys = [*hypers]  #fails on 2.7
  target_set = set(['epochs', 'cost-reporting', 'learning-rate'])  #might add more later
  diff_set = set(hyper_keys) - target_set
  if diff_set: print('WARNING: unrecognized hyper parameters ' + str(diff_set))

  max_epochs = hypers['epochs'] if 'epochs' in hypers else 100
  cost_reporting = hypers['cost-reporting'] if 'cost-reporting' in hypers else 100  #how often to report epoch cost
  alpha = hypers['learning-rate'] if 'learning-rate' in hypers else .05
  
  cost_accumulator = [0, 0]  #[count, sum] use to print out costs now and then
  
  for i in range(max_epochs):

    #Go through each sample forward and backward
    for j in range(len(all_samples)):


      #do forward propogation
      sample = np.expand_dims(all_samples[j], axis=1) #transform to match up with weight shape
      XW = np.multiply(sample, weights)
      XW_sum = np.sum(XW, axis=0)
      raw_output = XW_sum + bias
      z = sigmoid(raw_output)  #what we are predicting

      #compute error
      cost = mse(z, labels[j])
      cost_accumulator[0] += 1  #use to print out
      cost_accumulator[1] += cost  #use to print out

      #back propogation
      mse_deriv_value = mse_der(z, labels[j])
      sigmoid_deriv_value = sigmoid_der(raw_output)
      z_delta = mse_deriv_value * sigmoid_deriv_value

      #update weights - notice z_delta part of each update
      for k in range(len(weights)):
        weights[k][0] -= alpha * all_samples[j][k] * z_delta
        
      #update bias
      bias -=  1.0*z_delta

    #print ith cost value
    if i%cost_reporting == 0:
      average_cost = cost_accumulator[1]/cost_accumulator[0]  #really mse where n is cost_reporting epochs
      print((i,average_cost))
      cost_accumulator = [0, 0]  #reset
  #end epoch loop
  
  if cost_accumulator[0]:
    average_cost = cost_accumulator[1]/cost_accumulator[0]  #really mse where n is cost_reporting epochs
    print((max_epochs,average_cost))
    
  return (weights,bias)  #don't lose these! They are the whole model.

#********************************************************

def from_scratch(samples, labels, hypers):
  
  input_n = samples.shape[1]
  
  #reset weights to initial values. Seed of 42 guarantees same random values
  np.random.seed(42)
  weights = np.random.rand(input_n,1)  #elasticity in action
  bias = np.random.rand(1)
  
  return ann_simple(samples, labels, weights, bias, hypers)

#********************************************************

def ann_predictor(sample, weights, bias):
  
  s2 = np.expand_dims(sample, axis=1)
  XW = np.multiply(s2, weights)
  XW_sum = np.sum(XW, axis=0)
  raw_output = XW_sum + bias
  z = sigmoid(raw_output)

  return 1 if z > .5 else 0  #.5 should probably be a parameter

#********************************************************

def ann_tester(samples, labels, weights, bias):
  weights = np.array(weights)
  bias = np.array(bias)
  
  predictions = [ann_predictor(s, weights, bias) for s in samples]
  zipped = list(zip(predictions, labels))
  
  return (zipped.count((1,1)) + zipped.count((0,0)))/len(zipped)

#********************************************************


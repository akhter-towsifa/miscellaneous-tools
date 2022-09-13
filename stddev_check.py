'''
The code below takes a root file as 'f', goes through the ttree 'event'.
It stores values from a particular branch (RdPhi_Corrected in this 
particular example) into the residual list.
The std_dev function first calculates the total number of entries or size
of the population. Next, the function calculates the average value simply.
The standard deviation is then calculated over the residual list.
'''

import ROOT, sys, os, array, math
import numpy as np

f = ROOT.TFile("../Run2022C_GEM_GPR_ZMu_RAWRECO_v1_aligned.root")
event = f.Get("analyzer/ME11Seg_Prop")

residual = []

for i in event:
  if i.muon_pt>20 and i.muon_pt<200 and i.n_ME11_segment==1 and i.has_fidcut and abs(i.RdPhi_Corrected)<2 and not (i.prop_location[0]==1 and (i.prop_location[2]==18 or i.prop_location[2]==31 or i.prop_location[2]==33)):
    residual.append(i.RdPhi_Corrected)

def std_dev(data, numerator=0):
  n = len(data)
  mean = sum(data)/n
  for i in residual:
    numerator += (i-mean)**2
  std_dev_value = np.sqrt(numerator / (n-1))
  #return np.sqrt(sum(x - mean)**2 for x in data / (n-1))
  return print("Entries: ", n, "\nMean: ", mean, "\nStandard Deviation: ", std_dev_value)

#print(residual[:10])
std_dev(residual)

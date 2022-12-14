import math
import os
import random
import re
import sys
import logging


#
# Complete the 'valuation' function below.
#
# The function is expected to v = a LONG_INTEGER.
# The function accepts following parameters:
#  1. LONG_INTEGER reqArea
#  2. LONG_INTEGER_ARRAY area
#  3. LONG_INTEGER_ARRAY price
import bisect
from collections import defaultdict
from collections import OrderedDict

## Answer formatting function
def FormatAnswer(x):
    if x < 10 ** 3:
        return 10 ** 3
    elif x > 10 ** 6:
        return 10 ** 6
    else:
        return int(round(x))

## Creat function to process Outliers, O(n) time;
def outlierRemoval(area, price):
    d = defaultdict(list)                  #area to prices; 1-to-many 
    x_total = {}                           #area to sum
    sum_x_squared = ({})                   #area to sum**2
    
    #loop over area indices to generate dicts
    for j in range(len(area)):
        d[area[j]].append(price[j])
        if area[j] not in x_total:
            x_total[area[j]] = price[j]
        else:
            x_total[area[j]] += price[j]
        if area[j] not in sum_x_squared:
            sum_x_squared[area[j]] = price[j] ** 2
        else:
            sum_x_squared[area[j]] += price[j] ** 2
            
    comparisonAreas = defaultdict(float)  #comparison areas to total price
    comparisonFreq = defaultdict(int)     #comparison areas to frequency of equivalents
    for key, v in d.items():                                                                       #loop over dict
        for i in range(len(v)):                                                                    #loop over dict entry
            if len(v) > 1:                                                                         #check if non-empty
                average = (x_total[key] - v[i]) / (len(v) - 1)                                     #calculating parameters
                sigma = ((sum_x_squared[key] - v[i] ** 2) / (len(v) - 1) - average ** 2) ** 0.5    #######################
                if not abs(v[i] - average) > 3 * sigma:                                            #apply outlier condition
                    comparisonAreas[key] += v[i]
                    comparisonFreq[key] += 1
            else:
                comparisonAreas[key] += v[i]
                comparisonFreq[key] += 1
    for key in comparisonFreq.keys():
        comparisonAreas[key] /= comparisonFreq[key]
    return comparisonAreas

def valuation(reqArea, area, price):

    comparisonAreas = outlierRemoval(area, price)                                          
    finalArea, finalPrice = [], []                                                                      
    k = OrderedDict(sorted(comparisonAreas.items()))                                           #sort filtered Areas
    for key, v in k.items():
        finalArea.append(key)
        finalPrice.append(v)

    
    if len(finalArea) == 0:                                                                     #check if empty
        return FormatAnswer(1000 * reqArea)
    elif len(finalArea) == 1:                                                                   #check if 1
        return FormatAnswer(reqArea * (finalPrice[0] / finalArea[0]))
    elif reqArea in finalArea:                                                                  #check if reqArea is represented
        j = finalArea.index(reqArea)
        return FormatAnswer(finalPrice[j])
    else:
        insertPosi = bisect.bisect_left(finalArea, reqArea)                                     #binary search
        if insertPosi == len(finalArea):                                                        #if > all, extrapolate right
            leftP, rightP = finalPrice[-2], finalPrice[-1]
            leftA, rightA = finalArea[-2], finalArea[-1]
            
            ans = rightP+ (reqArea - rightA)* ((rightP - leftP) / (rightA - leftA))
            return FormatAnswer(ans)
        elif insertPosi == 0:                                                                   #if < all, extrapolate left
            leftP, rightP = finalPrice[0], finalPrice[1]
            leftA, rightA = finalArea[0], finalArea[1]
            
            ans = leftP - (leftA - reqArea)* ((rightP - leftP) / (rightA - leftA))
            return FormatAnswer(ans)
        else:
            leftP, rightP = (finalPrice[insertPosi - 1],finalPrice[insertPosi])                 #else interpolate
            leftA, rightA = (finalArea[insertPosi - 1],finalArea[insertPosi])
            
            ans = leftP + (reqArea - leftA)* ((rightP - leftP) / (rightA - leftA))
            
            return FormatAnswer(ans)
    
            
                         
                

if __name__ == '__main__':
import pyfiglet
import numpy as np, numpy.random
import matplotlib.pyplot as plt
import pandas as pd
from rtreelib import RTree, Rect



def main():
    intro = pyfiglet.figlet_format("Index Comparison")
    print(intro)

    df1 = pd.read_csv('/input/flightAdsb.csv')
    df2 = pd.read_csv('/input/flightTelem.csv')
    df3 = pd.read_csv('/input/flightTelem2.csv')
    
    
main()

"""
Created on Mar 5, 2015

@author: brian
"""

from traits.api import BaseFloat

class LogFloat(BaseFloat):
    """
    A trait to represent a condition that needs to be represented on a log scale
    """
    
    #pass  # don't need to actually override anything
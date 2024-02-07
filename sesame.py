import numpy as np

class SesameChecker():
    """Class to perform the conformity checks to the Sesame criteria.
    """
    def __init__(self, f, hv, sigmaA, sigmaf, lw, nw):
        """ Class initializer
        Args:
          - f  = frequencies of the h/v curve
          - hv = amplitudes of the h/v curve
          - sigmaA = amplitude uncertainities of the h/v curve
          - sigmaf = uncertainty of the peak frequency
          - lw = windows length [in s]
          - nw = number of windows
        """
        self.f = np.array(f)
        self.hv = np.array(hv)
        self.sigmaA = sigmaA
        self.sigmaf = sigmaf
        self.lw = lw
        self.nw = nw
        self.f0 = f[np.argmax(self.hv)]
        self.A0 = np.max(self.hv)
        self.nc = self.lw*self.nw*self.f0
        pass
    
    def Reliability(self, explicit_criteria=False):
        """Check conditions for reliability criterium.
        If explicit_criteria is True the function outputs a list of bool (one value for each criterium).
        """
        C1 = self.f0>10/self.lw
        C2 = self.nc>200
        thr3 = 2 if self.f0>0.5 else 3
        C3 = np.all(self.sigmaA[(self.f>0.5*self.f0)&(self.f<2*self.f0)]<thr3)
        reliable = np.all([C1, C2, C3])
        statement = "" if reliable else "NOT "
        print(f'The H/V curve is {statement}reliable.')
        if explicit_criteria:
            return [C1, C2, C3]
        return reliable
    
    def Clarity(self, explicit_criteria=False):
        """Check conditions for clarity criterium.
        If explicit_criteria is True the function outputs a list of bool (one value for each criterium).
        """
        C1 = np.any(self.f[(self.f>self.f0/4)&(self.f<self.f0)&(self.hv<self.A0)])
        C2 = np.any(self.f[(self.f>self.f0)&(self.f<4*self.f0)&(self.hv<self.A0)])
        C3 = self.A0>2
        C4 = []
        for sign in [1, -1]:
            fpeak = np.max(self.A0+sign*self.sigmaA)
            C4.append(((fpeak>0.95*self.f0)&(fpeak<1.05*self.f0)))
        C4 = np.all(C4)
        if self.f0<0.2:
            epsilon = 0.25*self.f0
            theta = 3.0
        elif self.f0<0.5:
            epsilon = 0.20*self.f0
            theta = 2.5
        if self.f0<0.1:
            epsilon = 0.15*self.f0
            theta = 2.0
        if self.f0<2.0:
            epsilon = 0.10*self.f0
            theta = 1.78
        else:
            epsilon = 0.05*self.f0
            theta = 1.58
        C5 = self.sigmaf<epsilon
        C6 = self.sigmaA[np.argmax(self.hv)]<theta
        clarity = sum([C1, C2, C3, C4, C5, C6])>=5
        statement = "" if clarity else "NOT "
        print(f'The H/V curve is {statement}clear.')
        if explicit_criteria:
            return [C1, C2, C3, C4, C5, C6]
        return clarity

    def runChecks(self, explicit_criteria=False):
        """Runs the checks on both reliability and clarity.
        If explicit_criteria is True the function outputs a list of lists of bool (each value corresponds to a criterium).
        """
        R = self.Reliability(explicit_criteria)
        C = self.Clarity(explicit_criteria)
        return [R, C]
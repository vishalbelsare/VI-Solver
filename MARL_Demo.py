import time
import datetime
import numpy as np

from Domains.DummyMARL import *
from Domains.DummyMARL2 import *
from Domains.Coordination import *
from Domains.MatchingPennies import *
from Domains.Tricky import *

from Solvers.Euler import *
from Solvers.Extragradient import *
from Solvers.AcceleratedGradient import *
from Solvers.HeunEuler import *
from Solvers.AdamsBashforthEuler import *
from Solvers.CashKarp import *
from Solvers.GABE import *
from Solvers.Drift import *
from Solvers.DriftABE import *
from Solvers.DriftABE_Exact import *
from Solvers.DriftABE_BothExact import *
from Solvers.DriftABE_VIteration import *
from Solvers.DriftABE2 import *
from Solvers.DriftABE3 import *
from Solvers.DriftABE4 import *

from Solver import Solve
from Options import *
from Log import *

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

def Demo():

    #__DUMMY_MARL__##################################################

    # Define Domain
    # Domain = Coordination()
    Domain = MatchingPennies()
    # Domain = Tricky()

    # Set Method
    # Method = Euler(Domain=Domain,P=RPlusProjection())
    # Method = EG(Domain=Domain,P=RPlusProjection())
    # Method = AG(Domain=Domain,P=RPlusProjection())
    # Method = HeunEuler(Domain=Domain,P=IdentityProjection(),Delta0=1e-6)
    # Method = ABEuler(Domain=Domain,P=RPlusProjection(),Delta0=1e-5)
    # Method = CashKarp(Domain=Domain,P=RPlusProjection(),Delta0=1e-6)
    # Method = GABE(Domain=Domain,P=RPlusProjection(),Delta0=1e-5)
    # Method = Drift(Domain=Domain)
    box = np.array([0.,1.])
    epsilon = np.array([-0.01,0.01])
    # Method = DriftABE(Domain=Domain,P=BoxProjection(box[0],box[1]),Delta0=1e-5) #(1e-5)
    # Method = DriftABE_VIteration(Domain=Domain,P=EntropicProjection(),Delta0=1e-5,MaxStep=1e-2) #(1e-5)
    # Method = DriftABE2(Domain=Domain,P=EntropicProjection(),Delta0=1e-5,MaxStep=1e-2) #(1e-5)
    # Method = DriftABE3(Domain=Domain,P=EntropicProjection(),Delta0=1e-5,MaxStep=1e-2) #(1e-5)
    Method = DriftABE4(Domain=Domain,P=EntropicProjection(),Delta0=1e-6,MaxStep=1e-2) #(1e-5)
    # Method = DriftABE_Exact(Domain=Domain,P=IdentityProjection(),Delta0=1e-5)
    # Method = DriftABE_BothExact(Domain=Domain,P=IdentityProjection(),Delta0=1e-5)

    # Initialize Starting Point
    # Start = np.array([0,1])
    Start = np.array([[0.6,0.4],[0.6,0.4]])

	# Set Options
    Init = Initialization(Step=2e-3)
    # Init = Initialization(Step=-0.1)
    Term = Termination(MaxIter=100000,Tols=[(Domain.NE_L2Error,1e-4)]) #(1,000,000)
    Repo = Reporting(Requests=[Domain.NE_L2Error,'Policy','Policy Learning Rate','Projections'])
    Misc = Miscellaneous()
    Options = DescentOptions(Init,Term,Repo,Misc)

    # Print Stats
    # PrintSimStats(Domain,Method,Options)

    # Start Solver
    tic = time.time()
    MARL_Results = Solve(Start,Method,Domain,Options)
    toc = time.time() - tic

    # Print Results
    PrintSimResults(Options,MARL_Results,Method,toc)

    Data = np.array(MARL_Results.PermStorage['Policy'])[:,:,0] # Just take probabilities for first action
    print('Endpoint:')
    print(Data[-1])

    fig, ax = plt.subplots(1,1)

    # Choose a color map, loop through the colors, and assign them to the color 
    # cycle. You need NPOINTS-1 colors, because you'll plot that many lines 
    # between pairs. In other words, your line is not cyclic, so there's 
    # no line from end to beginning
    # cm = plt.get_cmap('winter')
    # ax.set_color_cycle([cm(1.*i/(Data.shape[0]-1)) for i in xrange(Data.shape[0]-1)])
    # for i in xrange(Data.shape[0]-1):
    #     ax.plot(Data[i:i+2,0],Data[i:i+2,1])

    ax.plot(Data[:,0],Data[:,1])
    ax.set_xlim(box+epsilon);
    ax.set_ylim(box+epsilon);
    plt.show()

if __name__ == '__main__':
  Demo()







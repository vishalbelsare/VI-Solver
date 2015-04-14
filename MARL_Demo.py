import time
from optparse import OptionParser

# from Domains.DummyMARL import *
# from Domains.DummyMARL2 import *

from VISolver.Solvers.Solver import solve
from Domains.MatchingPennies import MatchingPennies
from Domains.Tricky import Tricky
from Domains.PrisonersDilemma import PrisonersDilemma
from Domains.PureStrategyTest import PureStrategyTest
from Domains.BattleOfTheSexes import BattleOfTheSexes

from Domains.BloodBank import BloodBank, CreateRandomNetwork

from Solvers.MARL_prior.WPL import *
from Solvers.MARL_prior.WoLFIGA import *
from Solvers.MARL_prior.AWESOME import *
from Solvers.MARL_prior.PGA_APP import *
from Solvers.MultiAgentVI import MultiAgentVI
from Solvers.BoostedWPL import BoostedWPL

from Options import (
    DescentOptions, Miscellaneous, Reporting, Termination, Initialization)
from VISolver.Log import print_sim_results

from Utilities import *


def demo(domain, method, iterations=500):
    # __DUMMY_MARL__##################################################

    # Set Method
    # box = np.array(Domain.reward_range)
    box = np.array([np.vstack((domain.r_reward, domain.c_reward)).min(),
                    np.vstack((domain.r_reward, domain.c_reward)).max()])
    epsilon = np.array([-0.01, 0.01])

    # Initialize Starting Point
    # Start = np.array([0,1])
    start_strategies = np.random.random((domain.players, domain.dim))
    for i in range(start_strategies.shape[0]):
        start_strategies[i] /= np.sum(start_strategies[i])
    # start_strategies = np.array([[.8, .2], [.1, .9]])

    # Set Options
    initialization_conditions = Initialization(step=1e-4)
    # init = Initialization(Step=-0.1)
    terminal_conditions = Termination(max_iter=iterations, tols=[(domain.ne_l2error, 1e-3)])
    reporting_options = method.reporting_options()
    whatever_this_does = Miscellaneous()
    options = DescentOptions(initialization_conditions, terminal_conditions, reporting_options, whatever_this_does)

    # Print Stats
    # print_sim_stats(domain,Method,Options)

    # Start Solver
    tic = time.time()
    # set random seed
    # np.random.seed(0)
    marl_results = solve(start_strategies, method, domain, options)
    toc = time.time() - tic

    # Print Results
    if config.debug_output_level != -1:
        print_sim_results(options, marl_results, method, toc)

    # creating plots, if desired:
    if config.show_plots:
        policy = np.array(marl_results.perm_storage['Policy'])[:, :, 0]  # Just take probabilities for first action
        if 'Forecaster Policies' in marl_results.perm_storage:
            forecaster = np.array(marl_results.perm_storage['Forecaster Policies'])[:, :, :, 0]  # Just take probabilities for first action
        # policy_est = np.array(marl_results.perm_storage['Policy Estimates'])
        val_fun = np.array(marl_results.perm_storage['Value Function'])[-1]
        true_val_fun = np.array(marl_results.perm_storage['True Value Function'])
        # val_var = np.array(marl_results.perm_storage['Value Variance'])
        pol_grad = np.array([[marl_results.perm_storage['Policy Gradient (dPi)'][i][0, 0],
                              marl_results.perm_storage['Policy Gradient (dPi)'][i][1, 0]]
                             for i in range(1, len(marl_results.perm_storage['Policy Gradient (dPi)']))])
        pol_lr = np.array(marl_results.perm_storage['Policy Learning Rate'])
        reward = np.array(marl_results.perm_storage['Reward'])
        action = np.array(marl_results.perm_storage['Action'])
        # value_function_values = np.array(MARL_Results.perm_storage['Value Function'])[:, :, 0]
        print('Ratio of games won:')
        win_ratio = np.mean(.5 + .5*reward, axis=0).round(2)
        print 'Player 1:', win_ratio[0], 'Player 2:', win_ratio[1]
        print('Endpoint:')
        print(policy[-1])
        pol_grad = np.vstack(([0., 0.], pol_grad))
        print 'pol1, pol2, action1, action2, reward1, reward2, polgrad1, polgrad2'
        # for i in np.hstack((np.round(policy, 2), action, reward, np.round(pol_grad, 2))):
        #     print i

        # ax[0, 1].plot(policy[:, 0], policy[:, 1])
        # ax[0, 1].set_xlim(box + epsilon)
        # ax[0, 1].set_ylim(box + epsilon)
        # ax[0, 1].set_title('The policy-policy space')
        # ax[0, 1].grid(True)

        printing_data = {}
        # printing_data['The value function'] = {'values': val_fun.T, 'smooth':-1}
        printing_data['Analytic Value of policies played'] = {'values': true_val_fun, 'yLimits': box, 'smooth': 1}
        printing_data['The policies'] = {'values': policy, 'yLimits': np.array([0, 1]) + epsilon, 'smooth': -1}
        if 'Forecaster Policies' in marl_results.perm_storage:
            printing_data['Forecaster - P1'] = {'values': forecaster[:, 0, :], 'yLimits': np.array([0, 1]) + epsilon, 'smooth': -1}
            printing_data['Forecaster - P2'] = {'values': forecaster[:, 1, :], 'yLimits': np.array([0, 1]) + epsilon, 'smooth': -1}
        # printing_data['The policy gradient'] = {'values': pol_grad}
        # printing_data['Policy Estimates'] = {'values': policy_est, 'yLimits': box}
        plot_results(printing_data)
    reward = np.array(marl_results.perm_storage['Reward'])
    win_ratio = np.mean(.5 + .5*reward, axis=0).round(2)
    return win_ratio


def wrapper():
    # Define Domain
    # domain = MatchingPennies()
    domain = PureStrategyTest()
    # domain = BattleOfTheSexes('traditional')
    # domain = BattleOfTheSexes('new')
    # domain = Tricky()
    # domain = PrisonersDilemma()
    # Network = CreateRandomNetwork(nC=2,nB=2,nD=2,nR=2,seed=0)
    # domain = BloodBank(Network=Network,alpha=2)

    # method = IGA(domain, P=BoxProjection())
    # method = WoLFIGA(domain, P=BoxProjection(), min_step=1e-4, max_step=1e-3 )
    # method = MySolver(domain, P=BoxProjection())
    # method = MyIGA(domain, P=BoxProjection())
    # method = MyIGA(domain, P=LinearProjection())
    # method = WPL(domain, P=LinearProjection(low=.001))
    method1 = WPL(domain, P=BoxProjection(low=.001))
    # method = AWESOME(domain, P=LinearProjection())
    # method = PGA_APP(domain, P=LinearProjection())
    # method = MultiAgentVI(domain, P=LinearProjection())
    method2 = BoostedWPL(domain, P=LinearProjection())
    results1 = []
    results2 = []
    iterations = 100
    for i in range(20):
        results1.append(demo(domain, method1, iterations))
        results2.append(demo(domain, method2, iterations))

    print 'first method'
    print 'max values', np.array(results1).max(axis=0)
    print 'min values', np.array(results1).min(axis=0)
    print 'averages', np.mean(results1, axis=0)
    print 'median', np.median(results1, axis=0)
    print 'second method'
    print 'max values', np.array(results2).max(axis=0)
    print 'min values', np.array(results2).min(axis=0)
    print 'averages', np.mean(results2, axis=0)
    print 'median', np.median(results2, axis=0)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-p', '--suppress-plots', action='store_false', dest='plot', default=True, help='suppress plots')
    parser.add_option('-v', '--show-output', type='int', dest='debug', default=0, help='debug level')
    (options, args) = parser.parse_args()
    config.debug_output_level = options.debug
    config.show_plots = options.plot
    # domain = PureStrategyTest()
    domain = MatchingPennies()
    # domain = Tricky()
    method2 = BoostedWPL(domain, P=LinearProjection())
    # method2 = WPL(domain, P=LinearProjection())

    demo(domain, method2, 6000)

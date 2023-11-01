import numpy as np
import networkx as nx
from dm_data import dm_instance
from helper import blossom_separation
from helper import birkhoff_von_neumann_decomposition
from numpy.random import RandomState
import copy
from affine_model import affine_model
from alp_cg import alp_cg
from myopic import myopic_model
from limited_lookahead import limited_lookahead_model
from ow_lp import ow_lp
from deterministic_lp import deterministic_lp
from time import time
    
'''
    simulator class for running experiments
'''

TIME_LIMIT = 600

class simulator:
    def __init__(self, a_dminstance, L):
        self.DM = copy.deepcopy(a_dminstance)
        self.L = L
        self.results = {}
        self.seed = None


    def get_alp_ub(self):
        t = time()
        alp = affine_model(self.DM, self.L)
        alp.optimize()
        alp_ub = alp.r_alp.objVal
        self.results['alp_ub'] = alp_ub

    def get_cg_ub(self, verbose=0):
        t = time()
        cg = alp_cg(self.DM, self.L)
        cg_ub = cg.solve_integer(verbose)
        self.results['cg_ub'] = cg_ub

    def get_dlp_ub(self):
        dlp = deterministic_lp(self.DM, self.L)
        t = time()
        dlp_ub = dlp.multi_dlp()
        self.results['dlp_ub'] = dlp_ub

    def sim_alp_dual(self, N, seed=0):
        # latest and greatest prop 3
        lbs = []
        num_of_cg_cuts_list = []
        for i in range(N):
            t0 = time()
            lb = 0
            alp = affine_model(self.DM, self.L, seed=i+seed)
            alp.DM.rg = RandomState(i+seed)
            while(len(alp.DM.Horizon)>0):
                if time() - t0 > TIME_LIMIT:
                    lb = -1
                    break
                if self.L == 2:
                    reward, num_of_cg_cuts = alp.prob_solve()
                    lb += reward
                    num_of_cg_cuts_list.append(num_of_cg_cuts)
                else:
                    lb += alp.solve()
                alp.DM.generate_arrival_departure()
            lbs.append(lb)
        self.results['alp_dual_lb'] = sum(lbs)/N



    def sim_alp_primal(self, N, seed=0):
        lbs = []
        for i in range(N):
            t0 = time()
            lb = 0
            alp = affine_model(self.DM, self.L, seed=i+seed)
            alp.DM.rg = RandomState(i+seed)
            while(len(alp.DM.Horizon)>0):
                if time() - t0 > TIME_LIMIT:
                    lb = -1
                    break
                lb += alp.one_step_greedy()
                alp.DM.generate_arrival_departure()
            lbs.append(lb)
        self.results['alp_primal_lb'] = sum(lbs)/N


    def sim_alp_primal_no_re(self, N, seed=0):
        lbs = []
        for i in range(N):
            t0 = time()
            lb = 0
            alp = affine_model(self.DM, self.L, seed=i+seed)
            alp.get_all_V()
            alp.DM.rg = RandomState(i+seed)
            for t in self.DM.Horizon:
                if time() - t0 > TIME_LIMIT:
                    lb = -1
                    break
                lb += alp.dual_no_resolve(t)
                alp.DM.generate_arrival_departure()
            lbs.append(lb)
        self.results['alp_primal_lb_no_re'] = sum(lbs)/N

    def sim_myopic(self, N, seed=0):
        lbs = []
        for i in range(N):
            t0 = time()
            lb = 0
            myopic_lp = myopic_model(self.DM, self.L, seed=i+seed)
            myopic_lp.DM.rg = RandomState(i+seed)
            while(len(myopic_lp.DM.Horizon)>0):
                if time() - t0 > TIME_LIMIT:
                    lb = -1
                    break
                lb += myopic_lp.myopic_decision()
                myopic_lp.DM.generate_arrival_departure()
            lbs.append(lb)
        self.results['alp_primal_lb_no_re'] = sum(lbs)/N


    def sim_limited_lookahead(self, N, seed=0):
        if 'alp_ub' not in self.results:
            self.get_alp_ub()
        lbs = []
        for i in range(N):
            t0 = time()
            lb = 0
            lla = limited_lookahead_model(self.DM, self.L, seed=i+seed)
            lla.DM.rg = RandomState(i+seed)
            while(len(lla.DM.Horizon)>0):
                if time() - t0 > TIME_LIMIT:
                    lb = -1
                    break
                lb += lla.limited_lookahead_decision()
                lla.DM.generate_arrival_departure()
            lbs.append(lb)
        self.results['lla_lb'] = sum(lbs)/N

    def sim_dlp(self, N, seed=0):
        lbs = []
        for i in range(N):
            t0 = time()
            lb = 0
            dlp = deterministic_lp(self.DM, self.L)
            dlp.DM.rg = RandomState(i+seed)
            while(len(dlp.DM.Horizon)>0):
                if time() - t0 > TIME_LIMIT:
                    lb = -1
                    break
                lb += dlp.multi_dlp_solve()
                dlp.DM.generate_arrival_departure()
            lbs.append(lb)
        self.results['dlp_lb'] = sum(lbs)/N


    def sim_ow_lp(self, N, ow_instance, seed=0):
        lbs = []
        olp = ow_lp(ow_instance)
        olp.get_x()
        self.results['olp_ub'] = [olp.upper_bound]
        for i in range(N):
            t0 = time()
            lb = 0
            olp_i = copy.deepcopy(olp)
            olp_i.dm_instance.rg = RandomState(i+seed)
            while(len(olp_i.dm_instance.Horizon)>0):
                if time() - t0 > TIME_LIMIT:
                    lb = -1
                    break
                lb += olp_i.randomized_lp_decision()
                olp_i.dm_instance.generate_arrival_departure()
            lbs.append(lb)
        self.results['olp_lb'] = sum(lbs)/N


    def run(self, N):
        self.get_alp_ub()
        self.get_dlp_ub()
        self.sim_alp_dual(N)
        self.sim_alp_primal(N)
        self.sim_alp_primal_no_re(N)
        self.sim_limited_lookahead(N)
        self.sim_dlp(N)
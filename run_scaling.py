import numpy as np
import os

from multiarea_model import MultiAreaModel
from start_jobs import start_job
from config import submit_cmd, jobscript_template
from config import base_path
from figures.Schmidt2018_dyn.network_simulations import NEW_SIM_PARAMS


network_params, sim_params = NEW_SIM_PARAMS['Fig5'][0]

network_params['connection_params']['K_stable'] = os.path.join(
    base_path, 'figures/SchueckerSchmidt2017/K_prime_original.npy'
)

theory_params = {'dt': 0.1}

total_num_vp_per_node = 24
t_presim = 10.
t_sim = 10000.
NEST_DIR = ['/p/project/cjinb33/albers2/nest_jasperalbers/nest-simulator/3_0_buffer_apr16_cc4cf8a/install/bin/nest_vars.sh']

for nest_dir in NEST_DIR:
    for mpi_proc_per_node in [1,2,12,24]:
        for num_nodes in [30,60]:#[20, 28, 44, 76, 92, 108, 124, 156, 172, 188]:#[20,100,140]:
            for master_seed in [75]:#, 17]:#, 666]:
                local_num_threads = int(total_num_vp_per_node / mpi_proc_per_node)
                num_processes = (num_nodes * mpi_proc_per_node)

                sim_params.update(
                        {
                            't_presim': t_presim,
                            't_sim': t_sim,
                            'num_processes': num_processes,
                            'num_nodes': num_nodes,
		            'local_num_threads': local_num_threads,
                            'master_seed': master_seed,
                            'nest_dir': nest_dir
                            }
                        )

                M = MultiAreaModel(network_params, simulation=True,
                                   sim_spec=sim_params,
                                   theory=True,
                                   theory_spec=theory_params)

                p, r = M.theory.integrate_siegert()

                print("Mean-field theory predicts an average "
                      "rate of {0:.3f} spikes/s across all populations.".format(np.mean(r[:, -1])))

                start_job(M.simulation.label, submit_cmd, jobscript_template)

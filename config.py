# Absolut path of repository
base_path = '/p/project/cjinb33/albers2/projects/mam_benchmarking/2_20/multi-area-model'

# Place to store simulations
data_path = '/p/scratch/cjinb33/albers2/mam_benchmarks/2_20/fig5_params_kernel_status'

# Template for jobscripts
jobscript_template = """#!/bin/bash -x
#SBATCH --job-name MAM_buffer
#SBATCH -o {sim_dir}/{label}.%j.o
#SBATCH -e {sim_dir}/{label}.%j.e
#SBATCH --mem=120G
#SBATCH --time=02:00:00
#SBATCH --exclusive
#SBATCH --cpus-per-task={local_num_threads}
#SBATCH --ntasks={num_processes}
#SBATCH --nodes={num_nodes}
#SBATCH --mail-type=END,FAIL # notifications for job done & fail
#SBATCH --mail-user=j.albers@fz-juelich.de
#SBATCH --account jinb33

module purge
module load GCC CMake ParaStationMPI Python SciPy-Stack GSL jemalloc
source {nest_dir}

export KMP_AFFINITY=scatter,verbose
#export LD_PRELOAD=/p/project/cjinb33/jinb3330/jemalloc/lib/libjemalloc.so

srun python -u {base_path}/run_simulation.py {label} {network_label}"""

# Command to submit jobs on the local cluster
submit_cmd = 'sbatch' 

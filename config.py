# Absolut path of repository
base_path = '/p/project/cjinb33/albers2/projects/mam_benchmarking/3_0/multi-area-model'

# Place to store simulations
data_path = '/p/scratch/cjinb33/albers2/mam_benchmarks/3_0_buffer_apr16'

# Template for jobscripts
jobscript_template = """#!/bin/bash -x
#SBATCH --job-name buffer
#SBATCH -o {sim_dir}/{label}.%j.o
#SBATCH -e {sim_dir}/{label}.%j.e
#SBATCH --time=01:00:00
#######SBATCH --contiguous
#SBATCH --exclusive
#SBATCH --cpus-per-task={local_num_threads}
#SBATCH --ntasks={num_processes}
#SBATCH --nodes={num_nodes}
#SBATCH --mail-type=END,FAIL # notifications for job done & fail
#SBATCH --mail-user=j.albers@fz-juelich.de
#SBATCH --account jinb33

#module purge
#module load GCC CMake ParaStationMPI Python SciPy-Stack GSL Boost/1.69.0-Python-3.6.8

module use Stages/2019a
ml Intel/2019.5.281-GCC-8.3.0
ml ParaStationMPI/5.4.4-1-mt
ml GSL/2.5
ml Python SciPy-Stack
ml Boost/1.68.0-Python-3.6.8
ml CMake
ml jemalloc

source {nest_dir}
export __PSI_NO_PINPROC

srun --cpu_bind=sockets python -u {base_path}/run_simulation.py {label} {network_label}"""

# Command to submit jobs on the local cluster
submit_cmd = 'sbatch' 

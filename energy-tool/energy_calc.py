"""Estimates energy by perf measurements and processor model"""
import os
import sys
import subprocess
import logging
import shutil


# types of stats to be collected from perf
stat_types = [
              'cache-references',
              'cache-misses',
              'cycles',
              'instructions',
              'branches',
              'faults',
              'migrations',
              'r530110', # traditional 8087 style 80bit floating point operations
              'r531010', # SSE double-precision on packed data (128 bit registers, so this is two operations)
              'r532010', # one single-precision operation
              'r534010', # four single-precision operation (32bit single precision packed into 128 bit register)
              'r538010', # one double-precision operation
             ]


# constants for energy estimation
# energy units are in PJ 
Xeon_IPC = 3
cacheline_size_bits = 64 * 8
energy_per_inst = 1000
energy_per_fp = 3.7
energy_per_cache_access = 100
DDR4_energy_per_bit = 60


# prints usage
def print_usage():
    print("Usage options:")
    print("1) If testing ordinary executable:\n \
            python3 energy_calc.py <executable>")
    print("2) If testing Python program:\n \
            python3 energy_calc.py python3 <program.py>")


# collects perf outputs into a dictionary
def process_perf_output(output_str):
    perf_data = {}
    for line in output_str.splitlines():
        line = line.split()
        for stat in stat_types:
            if stat in line:
                stat_index = line.index(stat)
                try:
                    perf_data[stat] = int(line[stat_index - 1].replace(',', ''))
                except ValueError:
                    logging.info("Could not collect %s stats" % stat)
                    perf_data[stat] = 0
    return perf_data


# executes perf to find performance stats
def execute_perf(exec_cmd):
    if isinstance(exec_cmd, str):
        exec_cmd = [exec_cmd]
    perf_cmd = ['sudo', 'perf', 'stat', '-B'] + ["-e " + stat for stat in stat_types] +  exec_cmd
    perf_proc = subprocess.Popen(perf_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (perf_out, _) = perf_proc.communicate()
    return process_perf_output(perf_out.decode("utf8"))


# processes performance stats to estimate energy in picojoules
def calculate_energy_cpu(perf_data):
    energy = 0
    # due to general instructions
    energy += perf_data['cycles'] * Xeon_IPC * energy_per_inst
    # due to floating point instructions
    float_insts = perf_data['r530110'] + perf_data['r531010'] * 2 + perf_data['r532010'] + perf_data['r534010'] * 4 + perf_data['r538010']
    energy += float_insts * energy_per_fp
    # due to cache accesses
    energy += perf_data['cache-references'] * energy_per_cache_access
    # due to DDR4 accesses
    energy += perf_data['cache-misses'] * DDR4_energy_per_bit * cacheline_size_bits
    return energy


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    if shutil.which('perf') is None:
        logging.error("perf not found, please install and try again")
        sys.exit()
    if len(sys.argv) == 1:
        print_usage()
        sys.exit()
    perf_data = execute_perf(sys.argv[1:])
    print("%s microjoules" % str(calculate_energy_cpu(perf_data) / 10**6))

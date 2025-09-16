import time

import numpy as np

from pathlib import Path

import parser_short_long

import rust_bindings
from prob_fast import calculate_confidence_scores

from output_adapters import *

from data_generator import float_to_string_without_point
from data_generator import simulate_references_queries

from fasta_editor import mutate_fasta

import parser_short_short

def main():
    """
    print(len(queries_paths), len(reference_paths))

    for i in range(21, 25, 1):

        reference_path = Path("./example_short_long/mutation_rate_boundary/references_s1000_t1.fasta")
        query_path = Path("./example_short_long/mutation_rate_boundary/queries_200_error" + str(i) + ".fasta")

        print(time.perf_counter())

        #results_control, reference_sizes_control, names_control = rust_bindings.parse_input1(reference_path_str, queries_path_str, False)
        #res1, reference_sizes_control, nam1 = rust_bindings.parse_input1(reference_path_str, queries_path_str_control, True)

        #results, reference_sizes, names = rust_bindings.parse_input1(reference_path_str, queries_path_str, True)

        #results, names = parser_short_short.get_intersection_sizes(Path(reference_path_str), Path(queries_path_str), False)

        #results, names = parser_short_long.get_intersection_sizes(Path(reference_path_str), Path(queries_path_str), 205)

        results, names, runtime_info = parser_short_long.get_intersection_sizes(reference_path, query_path, True)

        print(time.perf_counter())

        base_dir = reference_path.parent
        ref_name = reference_path.stem
        query_name = query_path.stem
        output_dir_name = f"results_{ref_name}_{query_name}"

        result_dir = base_dir / output_dir_name

        #output_sim_miseq(results, names, runtime_info, result_dir)
        output_s_t(results, names, runtime_info, result_dir)

        print(time.perf_counter())"""

    """
    tree_heights = [0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19]
    seed_nums = [941, 303, 37, 932, 855, 461, 150, 285, 613, 235]


    for i in range(10):
        tree_height = tree_heights[i]
        seed_num = seed_nums[i]
        print(tree_height)

        path = Path(f"./example_short_long/tree_height_boundary/t{float_to_string_without_point(tree_height)}")

        simulate_references_queries(path, 1000, 50000, tree_height, 200, seed_num)

        reference_path = path / "references.fasta"
        query_path = path / "queries_200.fasta"

        start_time = time.perf_counter()

        results, names, runtime_info = parser_short_long.get_intersection_sizes(reference_path, query_path, True)

        print(time.perf_counter())

        base_dir = reference_path.parent
        ref_name = reference_path.stem
        query_name = query_path.stem
        output_dir_name = f"results_{ref_name}_{query_name}"

        result_dir = base_dir / output_dir_name

        # output_sim_miseq(results, names, runtime_info, result_dir)

        end_time = time.perf_counter()
        total_execution_time = end_time - start_time
        output_s_t(results, names, runtime_info, result_dir, total_execution_time)
    """

    """
    mutation_rates = [0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22]
    seed_nums = [941, 303, 37, 932, 855, 461, 150, 285, 613, 235]

    for i in range(10):
        mutation_rate = mutation_rates[i]
        seed_num = seed_nums[i]

        print(mutation_rate)

        path = Path(f"example_short_long/mutation_rate/mutation_rate_boundary/m{int(100 * mutation_rate)}")

        simulate_references_queries(path, 1000, 50000, 1, 200, seed_num)

        reference_path = path / "references.fasta"
        query_path = path / "queries_200.fasta"
        query_mutate_path = path / f"queries_200_error{int (100 * mutation_rate)}.fasta"

        mutate_fasta(query_path, query_mutate_path, mutation_rate)

        start_time = time.perf_counter()

        results, names, runtime_info = parser_short_long.get_intersection_sizes(reference_path, query_mutate_path, True)

        print(time.perf_counter())

        base_dir = reference_path.parent
        ref_name = reference_path.stem
        query_name = query_mutate_path.stem
        output_dir_name = f"results_{ref_name}_{query_name}"

        result_dir = base_dir / output_dir_name

        # output_sim_miseq(results, names, runtime_info, result_dir)

        end_time = time.perf_counter()
        total_execution_time = end_time - start_time
        output_s_t(results, names, runtime_info, result_dir, total_execution_time)
    """

    tree_height = 0.1

    path = Path(f"./experiments/random_testing/test_parallel3")

    simulate_references_queries(path, 1000, 50000, tree_height, 200, -1)

    start_time = time.perf_counter()

    reference_path = path / "references.fasta"
    query_path = path / "queries_200.fasta"

    results, names, runtime_info = parser_short_long.get_intersection_sizes_parallel(reference_path, query_path, True)

    base_dir = reference_path.parent
    ref_name = reference_path.stem
    query_name = query_path.stem
    output_dir_name = f"results_{ref_name}_{query_name}"

    result_dir = base_dir / output_dir_name

    end_time = time.perf_counter()
    total_execution_time = end_time - start_time
    output_s_t(results, names, runtime_info, result_dir, total_execution_time)

if __name__ == "__main__":

    """
    T789 1093
    [41, 39, 33, 33, 33, 39, 36, 36, 34, 38, 40, 35, 36, 29, 33, 33, 34, 37, 33, 36, 38, 33, 32, 34, 36, 31, 39, 36, 30, 41, 35, 33, 33, 40, 39, 37, 43, 39, 39, 34, 29, 32, 30, 33, 31, 33, 39, 38, 35, 36, 37, 32, 34, 35, 37, 35, 43, 35, 41, 37, 35, 43, 42, 41, 34, 35, 34, 41, 40, 39, 37, 35, 36, 35, 44, 37, 41, 38, 36, 34, 35, 31, 37, 35, 34, 34, 34, 35, 41, 33, 33, 37, 36, 36, 39, 32, 35, 37, 34, 40, 41, 34, 34, 38, 34, 32, 36, 37, 39, 41, 37, 33, 35, 38, 35, 35, 36, 32, 38, 35, 35, 51, 33, 31, 38, 35, 31, 43, 40, 38, 30, 40, 40, 34, 34, 33, 43, 39, 35, 34, 36, 36, 37, 37, 36, 30, 36, 33, 40, 34, 34, 40, 32, 35, 37, 34, 40, 40, 37, 36, 39, 31, 39, 38, 39, 36, 36, 34, 37, 34, 33, 36, 37, 38, 33, 33, 36, 39, 35, 40, 34, 33, 36, 41, 34, 39, 35, 38, 36, 36, 37, 41, 40, 33, 34, 38, 37, 32, 37, 40, 40, 36, 37, 31, 31, 34, 37, 44, 38, 32, 36, 36, 36, 34, 34, 38, 32, 33, 46, 36, 36, 40, 46, 33, 38, 37, 37, 33, 39, 32, 32, 38, 39, 34, 37, 37, 38, 29, 32, 33, 34, 35, 39, 44, 29, 33, 30, 30, 34, 33, 34, 34, 34, 32, 41, 42, 36, 35, 35, 41, 36, 41, 32, 31, 33, 32, 33, 33, 35, 34, 41, 42, 37, 33, 37, 31, 32, 30, 35, 38, 34, 43, 38, 37, 31, 31, 36, 34, 36, 38, 36, 33, 30, 34, 33, 38, 38, 37, 38, 39, 35, 41, 36, 45, 41, 34, 35, 30, 37, 41, 32, 43, 36, 34, 37, 34, 38, 39, 34, 35, 47, 34, 33, 35, 39, 36, 35, 37, 32, 28, 37, 40, 28, 33, 31, 42, 40, 33, 34, 33, 36, 36, 39, 35, 32, 34, 37, 35, 34, 36, 32, 32, 45, 40, 34, 34, 36, 37, 38, 34, 36, 29, 33, 33, 43, 35, 33, 33, 34, 37, 33, 37, 39, 38, 32, 35, 38, 34, 33, 37, 40, 34, 36, 35, 34, 35, 35, 40, 35, 39, 35, 41, 36, 46, 37, 34, 34, 36, 32, 34, 35, 36, 33, 36, 34, 34, 34, 38, 35, 35, 32, 34, 34, 35, 38, 35, 32, 38, 34, 36, 33, 34, 39, 34, 39, 36, 35, 36, 32, 34, 34, 32, 36, 35, 32, 35, 35, 35, 35, 41, 37, 32, 33, 36, 244, 990, 130, 34, 35, 45, 40, 41, 35, 33, 33, 28, 30, 34, 35, 34, 34, 36, 32, 31, 43, 34, 44, 35, 34, 42, 35, 35, 35, 35, 34, 38, 40, 32, 35, 33, 37, 36, 38, 40, 38, 36, 41, 31, 41, 43, 40, 34, 38, 30, 35, 37, 33, 37, 40, 32, 36, 37, 34, 34, 30, 31, 40, 32, 32, 36, 39, 32, 42, 35, 39, 34, 32, 32, 32, 32, 36, 38, 39, 34, 35, 36, 40, 32, 35, 41, 32, 36, 35, 35, 38, 35, 38, 38, 36, 34, 31, 33, 41, 33, 40, 35, 35, 36, 34, 32, 36, 39, 38, 37, 31, 36, 36, 35, 33, 34, 32, 35, 37, 34, 43, 37, 40, 35, 37, 34, 34, 34, 34, 34, 34, 37, 33, 34, 37, 33, 32, 34, 37, 35, 36, 34, 38, 36, 35, 43, 33, 37, 44, 32, 29, 32, 39, 31, 39, 32, 37, 44, 36, 41, 37, 35, 37, 35, 35, 40, 36, 43, 35, 35, 35, 35, 40, 32, 33, 37, 34, 37, 41, 40, 34, 37, 33, 45, 37, 33, 34, 31, 34, 33, 37, 33, 34, 35, 30, 33, 36, 36, 35, 29, 44, 31, 39, 39, 36, 32, 43, 39, 37, 44, 40, 41, 40, 36, 36, 34, 34, 35, 35, 43, 39, 39, 36, 36, 36, 34, 40, 37, 43, 37, 37, 32, 36, 39, 36, 35, 37, 40, 36, 30, 39, 44, 37, 37, 35, 41, 32, 33, 34, 32, 36, 29, 33, 39, 35, 31, 33, 45, 33, 33, 32, 38, 36, 31, 41, 36, 36, 35, 42, 39, 36, 35, 36, 29, 36, 38, 31, 34, 34, 36, 41, 36, 38, 37, 35, 32, 39, 34, 37, 34, 37, 31, 33, 34, 32, 36, 35, 33, 43, 37, 36, 34, 35, 32, 38, 37, 37, 33, 35, 34, 35, 37, 32, 36, 36, 34, 36, 36, 37, 41, 34, 36, 34, 35, 36, 39, 32, 36, 39, 35, 33, 32, 36, 32, 33, 34, 33, 32, 38, 38, 40, 32, 34, 35, 39, 41, 34, 36, 40, 39, 35, 39, 39, 34, 32, 41, 41, 39, 35, 37, 31, 32, 39, 36, 36, 36, 34, 34, 35, 33, 37, 35, 39, 40, 33, 35, 35, 36, 32, 36, 33, 37, 36, 35, 39, 35, 31, 32, 35, 32, 37, 33, 37, 36, 33, 37, 32, 32, 34, 37, 34, 36, 38, 35, 34, 41, 33, 39, 39, 41, 39, 37, 41, 39, 31, 36, 30, 34, 33, 36, 36, 33, 32, 32, 36, 35, 36, 37, 38, 35, 38, 33, 37, 38, 34, 34, 35, 34, 37, 36, 35, 38, 40, 36, 38, 35, 36, 43, 36, 41, 38, 39, 36, 33, 36, 37, 36, 36, 33, 33, 33, 41, 38, 41, 31, 33, 37, 38, 33, 39, 40, 32, 41, 35, 42, 29, 34, 35, 30, 33, 39, 39, 36, 41, 39, 34, 35, 34, 36, 33, 37, 37, 32, 38, 35, 37, 35, 36, 34, 37, 37, 33, 36, 36, 40, 40, 32, 32, 40, 37, 35, 32, 38, 34, 33, 33, 32, 34, 36, 33, 35, 32, 31, 37, 37, 35, 39, 42, 32, 46, 31, 36, 35, 35, 32, 35, 38, 37, 37, 30, 39, 36, 33, 34, 37, 36, 38, 36, 38, 38, 38, 37, 32, 34, 36, 32]
    
    T488 284
    [9, 11, 8, 7, 7, 8, 7, 14, 7, 5, 7, 8, 7, 8, 8, 10, 9, 9, 8, 7, 8, 7, 7, 9, 7, 7, 8, 10, 6, 7, 6, 7, 8, 9, 9, 8, 6, 8, 8, 8, 6, 6, 10, 11, 7, 8, 8, 8, 8, 6, 6, 8, 10, 7, 8, 9, 9, 7, 7, 9, 9, 8, 9, 9, 11, 9, 10, 9, 7, 10, 9, 9, 8, 7, 8, 7, 5, 6, 14, 12, 11, 7, 8, 9, 9, 7, 12, 9, 7, 9, 7, 8, 7, 8, 8, 7, 9, 6, 7, 10, 9, 8, 8, 7, 7, 7, 8, 8, 7, 7, 9, 9, 11, 8, 12, 7, 7, 7, 7, 7, 8, 10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 6, 10, 9, 7, 10, 8, 8, 8, 10, 9, 9, 7, 7, 8, 8, 7, 8, 9, 9, 7, 9, 10, 7, 9, 7, 8, 8, 8, 8, 8, 7, 10, 8, 8, 7, 9, 8, 7, 10, 7, 7, 6, 11, 10, 8, 11, 7, 7, 7, 7, 7, 8, 7, 8, 8, 8, 13, 9, 9, 10, 10, 11, 7, 8, 10, 7, 7, 6, 8, 8, 6, 9, 7, 8, 8, 8, 8, 8, 7, 7, 10, 10, 8, 9, 7, 10, 9, 7, 9, 8, 6, 10, 7, 7, 9, 7, 8, 8, 9, 7, 7, 7, 9, 8, 8, 8, 10, 10, 11, 5, 6, 9, 8, 7, 6, 8, 7, 10, 10, 12, 8, 8, 8, 9, 10, 6, 7, 8, 7, 8, 6, 7, 6, 7, 9, 7, 9, 7, 9, 10, 9, 9, 7, 10, 7, 7, 9, 11, 10, 10, 11, 9, 10, 8, 8, 7, 8, 7, 7, 8, 9, 7, 6, 9, 8, 6, 11, 9, 8, 10, 6, 6, 7, 7, 8, 6, 8, 11, 9, 9, 8, 9, 6, 9, 8, 7, 7, 9, 8, 7, 10, 9, 8, 10, 8, 8, 8, 8, 14, 8, 7, 9, 8, 9, 8, 8, 12, 7, 10, 7, 8, 10, 10, 9, 7, 8, 8, 8, 7, 8, 6, 8, 7, 11, 11, 8, 5, 9, 7, 10, 9, 9, 8, 7, 7, 8, 10, 9, 9, 9, 7, 8, 6, 7, 9, 7, 9, 8, 9, 9, 7, 9, 8, 7, 6, 8, 9, 8, 8, 8, 7, 7, 9, 13, 9, 8, 8, 8, 9, 8, 10, 12, 8, 9, 9, 9, 9, 11, 9, 8, 10, 11, 7, 10, 8, 6, 9, 7, 7, 10, 7, 9, 6, 10, 11, 8, 8, 8, 11, 8, 9, 8, 6, 7, 6, 6, 16, 18, 7, 10, 9, 8, 7, 6, 8, 7, 15, 9, 12, 25, 23, 12, 11, 8, 8, 15, 23, 96, 65, 53, 259, 20, 13, 21, 8, 8, 9, 7, 8, 8, 6, 8, 6, 8, 8, 8, 7, 6, 9, 7, 7, 8, 9, 7, 7, 9, 10, 7, 9, 8, 8, 9, 8, 7, 7, 9, 9, 7, 11, 8, 9, 9, 8, 8, 8, 8, 9, 11, 8, 8, 7, 6, 5, 9, 7, 7, 7, 8, 9, 9, 7, 9, 6, 13, 7, 8, 7, 13, 14, 7, 10, 10, 9, 6, 6, 8, 11, 12, 7, 7, 9, 8, 9, 8, 10, 11, 6, 9, 8, 7, 10, 9, 8, 8, 9, 9, 8, 8, 6, 8, 9, 8, 10, 9, 8, 12, 8, 6, 6, 7, 8, 8, 12, 12, 10, 8, 9, 8, 6, 7, 7, 7, 9, 9, 9, 11, 6, 9, 8, 6, 7, 7, 9, 10, 7, 7, 10, 6, 6, 8, 8, 8, 9, 8, 11, 7, 8, 6, 7, 7, 7, 8, 8, 9, 6, 8, 9, 8, 7, 7, 7, 6, 9, 6, 8, 7, 17, 8, 8, 9, 9, 7, 8, 7, 7, 7, 11, 9, 9, 8, 7, 9, 10, 6, 8, 9, 5, 7, 6, 6, 8, 6, 8, 9, 6, 9, 10, 10, 9, 8, 8, 8, 7, 7, 6, 8, 8, 8, 9, 8, 11, 8, 8, 8, 7, 8, 6, 8, 8, 10, 10, 7, 10, 8, 10, 7, 7, 6, 10, 8, 9, 6, 7, 10, 9, 8, 8, 7, 9, 9, 7, 7, 7, 6, 8, 8, 7, 9, 9, 8, 8, 9, 9, 9, 6, 7, 15, 9, 7, 7, 8, 8, 8, 11, 7, 8, 9, 8, 9, 9, 14, 5, 14, 8, 10, 8, 8, 7, 7, 7, 7, 9, 8, 8, 9, 6, 9, 7, 6, 8, 9, 7, 8, 8, 6, 9, 7, 8, 8, 7, 7, 9, 7, 7, 7, 7, 7, 8, 10, 10, 9, 6, 8, 7, 7, 6, 8, 8, 6, 7, 11, 7, 8, 8, 7, 8, 7, 10, 10, 11, 7, 10, 12, 8, 7, 7, 8, 7, 6, 10, 10, 11, 6, 7, 7, 8, 8, 8, 9, 8, 8, 8, 6, 7, 11, 7, 9, 10, 9, 7, 7, 7, 9, 10, 8, 9, 10, 6, 8, 8, 8, 9, 8, 7, 10, 8, 7, 7, 8, 6, 9, 7, 7, 8, 4, 9, 10, 10, 9, 8, 8, 8, 8, 7, 7, 10, 7, 7, 10, 9, 10, 8, 6, 8, 9, 10, 11, 7, 9, 8, 7, 10, 10, 8, 9, 6, 7, 7, 7, 9, 10, 9, 8, 9, 10, 8, 7, 7, 9, 8, 7, 9, 10, 10, 6, 7, 8, 9, 10, 11, 9, 8, 6, 9, 8, 7, 8, 6, 7, 8, 11, 8, 7, 9, 7, 7, 10, 10, 8, 8, 8, 7, 8, 7, 8, 9, 7, 9, 7, 9, 8, 8, 10, 7, 8, 8, 7, 7, 7, 8, 11, 10, 11, 11, 6, 6, 10, 8, 9, 10, 9, 7, 7, 6, 7, 7, 10, 7, 7, 11, 8, 7, 9, 10, 9, 9, 10, 8, 10, 8, 8, 8, 9, 7, 8, 8, 8, 11, 7, 8, 8, 9, 8, 8, 8, 8, 8, 7, 8, 6, 9, 10, 8, 8, 11, 8, 7, 6, 7]

    """

    main()
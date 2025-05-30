import time

import numpy as np

from itertools import groupby
from operator import itemgetter

import rust_bindings
from prob import calculate_confidence_scores

def main():

    reference_path_str = "./validator/example/diptera_references.fasta"
    queries_path_str = "./validator/example/diptera_queries_triple.fasta"
    queries_path_str_control = "./validator/example/diptera_queries_complement_alternate.fasta"

    print(time.perf_counter())

    #results_control, reference_sizes_control, names_control = rust_bindings.parse_input1(reference_path_str, queries_path_str, False)

    #res1, reference_sizes_control, nam1 = rust_bindings.parse_input1(reference_path_str, queries_path_str_control, True)

    results, reference_sizes, names = rust_bindings.parse_input1(reference_path_str, queries_path_str, True)
    print(time.perf_counter())

    #check_similarity(results, res1)

    """
    print("control is the same:")
    # Vergleiche Element für Element
    equal = np.array(results[2]).flatten() == np.array(res1[2]).flatten()
    # Anzahl gleicher Elemente
    num_equal = np.sum(equal)
    # Gesamtanzahl der Elemente
    total = len(reference_sizes)
    # Prozentuale Übereinstimmung
    percentage = (num_equal / total) * 100
    print(percentage)
    print()"""

    #print("reference sizes:")
    #print(reference_sizes)
    print()

    for x in results:
        t = x[1] // 2
        print(x[0])
        prob = calculate_confidence_scores(np.array(x[2]), np.array(reference_sizes), t, x[1])

        combined = list(zip(names, prob))
        #print(combined[:10])
        result = [(key, sum(p for _, p in group)) for key, group in groupby(combined, key=itemgetter(0))]
        #print(result[:10])
        filtered_result = sorted([(n, p) for n, p in result if p >= 0.005], key=lambda x: x[1], reverse=True)
        #print(filtered_result)

        for n, p in filtered_result:
            print(n, p)


        print()

        #print("Name:")
        #print(x[0])
        #print()

        #print("querie set size:")
        #print(x[1])
        #print()

        #print("intersection sizes:")
        #print(x[2])
        #print()

        #print("probability:")
        #print(prob)
        #print(np.sum(prob))

        #print("result:")
        #print(x[0], max(prob))


        print("name : intersection size")
        k = 30
        indices = np.argpartition(x[2], -k)[-k:]
        print(sorted(indices))
        top_k_data = [(names[i], x[2][i]) for i in indices]
        top_k_data_sorted = sorted(top_k_data, key=lambda x: x[1], reverse=True)
        for name, size in top_k_data_sorted:
            print(name, size)

        indices = np.argpartition(prob, -k)[-k:]
        top_k_data = [(names[i], prob[i]) for i in indices]
        top_k_data_sorted = sorted(top_k_data, key=lambda x: x[1], reverse=True)
        for name, size in top_k_data_sorted:
            print(name, size)

        print(len(prob), len(names))

    print(time.perf_counter())


    #print(reference_sizes)

    print("----------------------------------------------------------")

if __name__ == "__main__":
    main()
"""
output_adapters.py

Description
-----------
Module responsible for formatting, filtering and exporting classification results.
"""
import time
import itertools
import operator
from pathlib import Path

import raxtax_extension_prototype.prob_fast as prob_fast

def evaluate_confidence_scores(names, prob):
    """
    Aggregates, ranks, and filters confidence scores to identify relevant
    results.

    Scores associated with identical names are aggregated, sorted in
    descending order, and filtered using a minimum confidence threshold
    of 0.5%. If no result exceeds the threshold, the highest-scoring
    entry is returned to ensure a non-empty result.

    Parameters
    ----------
    names : iterable
        Identifiers associated with the confidence scores (e.g.,
        reference or lineage names).
    prob : iterable
        Confidence scores corresponding to the provided names.

    Returns
    -------
    list of tuples
        List of (name, confidence_score) pairs representing the filtered
        and ranked results.
    """
    combined = list(zip(names, prob))
    result = [(key, sum(p for _, p in group)) for key, group in itertools.groupby(combined, key=operator.itemgetter(0))]
    sorted_result = sorted([(n, float(round(p, 2))) for n, p in result], key=lambda x: x[1], reverse=True)

    filtered_result = [(n, p) for n, p in sorted_result if p >= 0.005]

    if not filtered_result:
        filtered_result.append(sorted_result[0])

    return filtered_result

def output_s_t(results, reference_names, runtime_info, result_dir: Path, total_execution_time, confidence_threshold=0.5):
    """
    Evaluates and records confidence scores and evaluation metrics.

    For each query, confidence scores are computed and written to an
    output file. Predictions are evaluated using a confidence threshold to
    determine true positives, false positives, false negatives and
    misclassifications. Summary statistics and runtime information are
    stored as metadata.

    Parameters
    ----------
    results : list of tuples
        Matching results for all queries. Each entry is a tuple of the form
        (query_name, query_kmer_set_size, intersection_sizes), where
        intersection_sizes is a list of k-mer intersection sizes between
        the query and all reference sequences.
    reference_names : list of str
        Names of the reference sequences.
    runtime_info : dict
        Runtime measurements for the individual processing steps.
    result_dir : pathlib.Path
        Directory where result files and metadata are written.
    total_execution_time : float
        Total execution time of the simulation.
    confidence_threshold : float, optional
        Minimum confidence score required for a positive classification.

    Returns
    -------
    None
        Results and metadata are written to disk.
    """
    tp = 0
    mc = 0
    fn = 0
    fp = 0

    average_prob_calculation_time = 0

    result_dir.mkdir(exist_ok=True)
    results_file = result_dir / "results.out"

    with results_file.open("w") as f:
        for query_name, query_set_size, intersection_sizes in results:
            f.write(query_name + "\n")
            t = query_set_size // 2

            start_calculation_prob_time = time.perf_counter()
            prob = prob_fast.calculate_confidence_scores(intersection_sizes, t, query_set_size)
            end_calculation_prob_time = time.perf_counter()
            calculation_prob_time = end_calculation_prob_time - start_calculation_prob_time

            average_prob_calculation_time += calculation_prob_time

            filtered_result = evaluate_confidence_scores(reference_names, prob)

            for (n, p) in filtered_result:
                f.write(str(n) + ": " + str(p) + "\n")

            if filtered_result[0][1] > confidence_threshold:
                if filtered_result[0][0] == query_name:
                    tp += 1
                elif query_name in reference_names:
                    mc += 1
                else:
                    fp += 1
            else:
                if query_name in reference_names:
                    fn += 1
    average_prob_calculation_time /= len(results)

    if tp == 0:
        recall = 0
        precision = 0
        f1_score = 0
    else:
        recall = tp / (tp + mc + fn)
        precision = tp / (tp + fp)
        f1_score = 2 * precision * recall / (recall + precision)

    metadata = {
        "reference_count": len(reference_names),
        "query_count": len(results),
        "total_execution_time": total_execution_time,
        "reference_parse_time": runtime_info["reference_parse_time"],
        "query_parse_time": runtime_info["query_parse_time"],
        "orient_queries_time": runtime_info["orient_queries_time"],
        "calculate_intersection_sizes_time": runtime_info["calculate_intersection_sizes_time"],
        "average_reference_processing_time": runtime_info["average_reference_processing_time"],
        "average_prob_calculation_time": average_prob_calculation_time,
        "tp": tp,
        "mc": mc,
        "fp": fp,
        "fn": fn,
        "recall": round(recall, 2),
        "precision": round(precision, 2),
        "f1_score": round(f1_score, 2),
    }

    output_meta_data(result_dir, metadata)

def output_meta_data(result_dir: Path, metadata):
    """
    Writes metadata key–value pairs to a metadata output file.
    """
    result_dir.mkdir(exist_ok=True)
    results_file = result_dir / "metadata.out"

    with results_file.open("w") as f:
        for key, value in metadata.items():
            f.write(key + ": " + str(value) + "\n")
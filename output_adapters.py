import time
from itertools import groupby
from operator import itemgetter
from pathlib import Path

from prob_fast import calculate_confidence_scores


def evaluate_confidence_scores(names, prob):

    combined = list(zip(names, prob))
    result = [(key, sum(p for _, p in group)) for key, group in groupby(combined, key=itemgetter(0))]
    sorted_result = sorted([(n, float(round(p, 2))) for n, p in result], key=lambda x: x[1], reverse=True)

    filtered_result = [(n, p) for n, p in sorted_result if p >= 0.005]

    if not filtered_result:
        filtered_result.append(sorted_result[0])

    return filtered_result

def print_lineage_matching(lineage_confidences):
    for (n, p) in lineage_confidences:
        print(n, p)

def output_sim_miseq(results, reference_names, runtime_info, result_dir: Path, confidence_threshold=0.5):

    reference_names_short = [name.split(",")[-1][2:-1] for name in reference_names]

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
            query_name_short = "_".join(query_name.split("_")[1:-2])

            print(query_name, query_set_size)
            print(intersection_sizes)

            start_calculation_prob_time = time.perf_counter()
            prob = calculate_confidence_scores(intersection_sizes, t, query_set_size)
            end_calculation_prob_time = time.perf_counter()
            calculation_prob_time = end_calculation_prob_time - start_calculation_prob_time

            average_prob_calculation_time += calculation_prob_time

            filtered_result = evaluate_confidence_scores(reference_names_short, prob)

            for (n, p) in filtered_result:
                f.write(str(n) + ": " + str(p) + "\n")

            if filtered_result[0][1] >= confidence_threshold:
                if filtered_result[0][0] == query_name_short:
                    tp += 1
                elif query_name_short in reference_names_short:
                    mc += 1
                else:
                    fp += 1
            else:
                if query_name_short in reference_names_short:
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
        "reference_parse_time": runtime_info["reference_parse_time"],
        "query_parse_time": runtime_info["query_parse_time"],
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

def output_s_t(results, reference_names, runtime_info, result_dir: Path, total_execution_time, confidence_threshold=0.5):
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

            print(query_name, query_set_size)
            print(intersection_sizes)

            start_calculation_prob_time = time.perf_counter()
            prob = calculate_confidence_scores(intersection_sizes, t, query_set_size)
            end_calculation_prob_time = time.perf_counter()
            calculation_prob_time = end_calculation_prob_time - start_calculation_prob_time

            average_prob_calculation_time += calculation_prob_time

            filtered_result = evaluate_confidence_scores(reference_names, prob)

            for (n, p) in filtered_result:
                f.write(str(n) + ": " + str(p) + "\n")

            if filtered_result[0][1] > confidence_threshold:
                if filtered_result[0][0] == query_name:
                    tp += 1
                else:
                    mc += 1
            else:
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
    result_dir.mkdir(exist_ok=True)
    results_file = result_dir / "metadata.out"

    with results_file.open("w") as f:
        for key, value in metadata.items():
            f.write(key + ": " + str(value) + "\n")
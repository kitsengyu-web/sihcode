import sys
from pathlib import Path
import json
PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

from embedding.rerank_retrieval import (
    search_bis,
    RETRIEVAL_TOP_K,
)

from metrics import calculate_metrics


# ============================================================
# PATHS
# ============================================================

EVALUATION_DIR = Path(__file__).resolve().parent

QUERIES_FILE = EVALUATION_DIR / "queries.json"


# ============================================================
# LOAD QUERIES
# ============================================================

with open(
    QUERIES_FILE,
    "r",
    encoding="utf-8"
) as f:
    queries = json.load(f)


# ============================================================
# EVALUATE ONE METHOD
# ============================================================

def evaluate_method(
    query,
    relevant_standards,
    method
):
    """
    Evaluate one retrieval method.

    Methods:
        bge
        cross_encoder
        hybrid
    """

    results = search_bis(
        query=query,
        retrieval_top_k=RETRIEVAL_TOP_K,
        final_top_k=RETRIEVAL_TOP_K,
    )

    if method == "bge":

        ranked_results = sorted(
            results,
            key=lambda x: x["bge_distance"]
        )

    elif method == "cross_encoder":

        ranked_results = sorted(
            results,
            key=lambda x: x["cross_encoder_raw"],
            reverse=True
        )

    elif method == "hybrid":

        ranked_results = sorted(
            results,
            key=lambda x: x["hybrid_score"],
            reverse=True
        )

    else:
        raise ValueError(
            f"Unknown method: {method}"
        )

    metrics = calculate_metrics(
        ranked_results,
        relevant_standards
    )

    return ranked_results, metrics


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():

    methods = [
        "bge",
        "cross_encoder",
        "hybrid"
    ]

    all_metrics = {
        method: []
        for method in methods
    }

    print()
    print("=" * 80)
    print("BIS RETRIEVAL EVALUATION")
    print("=" * 80)

    for item in queries:

        query = item["query"]

        relevant_standards = set(
            item["relevant_standards"]
        )

        print()
        print("-" * 80)
        print(f"QUERY: {query}")
        print(
            f"RELEVANT: "
            f"{', '.join(relevant_standards)}"
        )
        print("-" * 80)

        for method in methods:

            ranked_results, metrics = evaluate_method(
                query=query,
                relevant_standards=relevant_standards,
                method=method
            )

            all_metrics[method].append(
                metrics
            )

            top_10 = ranked_results[:10]

            print()
            print(f"{method.upper()}")

            print(
                f"Recall@5  : "
                f"{metrics['recall@5']:.3f}"
            )

            print(
                f"Recall@10 : "
                f"{metrics['recall@10']:.3f}"
            )

            print(
                f"MRR       : "
                f"{metrics['mrr']:.3f}"
            )

            print(
                f"nDCG@10   : "
                f"{metrics['ndcg@10']:.3f}"
            )

            print("Top 10:")

            for rank, result in enumerate(
                top_10,
                start=1
            ):

                standard_number = result[
                    "standard_number"
                ]

                standard_name = result[
                    "standard_name"
                ]

                print(
                    f"{rank:2}. "
                    f"{standard_number} "
                    f"- {standard_name}"
                )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print()
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    print()

    print(
        f"{'METHOD':<20}"
        f"{'R@5':>10}"
        f"{'R@10':>10}"
        f"{'MRR':>10}"
        f"{'nDCG@10':>12}"
    )

    print("-" * 62)

    for method in methods:

        metric_list = all_metrics[method]

        count = len(metric_list)

        if count == 0:
            continue

        recall_5 = sum(
            x["recall@5"]
            for x in metric_list
        ) / count

        recall_10 = sum(
            x["recall@10"]
            for x in metric_list
        ) / count

        mrr_score = sum(
            x["mrr"]
            for x in metric_list
        ) / count

        ndcg = sum(
            x["ndcg@10"]
            for x in metric_list
        ) / count

        print(
            f"{method:<20}"
            f"{recall_5:>10.3f}"
            f"{recall_10:>10.3f}"
            f"{mrr_score:>10.3f}"
            f"{ndcg:>12.3f}"
        )

    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
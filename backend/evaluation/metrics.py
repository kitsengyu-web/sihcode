import math


def get_standard_number(result):
    """
    Extract the standard number from a retrieval result.

    Supports:
        result["standard_number"]

    Also handles nested metadata as a fallback.
    """

    if isinstance(result, str):
        return result

    if not isinstance(result, dict):
        return None

    standard_number = result.get(
        "standard_number"
    )

    if standard_number:
        return str(standard_number)

    metadata = result.get(
        "metadata"
    )

    if isinstance(metadata, dict):

        standard_number = metadata.get(
            "standard_number"
        )

        if standard_number:
            return str(standard_number)

    return None


def recall_at_k(
    results,
    relevant_standards,
    k
):
    """
    Query-level Recall@K.

    Returns 1 if at least one relevant
    standard appears in top-k.
    """

    relevant = {
        str(standard)
        for standard in relevant_standards
    }

    retrieved = {
        get_standard_number(result)
        for result in results[:k]
    }

    retrieved.discard(None)

    return 1.0 if (
        retrieved & relevant
    ) else 0.0


def mrr(
    results,
    relevant_standards
):
    """
    Mean Reciprocal Rank for one query.
    """

    relevant = {
        str(standard)
        for standard in relevant_standards
    }

    for rank, result in enumerate(
        results,
        start=1
    ):

        standard_number = (
            get_standard_number(result)
        )

        if standard_number in relevant:
            return 1.0 / rank

    return 0.0


def ndcg_at_k(
    results,
    relevant_standards,
    k
):
    """
    Binary relevance nDCG@K.
    """

    relevant = {
        str(standard)
        for standard in relevant_standards
    }

    dcg = 0.0

    for rank, result in enumerate(
        results[:k],
        start=1
    ):

        standard_number = (
            get_standard_number(result)
        )

        if standard_number in relevant:

            dcg += (
                1.0
                / math.log2(rank + 1)
            )

    ideal_relevant_count = min(
        len(relevant),
        k
    )

    if ideal_relevant_count == 0:
        return 0.0

    idcg = sum(
        1.0 / math.log2(rank + 1)
        for rank in range(
            1,
            ideal_relevant_count + 1
        )
    )

    if idcg == 0:
        return 0.0

    return dcg / idcg


def calculate_metrics(
    results,
    relevant_standards
):
    """
    Calculate all metrics for one query.
    """

    return {

        "recall@5": recall_at_k(
            results,
            relevant_standards,
            5
        ),

        "recall@10": recall_at_k(
            results,
            relevant_standards,
            10
        ),

        "mrr": mrr(
            results,
            relevant_standards
        ),

        "ndcg@10": ndcg_at_k(
            results,
            relevant_standards,
            10
        ),
    }


def average_metrics(
    metrics_list
):
    """
    Average metrics across queries.
    """

    if not metrics_list:

        return {
            "recall@5": 0.0,
            "recall@10": 0.0,
            "mrr": 0.0,
            "ndcg@10": 0.0,
        }

    return {

        "recall@5": sum(
            metrics["recall@5"]
            for metrics in metrics_list
        ) / len(metrics_list),

        "recall@10": sum(
            metrics["recall@10"]
            for metrics in metrics_list
        ) / len(metrics_list),

        "mrr": sum(
            metrics["mrr"]
            for metrics in metrics_list
        ) / len(metrics_list),

        "ndcg@10": sum(
            metrics["ndcg@10"]
            for metrics in metrics_list
        ) / len(metrics_list),
    }
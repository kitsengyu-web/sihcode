from rerank_retrieval import search_bis
from relationship_expansion import build_relationship_context


query = "drinking water quality"

results = search_bis(
    query,
    retrieval_top_k=30,
    final_top_k=5,
)

print("\n" + "=" * 80)
print("RELATIONSHIP EXPANSION")
print("=" * 80)

for index, result in enumerate(results[:5], start=1):

    print(f"\n[{index}] {result['standard_number']}")
    print(result["standard_name"])

    print("\n" + build_relationship_context(result))
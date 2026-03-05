from rag_retriever import load_vector_store

vectorstore = load_vector_store()


def plan_trip(destination, days, budget):
    results = vectorstore.similarity_search(destination, k=3)

    if not results:
        return None, "No matching destination found"

    trip = []
    total_cost = 0
    reasoning = []

    for doc in results:
        daily_cost = int(doc.metadata["daily_cost"])
        cost = daily_cost * days

        reasoning.append(
            f"{doc.metadata['destination']} costs {daily_cost}/day → {cost} total"
        )

        if total_cost + cost <= budget:
            trip.append({
                "destination": doc.metadata["destination"],
                "days": days,
                "daily_cost": daily_cost,
                "total_cost": cost,
                "temperature": doc.metadata["avg_temp"]
            })
            total_cost += cost

    if not trip:
        return None, "Budget too low for selected destination"

    return {
        "itinerary": trip,
        "total_cost": total_cost,
        "remaining_budget": budget - total_cost
    }, reasoning
class EvaluationMetrics:

    def hit_rate_at_k(
        self,
        retrieved_ids,
        relevant_ids
    ):

        return int(
            any(
                chunk_id in relevant_ids
                for chunk_id in retrieved_ids
            )
        )

    def recall_at_k(
        self,
        retrieved_ids,
        relevant_ids
    ):

        hits = len(
            set(retrieved_ids)
            &
            set(relevant_ids)
        )

        return hits / len(relevant_ids)

    def mrr(
        self,
        retrieved_ids,
        relevant_ids
    ):

        for rank, chunk_id in enumerate(
            retrieved_ids,
            start=1
        ):

            if chunk_id in relevant_ids:

                return 1 / rank

        return 0
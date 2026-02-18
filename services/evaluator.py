class AnswerEvaluator:

    def evaluate(self, answer: str, context_chunks: list[str]) -> float:
        if not answer or len(answer.strip()) < 10:
            return 0.0

        answer_words = set(answer.lower().split())
        context_words = set(
            " ".join(context_chunks).lower().split()
        )

        overlap = answer_words.intersection(context_words)

        if not overlap:
            return 0.0

        coverage = len(overlap) / max(len(answer_words), 1)

        return round(min(coverage * 2, 1.0), 2)

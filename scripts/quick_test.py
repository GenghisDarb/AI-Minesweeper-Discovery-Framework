from ai_minesweeper import BoardBuilder, SpreadRiskAssessor, ConfidencePolicy

# Define a trivial domain: 3 hypotheses, with a simple constraint like "at most 1 of these 3 is false".
hypotheses = [
    {"id": 1, "desc": "Hypothesis A", "neighbors": [2, 3]},
    {"id": 2, "desc": "Hypothesis B", "neighbors": [1, 3]},
    {"id": 3, "desc": "Hypothesis C", "neighbors": [1, 2]}
]
constraints = [
    {"neighbors": [1, 2, 3], "max_false": 1}
]

# Build the board
board = BoardBuilder.from_manual(hypotheses, constraints)
assessor = SpreadRiskAssessor()
policy = ConfidencePolicy(SpreadRiskAssessor, None)

# Simulate one step
probs = assessor.get_probabilities(board)
print("Initial probabilities:", probs)
choice = policy.pick(board)
print("Chosen hypothesis to test:", choice)

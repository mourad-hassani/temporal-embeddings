from temporal_embeddings.evaluation.evaluation import Evaluator
from temporal_embeddings.utils.save import save_json
from temporal_embeddings.parameters.parameters import OUTPUT_DIRECTORY_PATH

evaluator: Evaluator = Evaluator()

evaluator.evaluate()

metrics: float = evaluator.evaluate()
save_json(metrics, OUTPUT_DIRECTORY_PATH / "metrics.json")
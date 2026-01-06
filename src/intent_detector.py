import json
from typing import Tuple, Optional
from src.embedding_utils import get_embedding
from src.similarity import cosine_similarity


class IntentDetector:
    def __init__(self, intents_file: str):
        with open(intents_file, "r") as f:
            self.intents = json.load(f)["intents"]

        # Precompute embeddings once
        self.intent_embeddings = []
        for intent in self.intents:
            for example in intent["examples"]:
                emb = get_embedding(example)
                self.intent_embeddings.append({
                    "intent": intent,
                    "embedding": emb
                })

    def get_intent(self, query: str, threshold: float = 0.6) -> Tuple[Optional[dict], float]:
        query_embedding = get_embedding(query)

        best_score = 0.0
        best_intent = None

        for item in self.intent_embeddings:
            score = cosine_similarity(query_embedding, item["embedding"])
            if score > best_score:
                best_score = score
                best_intent = item["intent"]

        if best_score >= threshold:
            return best_intent, best_score

        return None, best_score

    def is_private_intent(self, intent_id: str) -> bool:
        for intent in self.intents:
            if intent["intent_id"] == intent_id:
                return intent.get("is_private", False)
        return False

    def get_general_intents(self):
        return [i for i in self.intents if not i.get("is_private")]

    def get_employee_intents(self):
        return [i for i in self.intents if i.get("is_private")]

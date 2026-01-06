from src.intent_detector import IntentDetector

# Test the improved intent detection
detector = IntentDetector()

# Test cases that were failing
test_queries = [
    "What can you do?",
    "What are your capabilities?",
    "How can you help me?",
    "Tell me what you can do",
    "What services do you provide?"
]

print("Testing improved intent detection for general_inquiry:")
print("=" * 60)

for query in test_queries:
    intent, confidence = detector.get_intent(query)
    if intent:
        print(f"Query: '{query}'")
        print(f"  Intent: {intent['intent_id']} - {intent['name']}")
        print(f"  Confidence: {confidence:.3f}")
        print()
    else:
        print(f"Query: '{query}'")
        print("  No intent detected")
        print()

# Test some other intents to make sure we didn't break anything
other_tests = [
    "Hello",
    "What is the leave policy?",
    "How many leaves do I have?",
    "Who is my manager?"
]

print("Testing other intents:")
print("=" * 60)

for query in other_tests:
    intent, confidence = detector.get_intent(query)
    if intent:
        print(f"Query: '{query}'")
        print(f"  Intent: {intent['intent_id']} - {intent['name']}")
        print(f"  Confidence: {confidence:.3f}")
        print()
    else:
        print(f"Query: '{query}'")
        print("  No intent detected")
        print()

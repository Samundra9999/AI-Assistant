fallback_responses = {
    "hi": "Hello! How can I assist you today?",
    "hello": "Hi there! What would you like to know?",
    "hey": "Hey! How can I help?",
    "good morning": "Good morning! How can I help you today?",
    "good afternoon": "Good afternoon! What would you like to ask?",
    "good evening": "Good evening! How can I assist you?",
    "good night": "Good night! Take care and sleep well!",
    "how are you": "I'm doing great! How about you?",
    "how is it going": "I'm fine, thanks for asking! How about you?",
    "what's up": "All good here! How can I help you today?",
    "how do you do": "I'm doing well, thank you! How can I assist?",
    "thanks": "You're welcome! Happy to help!",
    "thank you": "No problem! Let me know if you have more questions.",
    "thx": "You're welcome!",
    "appreciate it": "Glad I could help!",
    "bye": "Goodbye! Have a great day!",
    "see you": "See you! Take care!",
    "goodbye": "Bye! Let me know if you need help again."


}

def check_small_talk(query: str):
    query_lower = query.lower()
    for key, response in fallback_responses.items():
        if key in query_lower:
            return response
    return None

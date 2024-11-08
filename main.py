from cipher.basic.person import Person, Conversation

# Create people
alice = Person("Alice", 25)
bob = Person("Bob", 30)

# Create a conversation
chat = Conversation(context="AI and consciousness")

# Have people join the conversation
alice.join_conversation(chat)
bob.join_conversation(chat)

# Simulate some interaction
alice.speak("What do you think about artificial consciousness?")
bob.think("Considering artificial consciousness...")
bob.speak("I think it's a complex topic that requires careful consideration.")
alice.speak("Interesting perspective! Can you elaborate?")

# Check the conversation history
print("\nConversation history:")
for message in chat.message_history:
    print(message)

# Check Alice's memories about the conversation
print("\nAlice's memories about this conversation:")
for memory in alice.memory.retrieve_relevant_memories("consciousness", chat.id):
    print(f"{memory['timestamp']}: {memory['content']}, by {memory['source']}")
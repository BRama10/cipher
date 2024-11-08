from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class Message:
    content: str
    speaker: 'Person'
    timestamp: datetime = field(default_factory=datetime.now)
    context: Optional[str] = None

    def __repr__(self):
        return f"{self.speaker.name} ({self.timestamp.strftime('%H:%M:%S')}): {self.content}"

class Memory:
    def __init__(self):
        self.personal_memories: List[Dict] = []
        self.conversation_indices: Dict[int, List[int]] = {}  # Maps conversation_id to message indices
    
    def add_memory(self, memory_type: str, content: str, source: Optional[str] = None, 
                  conversation_id: Optional[int] = None):
        """Add a new memory with metadata"""
        memory = {
            'type': memory_type,  # 'thought', 'conversation', 'experience', etc.
            'content': content,
            'source': source,
            'timestamp': datetime.now(),
            'conversation_id': conversation_id
        }
        self.personal_memories.append(memory)
        
        if conversation_id is not None:
            if conversation_id not in self.conversation_indices:
                self.conversation_indices[conversation_id] = []
            self.conversation_indices[conversation_id].append(len(self.personal_memories) - 1)
    
    def retrieve_relevant_memories(self, context: str, conversation_id: Optional[int] = None) -> List[Dict]:
        """
        Retrieve memories relevant to the current context
        In a real implementation, this could use embedding similarity or other relevance metrics
        """
        # Simple implementation - could be enhanced with actual similarity search
        relevant_memories = []
        
        # If conversation_id provided, prioritize memories from that conversation
        if conversation_id and conversation_id in self.conversation_indices:
            for idx in self.conversation_indices[conversation_id]:
                relevant_memories.append(self.personal_memories[idx])
        
        # Add other relevant memories based on context
        # This is where you could implement more sophisticated memory retrieval
        for memory in self.personal_memories:
            if context.lower() in memory['content'].lower():
                relevant_memories.append(memory)
                
        return relevant_memories

class Conversation:
    def __init__(self, context: str = "general"):
        self.id: int = id(self)  # Unique identifier for the conversation
        self.participants: List[Person] = []
        self.message_history: List[Message] = []
        self.context: str = context
    
    def add_participant(self, person: 'Person'):
        if person not in self.participants:
            self.participants.append(person)
    
    def add_message(self, message: Message) -> None:
        """Add a message to the conversation and update all participants' memories"""
        self.message_history.append(message)
        
        # Update each participant's memory of the conversation
        for participant in self.participants:
            participant.memory.add_memory(
                memory_type='conversation',
                content=message.content,
                source=message.speaker.name,
                conversation_id=self.id
            )
    
    def get_recent_messages(self, n: int = 5) -> List[Message]:
        """Get the n most recent messages"""
        return self.message_history[-n:]
    
    def get_context(self) -> str:
        """Get the current conversation context plus recent message summary"""
        recent_messages = self.get_recent_messages()
        context = f"Conversation about {self.context}\n"
        context += "Recent messages:\n"
        context += "\n".join(str(msg) for msg in recent_messages)
        return context

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.memory = Memory()
        self.current_conversation: Optional[Conversation] = None
    
    def join_conversation(self, conversation: Conversation):
        """Join a conversation"""
        self.current_conversation = conversation
        conversation.add_participant(self)
    
    def think(self, context: str) -> str:
        """
        Generate thoughts based on context and memory
        This could integrate with an LLM
        """
        # Retrieve relevant memories
        relevant_memories = self.memory.retrieve_relevant_memories(
            context, 
            self.current_conversation.id if self.current_conversation else None
        )
        
        # Generate thought (this is where you'd integrate with an LLM)
        thought = f"Thinking about {context} based on {len(relevant_memories)} relevant memories..."
        
        # Store the thought in memory
        self.memory.add_memory('thought', thought)
        return thought
    
    def speak(self, message_content: str) -> None:
        """Speak a message in the current conversation"""
        if not self.current_conversation:
            raise ValueError("Not in a conversation")
            
        message = Message(content=message_content, speaker=self)
        self.current_conversation.add_message(message)
    
    def listen(self, message: Message) -> None:
        """
        Process a received message
        This could trigger thoughts or automatic responses
        """
        # Store the heard message in memory
        self.memory.add_memory(
            memory_type='heard',
            content=message.content,
            source=message.speaker.name,
            conversation_id=self.current_conversation.id if self.current_conversation else None
        )
        
        # Generate a thought about the message (could be integrated with LLM)
        self.think(f"Response to {message.content}")
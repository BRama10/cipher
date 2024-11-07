import ollama
import json

# Function to recommend an agent based on a prompt
def recommend_agent(prompt):
    agents = {
        "academic_agent": "Provides academic guidance, generates research insights, and assists with scholarly writing.",
        "math_agent": "Solves mathematical problems, explains concepts, and provides tutoring on complex equations.",
        "cocktail_mixlogist": "Suggests and customizes cocktail recipes based on ingredients and user preferences.",
        "cook_therapist": "Combines cooking advice with therapeutic insights to make meal prep a relaxing experience.",
        "creation_agent": "Assists with brainstorming and creating content for writing, art, or other creative projects.",
        "festival_card_designer": "Designs greeting cards and invitations for festivals and celebrations, customized to themes and styles.",
        "fitness_trainer": "Provides workout plans, fitness tips, and personalized training advice to meet health goals.",
        "logo_creator": "Generates logo designs for branding, using customizable templates and artistic styles.",
        "meme_creator": "Creates memes based on popular formats or user-submitted text for social media engagement.",
        "music_composer": "Composes original music, generates loops and samples, and customizes tunes based on mood and genre.",
        "story_teller": "Crafts stories, narratives, and interactive fiction, engaging users with creative storytelling."
    }

    # Prepare the prompt for Ollama with a strict JSON output requirement
    ollama_prompt = f"""You are an assistant that strictly outputs JSON-formatted responses. 
Based on the following user input, select the best agent from the list and provide a justification in JSON format:
    
User Input: '{prompt}'

Agents:
{json.dumps(agents, indent=2)}

Respond with only the following JSON structure:
{{
    "recommended_agent": "<agent_name>",
    "justification": "<reason for selecting the agent>"
}}"""

    # Call Ollama to get the response
    response = ollama.chat(model="llama3.2", messages=[
        {
            'role': 'user',
            'content': ollama_prompt,
        },
    ])

    # Attempt to parse and print the response as JSON
    try:
        recommendation = json.loads(response['message']['content'])
        print(json.dumps(recommendation, indent=2))
    except json.JSONDecodeError:
        print("Error: Response is not valid JSON.")

# Continuous loop for user input
while True:
    user_input = input("Enter your prompt (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        print("Exiting the program.")
        break
    recommend_agent(user_input)

from openai import OpenAI
from config import OPENAI_API_KEY

class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def call_llm(self, system_prompt, user_prompt):
        """
        Calls the OpenAI LLM with the given prompts.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o", # Or gpt-3.5-turbo if 4o is not available
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            self.log(f"Error calling LLM: {e}")
            return "Error generating response."

    def analyze(self, ticker):
        raise NotImplementedError("Subclasses must implement analyze method")
        
    def log(self, message):
        print(f"[{self.name}] {message}")

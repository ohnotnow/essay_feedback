from openai import OpenAI
from gepetto.gpt import Model

class Assistant:
    def __init__(self, id: str="", name: str="Feedback Assistant", model: str=Model.GPT_4_OMNI_0806.value[0], temperature: float = 1.0, top_p: float = 0.6, instructions: str="", api_key: str=""):
        if not api_key:
            raise ValueError("API key is required")
        self.client = OpenAI(api_key=api_key)
        self.assistant = self.get_assistant(id=id, name=name, model=model, temperature=temperature, top_p=top_p, instructions=instructions)
        self.id = self.assistant.id
        self.name = self.assistant.name
        self.model = self.assistant.model
        self.temperature = self.assistant.temperature
        self.top_p = self.assistant.top_p
        self.instructions = self.assistant.instructions

    def process_text(self, text: str) -> str:
        thread = self.create_thread()
        self.add_message_to_thread(thread_id=thread.id, message=text)
        run = self.run_assistant(thread_id=thread.id)
        return self.get_result(thread_id=thread.id)

    def create_assistant(self, name: str="", model: str="", temperature: float = 1.0, top_p: float = 0.6, instructions: str=""):
        assistant = self.client.beta.assistants.create(
            name=name,
            model=model,
            temperature=temperature,
            top_p=top_p,
            instructions=instructions
        )
        print(f"New assistant created: {assistant.id}")
        return assistant

    def get_assistant(self, id: str="", name: str="", model: str="", temperature: float = 1.0, top_p: float = 0.6, instructions: str=""):
        if not id:
            return self.create_assistant(name=name, model=model, temperature=temperature, top_p=top_p, instructions=instructions)
        assistant = self.client.beta.assistants.retrieve(assistant_id=id)
        return assistant

    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread

    def get_thread(self, id: str=""):
        if not id:
            return self.create_thread()
        thread = self.client.beta.threads.retrieve(thread_id=id)
        return thread

    def add_message_to_thread(self, thread_id: str, message: str):
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )

    def run_assistant(self, thread_id: str):
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=self.id
        )
        return run

    def get_run(self, thread_id: str, run_id: str):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        return run

    def get_thread_messages(self, thread_id: str):
        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        return messages

    def get_result(self, thread_id: str):
        messages = self.get_thread_messages(thread_id=thread_id)
        result = ""
        for message in messages.data:
            if message.role == "assistant":
                result += message.content[0].text.value
        return result

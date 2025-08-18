from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

class APIEvaluator:
    def __init__(self, api_key, api_base, model_name):
        self.llm = ChatOpenAI(
            verbose=True,
            openai_api_key=api_key,
            openai_api_base=api_base,
            model_name=model_name,
        )

    def answer(self, prompt):
        response = self.llm([HumanMessage(content=prompt)])
        return response.content

if __name__ == "__main__":
    evaluator = APIEvaluator()
    print(evaluator.answer("你好"))
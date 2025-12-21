from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os
import json
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from ..prompt import Question

load_dotenv()
api_key = os.getenv("HUGGINGFACE_API")

def image_content(content):
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    llm = HuggingFaceEndpoint(
    repo_id= repo_id,
    task="text-generation",
    huggingfacehub_api_token=api_key
    )
    model = ChatHuggingFace(llm = llm , temperature = 0.5)
    parser = PydanticOutputParser(pydantic_object=Question)

    template = PromptTemplate(template="""

    You are an expert question extract and your role is to extract questions from the paper
                          Rule for your role:
                          1) DO NOT Hallucinate.
                          2) DO NOT rewriting, rephrasing, or generating new questions
                          3) Do not change the content of the paper.
                          4) Avoid College name, year, pass marks, and other that are not related to questions.
                          5) Remove unnecessary numbers.

                          The paper content is :
                          -------------------
                               {paper}
                          -------------------

                          \n {format_instruction}

    """,
    input_variables=["paper"],
    partial_variables={"format_instruction":parser.get_format_instructions()})

    chain = template | model
    raw_result = chain.invoke({"paper":content})
    result = raw_result.model_dump()
    
    try:
        final_result = ((json.loads(result["content"]))["question"])
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"JSON Parse Error: {e}")
        print(f"Raw content: {result['content']}")
        # Fallback: return raw content or empty list
        return []
    
    return final_result




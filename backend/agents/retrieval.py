from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .conversation import check_small_talk

load_dotenv()
api_key = os.getenv("HUGGINGFACE_API")


def _truncate_text(text: str, max_chars: int = 20000):
        if not isinstance(text, str):
                return text
        if len(text) <= max_chars:
                return text
        truncated = text[:max_chars]
        last_dot = truncated.rfind('. ')
        if last_dot != -1 and last_dot > int(max_chars * 0.6):
                truncated = truncated[:last_dot+1]
        return truncated + "\n\n[TRUNCATED]"

def retreival_content(vector_store = None, image_content = None, query = None):
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    llm = HuggingFaceEndpoint(
    repo_id= repo_id,
    task="text-generation",
    huggingfacehub_api_token=api_key
    )
    model = ChatHuggingFace(llm = llm , temperature = 0.5)
    parser = StrOutputParser()

    if query and not vector_store and not image_content:
            prompt = PromptTemplate(
                    template="You are a helpful AI assistant. Answer user messages politely and concisely.\n\nUser: {user_input}\nAI:",
                    input_variables=["user_input"]
                    )
        
            chain = prompt| model | parser
            result = chain.invoke({"user_input":query})
            return result


    if vector_store and query and not image_content:
            prompt = PromptTemplate(template="""

                    You are an expert Assistant and your role is to give the correct answer of the user question from the given documents.
                     Rule to Follow:
                            1) DO NOT Hallucinate.
                            2) DO NOT WRITE ANYTHING THAT ARE NOT INCLUDED IN DOCUMENTS
                            3) DO NOT rewriting, rephrasing, or generating new questions
                            4) Do not change the content of the paper.
                            5) If there is not any content in the douments  related to user query you must simply say "Sorry! Content Not Found."
                            
                            Documents for the question:
                            --------------------------
                                     {documents}
                            --------------------------

                            and the question is {question}

                    """,
                    input_variables=["documents","question"])
            retriever = vector_store.as_retriever(search_kwargs={"k": 2})
            docs = retriever.invoke(query)
            documents = "\n".join([doc.page_content for doc in docs])
            documents = _truncate_text(documents, max_chars=20000)
            chain = prompt | model | parser
            result = chain.invoke({"documents":documents,"question":query})
            return result


    if image_content and not query and not vector_store:
        prompt = PromptTemplate(template="""
                        You are an expert chatbot and your role is to give the correct and accurate answer of user questions
                                Rules to follow:
                                1) Do not hallucinate.
                                2) If you don't know any question simply say 'Sorry i don't know the answer'

                                user questions:
                                ---------------
                                  {questions}
                                ---------------
                        """,
                        input_variables=["questions"])
        chain = prompt | model | parser
        batch_inputs = [{"questions": q} for q in image_content]
        result = chain.batch(inputs=batch_inputs)
        return result



    if image_content and query and not vector_store:
        prompt = PromptTemplate(template="""
                        You are an expert chatbot and your role is to give the correct and accurate answer of user questions
                                Rules to follow:
                                1) Do not hallucinate.
                                2) If you don't know any question simply say 'Sorry i don't know the answer'

                                user questions:
                                ---------------
                                  {questions}
                                ---------------
                        """,
                        input_variables=["questions"])
        chain = prompt | model | parser
        batch_inputs = [{"questions": q} for q in image_content]
        result = chain.batch(inputs=batch_inputs)
        return result

    if vector_store and image_content and not query:
        template = PromptTemplate(template="""
                    You are an expert chatbot who extract the answer for the question from the document
                          Rules:
                          1) DO not hallucinate.
                          2) If you didn't find any content just say 'Sorry content is not available'

                          documents are :
                          --------------
                             {documents}
                          --------------

                          and the questions are:
                          --------------
                             {questions}
                          --------------
                    """,
                    input_variables=["documents","questions"])
        # batch retrieval: reduce k and truncate each document to avoid oversized requests
        retriever = vector_store.as_retriever(search_kwargs={"k": 2})
        batch_docs = retriever.batch(inputs=image_content)
        documents = ["\n".join([i.page_content for i in result]) for result in batch_docs]
        documents = [_truncate_text(d, max_chars=20000) for d in documents]
        chain = template | model | parser
        inputs = [{"documents":documents[i], "questions":query[i]}
                    for i in range(len(query))]

        result = chain.batch(inputs=inputs)
        return result


    if vector_store and image_content and query:
        template = PromptTemplate(template="""
                    You are an expert chatbot who extract the answer for the question from the document
                          Rules:
                          1) DO not hallucinate.
                          2) If you didn't find any content just say 'Sorry content is not available'

                          documents are :
                          --------------
                             {documents}
                          --------------

                          and the questions are:
                          --------------
                             {questions}
                          --------------
                    """,
                    input_variables=["documents","questions"])
        # batch retrieval for image+text case
        retriever = vector_store.as_retriever(search_kwargs={"k": 2})
        batch_docs = retriever.batch(inputs=image_content)
        documents = ["\n".join([i.page_content for i in result]) for result in batch_docs]
        documents = [_truncate_text(d, max_chars=20000) for d in documents]
        chain = template | model | parser
        inputs = [{"documents":documents[i], "questions":query[i]}
                    for i in range(len(query))]

        result = chain.batch(inputs=inputs)
        return result
    

    


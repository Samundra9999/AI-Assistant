from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace, HuggingFaceEmbeddings


def huggingface_model(api_key):
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    llm = HuggingFaceEndpoint(
        repo_id= repo_id,
        task="text-generation",
        huggingfacehub_api_token=api_key
        )

    model = ChatHuggingFace(llm = llm,temperature = 0.7)
    return model



def huggingface_embedding():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embedding = HuggingFaceEmbeddings(model_name = model_name)
    return embedding

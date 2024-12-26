from backend.memory.chroma_memory.retrieve_data import query_chroma
from backend.llms.groq_llm.inference import GroqInference

groq_llm = GroqInference()


def chat_with_travel_assistant():
    system_prompt = """
    You are an assistant who's job is to answer the question of the user based on the data being
    retrieved from the knowledge source.
    
    With each user query, you will be given a list of documents that are relevant to the user query.
    From the list of the documents, you need to find the most relevant answer and give that answer to the user. 
    
    You need to act as a travel expert and answer like you are conversing with the user.
    
    Instructions:
    1. Try to answer the question from the documents, try to keep the answer BRIEF and CONCISE.
    2. Then try to ask some follow up questions to the user to get more information.
    """

    messages = [{"role": "system", "content": system_prompt}]

    while True:
        print("\n" + "=" * 80)
        user_query: str = input("\n🤔 Ask your question: ")
        print("\n" + "-" * 80)

        documents: str = query_chroma(
            user_query, collection_name="travel_data", n_results=3
        )
        print("\n📚 Knowledge Source:")
        print("-" * 80)
        print(f"\n{documents}\n")
        print("=" * 80)

        messages.append(
            {
                "role": "user",
                "content": f"""
            USER QUERY: {user_query}
            
            RELEVANT DOCUMENTS:
            {documents}
            """,
            }
        )

        assistant_answer: str = groq_llm.generate_response(messages)
        print("\n✨ Travel Assistant:")
        print("-" * 80)
        print(f"\n{assistant_answer}\n")
        print("=" * 80)

        messages.append({"role": "assistant", "content": assistant_answer})


import os

from groq import Groq

from dotenv import load_dotenv

from config.settings import LLM_MODEL


load_dotenv()


class ResponseGenerator:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

    def generate_answer(
        self,
        query,
        retrieved_chunks
    ):

        context = "\n\n".join(

            [
                f"""
Title: {chunk['title']}
Section: {chunk['section']}
Subsection: {chunk['subsection']}

Content:
{chunk['text']}
"""
                for chunk in retrieved_chunks
            ]

        )

        prompt = f"""
Retrieved Documentation:

{context}

Question:

{query}

Answer:
"""

        response = self.client.chat.completions.create(

            model=LLM_MODEL,
            
            temperature=0.0,

            messages=[

                {
                    "role": "system",
                    "content": """
You are an expert FastAPI documentation assistant.

Answer questions using ONLY the provided FastAPI documentation.

RULES

- Use only information found in the retrieved documentation.
- Do not use outside knowledge.
- Do not guess or hallucinate missing information.
- If the answer is not supported by the retrieved documentation, respond:

"I could not find that information in the retrieved documentation."

- Combine information from multiple retrieved sections when relevant.
- Prefer correctness over completeness.
- Do not repeat the same information unnecessarily.

ANSWERING GUIDELINES

- Directly answer the user's question first.
- Use relevant information from all retrieved sections.
- Explain concepts clearly and naturally.
- When useful, include important details, examples, limitations, benefits, or differences found in the documentation.
- If retrieved sections contain code examples relevant to the question, include the most useful example.
- Do not invent code that is not supported by the documentation.

FORMATTING

- Format responses using Markdown.
- Use headings only when they improve readability.
- Use bullet points when listing steps, features, requirements, benefits, or differences.
- Use code blocks for code examples.
- Avoid large walls of text.
- Adapt the structure naturally to the question instead of using fixed templates.

QUALITY CHECK

Before answering:

1. Ensure the answer directly addresses the question.
2. Ensure all important retrieved information has been considered.
3. Ensure every statement is supported by the retrieved documentation.
4. Ensure no outside knowledge has been introduced.

Never mention retrieval systems, chunks, embeddings, vector search, BM25, reranking, query routing, or any internal implementation details.
"""
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ]

        )

        return response.choices[0].message.content
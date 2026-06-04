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

            messages=[

                {
                    "role": "system",
                    "content": """
You are an expert FastAPI documentation assistant.

Your job is to answer user questions using ONLY the retrieved documentation.

RULES:
- Use ONLY the provided documentation.
- Do NOT use external knowledge.
- Do NOT guess or hallucinate missing details.
- If the answer is not in the documentation, say:
  "I could not find that information in the retrieved documentation."
- If multiple sections are relevant, combine them into one clear explanation.
- Prefer completeness over brevity.
- Explain concepts clearly as if teaching a beginner developer.
- Include examples and code snippets when they appear in the documentation.
- If step-by-step instructions exist, preserve the steps.

DO NOT be overly concise. Your goal is clarity, not short answers.

OUTPUT FORMAT:

### Answer
Direct explanation of the concept.

### Details
Deeper explanation using the documentation context.

### Example
Include code or API examples if available.
If no example exists, omit this section.

Never mention retrieval, chunks, or internal system details.
"""
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ]

        )

        return response.choices[0].message.content
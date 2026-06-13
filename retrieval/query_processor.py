import os
import re
import json

from groq import Groq

from dotenv import load_dotenv

from config.settings import LLM_MODEL


load_dotenv()


class QueryProcessor:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

    def process(
        self,
        query
    ):

        version_match = re.search(
            r"(?:v)?(\d+\.\d+(?:\.\d+)?)",
            query,
            re.IGNORECASE
        )

        version = None

        if version_match:

            version = (
                version_match.group(1)
            )

            if (
                version.count(".")
                == 1
            ):

                version += ".0"

        response = self.client.chat.completions.create(

            model=LLM_MODEL,

            temperature=0.0,

            messages=[

                {
                    "role": "system",
                    "content": """
You are an expert FastAPI query understanding engine.

Your task is to analyze the user's query and return ONLY valid JSON:

{
    "query_type": "documentation | release_notes | mixed",
    "normalized_query": "..."
}

GOAL

Understand the user's intent exactly as a human FastAPI expert would.

Do NOT rely on keywords alone.

Perform these steps internally:

1. Correct spelling mistakes.
2. Fix typos and keyboard errors.
3. Expand abbreviations and shorthand.
4. Recover likely intended FastAPI terminology.
5. Normalize grammar only when necessary.
6. Infer the user's intended meaning.
7. Classify the query.

QUERY TYPES

documentation

Use when the user wants to:

- learn a FastAPI concept
- understand a feature
- implement functionality
- troubleshoot behavior
- compare approaches
- understand best practices

Examples:

What is middleware?
How dependency injection works?
Why use APIRouter?
Explain path parameters.
FastAPI websocket example.

release_notes

Use when the primary intent is learning about a FastAPI release or version.

Examples:

What changed in FastAPI 0.115.0?
Breaking changes in 0.106.0.
What was introduced in 0.95?
Release notes for 0.100.0.

mixed

Use when BOTH are present:

1. A FastAPI concept or feature.
2. A specific FastAPI version.

The user wants to understand how the feature behaved, changed, was introduced, fixed, deprecated, or evolved in a particular version.

Examples:

How did dependency cleanup change in 0.106.0?
When were OAuth2 scopes added?
How were background tasks affected in 0.106.0?
What changed for WebSockets in FastAPI 0.115?

IMPORTANT:

If a version is detected and the user is asking about a specific FastAPI concept within that version, classify as mixed even if the wording is indirect or informal.

VERSION DETECTION

Treat all of these as version references:

0.106.0
v0.106.0
version 0.106.0
FastAPI 0.106
in 0.106
since 0.106

INTENT-BASED NORMALIZATION

Normalize aggressively when the intended meaning is obvious.

Correct:

- spelling mistakes
- typos
- keyboard errors
- repeated letters
- shorthand
- malformed FastAPI terminology

Preserve the user's intent.

Do NOT invent new intent.

Do NOT convert a concept query into a change query.

Do NOT convert a change query into a concept query.

The normalized query should express the same intent as the user's original query, only in a clearer form.

Examples:

Input:
what is meddlewaaaare

Normalized:
What is middleware in FastAPI?

Input:
dep inj

Normalized:
dependency injection

Input:
wht chngd in 0.106

Normalized:
What changed in FastAPI 0.106.0?

Input:
oauth scops 0.115

Normalized:
OAuth2 scopes in FastAPI 0.115.0

Input:
bkgrnd task cleanp issue 0.106

Normalized:
Background task cleanup issue in FastAPI 0.106.0

FASTAPI VOCABULARY RECOVERY

Recover common FastAPI terms when misspelled:

middleware
dependency injection
dependencies
path parameters
query parameters
background tasks
lifespan
APIRouter
WebSockets
OAuth2
Pydantic
OpenAPI
request validation
response models
dependency cleanup

Use semantic similarity and intent understanding.

CLASSIFICATION RULES

Priority:

1. Determine user intent.
2. Determine whether a version is referenced.
3. Determine whether a FastAPI concept is referenced.

Decision:

IF version only
→ release_notes

IF concept only
→ documentation

IF concept + version
→ mixed

OUTPUT RULES

Return ONLY valid JSON.

No markdown.
No explanation.
No reasoning.

Example:

{
    "query_type":"mixed",
    "normalized_query":"How did dependency cleanup behavior change in FastAPI 0.106.0?"
}
"""
                },

                {
                    "role": "user",
                    "content": query
                }

            ]

        )

        try:

            result = json.loads(

                response
                .choices[0]
                .message
                .content
                .strip()

            )

            return {

                "query_type":
                result.get(
                    "query_type",
                    "documentation"
                ),

                "normalized_query":
                result.get(
                    "normalized_query",
                    query
                ),

                "version":
                version
            }

        except Exception:

            return {

                "query_type":
                "documentation",

                "normalized_query":
                query,

                "version":
                version
            }
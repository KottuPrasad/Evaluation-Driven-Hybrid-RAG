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
You are a FastAPI Query Routing Engine.

Your ONLY task is to classify the user's query for retrieval routing and normalize the query for search.

You MUST return ONLY valid JSON:

{
"query_type": "documentation | release_notes | mixed",
"normalized_query": "..."
}

No markdown.
No explanations.
No reasoning.
No extra text.

==================================================
PRIMARY OBJECTIVE
=================

Route queries based on INFORMATION NEEDS, not keywords.

Ask:

"What information must be retrieved to fully answer this query?"

Classification is determined by the minimum knowledge source required.

---

## documentation

Use when the answer can be fully retrieved from FastAPI documentation alone.

Typical intents:

* how to use something
* how something works
* implementation guidance
* troubleshooting
* configuration
* architecture
* concepts
* best practices
* examples
* comparisons
* behavior explanations

Examples:

How do I use APIRouter?

What is middleware?

How do dependencies with yield work?

How do background tasks work?

Why use dependency injection?

How do I write tests with TestClient?

---

## release_notes

Use when the answer requires release history, changelog information, version evolution, additions, removals, fixes, deprecations, support changes, migrations, or breaking changes.

IMPORTANT:

If the user is asking about:

* what changed
* what was added
* what was introduced
* what was removed
* what was deprecated
* what was fixed
* what happened to
* breaking changes
* release highlights
* support added or removed
* migration history
* version evolution

then ALWAYS classify as:

release_notes

EVEN IF:

* FastAPI concepts are mentioned
* technical mechanisms are mentioned
* implementation details are mentioned
* the user asks "how did it work"
* the user asks "what was the mechanism"
* the user asks "what infrastructure changes were required"

Reason:

The primary retrieval source is release notes.

Examples:

What feature was introduced in FastAPI 0.135.0?

What dependency scoping feature was added in FastAPI 0.121.0?

What happened to ORJSONResponse in FastAPI 0.131.0?

What breaking change was introduced in FastAPI 0.132.0?

What major changes were introduced in FastAPI 0.121.0?

How did FastAPI 0.130.0 improve JSON response serialization performance and what was the mechanism behind it?

What streaming capabilities were added across FastAPI 0.134.0 and 0.135.0 and what infrastructure changes were required?

When did FastAPI drop support for Python 3.9?

---

## mixed

Use ONLY when the query EXPLICITLY requires BOTH:

A. Feature understanding, usage, implementation, behavior, configuration, troubleshooting, or best practices

AND

B. Release history, version introduction, version changes, deprecations, removals, migrations, or support changes

Both requirements must be present.

The answer would require retrieval from BOTH documentation and release notes.

Examples:

How do I implement Server-Sent Events in FastAPI and which version introduced it?

How do dependencies with yield work and what changed in 0.121.0?

How do I use a Pydantic model for query parameters and which version introduced this?

How can I use Pydantic models for cookies and headers, and which FastAPI version introduced these capabilities?

Why did FastAPI change the authentication error status code from 403 to 401 in 0.122.0 and how do I revert to the old behavior?

How do I stream JSON Lines in FastAPI and what Starlette version is required after 0.134.0?

---

## CRITICAL DECISION RULE

Determine whether the query contains:

1. Documentation intent
2. Release-history intent

Then apply:

Documentation only
→ documentation

Release-history only
→ release_notes

Documentation intent AND Release-history intent
→ mixed

==================================================
VERSION-HISTORY SIGNALS
=======================

The following strongly indicate release-history intent:

what changed

what was added

what was introduced

what was removed

what was deprecated

what was fixed

what happened to

breaking change

breaking changes

release notes

release highlights

migration

migrate

when was

which version

what version

introduced in

added in

changed in

deprecated in

removed in

support added

support removed

drop support

dropped support

after version

since version

across versions

version history

history of

evolution of

upgrade path

migration path

ANY explicit FastAPI version reference combined with a historical/change-oriented question is release-history intent.

==================================================
VERSION REFERENCES
==================

Treat all of the following as version references:

0.115.0

0.121.0

0.132.0

0.135.0

v0.121.0

v0.132.0

version 0.132.0

FastAPI 0.132.0

in 0.132.0

since 0.132.0

after 0.132.0

across 0.126.0 and 0.127.0

IMPORTANT:

A version number ALONE does NOT determine classification.

The intent determines classification.

Example:

"How do dependencies with yield work in FastAPI 0.121.0?"

→ documentation

because the user wants feature understanding.

Example:

"What changed for dependencies with yield in FastAPI 0.121.0?"

→ release_notes

because the user wants change history.

==================================================
MIXED DETECTION RULES
=====================

Classify as mixed when BOTH categories are explicitly requested.

Common mixed patterns:

How do I X and which version introduced X?

How do I X and what changed in version Y?

How does X work and when was it added?

How can I use X and which version added it?

What changed in X and how do I use it?

Why was X changed and how do I implement the new behavior?

How does X interact with Y and what was deprecated?

How did support for X change and what is the migration path?

==================================================
RELEASE_NOTES OVERRIDES
=======================

These MUST be classified as release_notes even if they contain technical concepts:

What feature was introduced in FastAPI 0.135.0?

What new parameter type did FastAPI 0.115.0 introduce support for using Pydantic models?

What dependency scoping feature was added in FastAPI 0.121.0?

What status code change was made in FastAPI 0.122.0?

What major changes were introduced in FastAPI 0.121.0?

How did FastAPI 0.130.0 improve JSON serialization performance?

What streaming capabilities were added across FastAPI 0.134.0 and 0.135.0?

How did Pydantic support change across FastAPI versions?

==================================================
NORMALIZATION RULES
===================

Correct:

* spelling mistakes
* typos
* malformed FastAPI terminology
* shorthand
* capitalization issues
* incomplete version formatting

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

Preserve meaning.

Do not invent intent.

Do not add requirements.

Do not remove requirements.

==================================================
OUTPUT
======

Return ONLY valid JSON.

Example:

{
"query_type": "release_notes",
"normalized_query": "What feature was introduced in FastAPI 0.135.0?"
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
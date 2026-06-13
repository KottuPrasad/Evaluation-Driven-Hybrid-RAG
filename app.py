from flask import (
    Flask,
    request,
    jsonify
)

from flask_cors import (
    CORS
)

from rag_pipeline import (
    RAGPipeline
)


app = Flask(
    __name__
)

CORS(app)

pipeline = (
    RAGPipeline()
)


@app.route(
    "/"
)
def home():

    return {

        "status":
        "running"
    }


@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    data = (
        request.get_json()
    )

    query = (
        data.get(
            "query",
            ""
        )
    )

    result = (
        pipeline.ask(
            query
        )
    )

    return jsonify(
        result
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )
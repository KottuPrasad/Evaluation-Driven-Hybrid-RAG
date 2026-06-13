import { useState } from "react";
import axios from "axios";

function App() {

  const [query, setQuery] = useState("");

  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([]);

  const sendQuery = async () => {

    if (!query.trim()) return;

    const userMessage = {
      role: "user",
      content: query
    };

    setMessages(prev => [
      ...prev,
      userMessage
    ]);

    const currentQuery = query;

    setQuery("");

    setLoading(true);

    try {

      const response = await axios.post(
        "http://127.0.0.1:5000/chat",
        {
          query: currentQuery
        }
      );

      const assistantMessage = {

        role: "assistant",

        content:
          response.data.answer,

        metadata: {

          query_type:
            response.data.query_type,

          route:
            response.data.route,

          version:
            response.data.version,

          normalized_query:
            response.data.normalized_query,

          sources:
            response.data.sources
        }
      };

      setMessages(prev => [
        ...prev,
        assistantMessage
      ]);

    } catch (error) {

      setMessages(prev => [

        ...prev,

        {
          role: "assistant",
          content:
            "Error connecting to backend."
        }

      ]);
    }

    setLoading(false);
  };

  return (

    <div
      style={{
        maxWidth: "1200px",
        margin: "0 auto",
        padding: "20px"
      }}
    >

      <h1
        style={{
          textAlign: "center"
        }}
      >
        FastAPI Documentation Assistant
      </h1>

      <p
        style={{
          textAlign: "center",
          color: "gray"
        }}
      >
        Evaluation-Driven Hybrid RAG System
      </p>

      <div
        style={{
          height: "70vh",
          overflowY: "auto",
          border: "1px solid #333",
          padding: "20px",
          borderRadius: "10px",
          marginBottom: "20px"
        }}
      >

        {messages.map((message, index) => (

          <div
            key={index}
            style={{
              marginBottom: "25px"
            }}
          >

            <div
              style={{
                background:
                  message.role === "user"
                    ? "#2563eb"
                    : "#1f2937",

                padding: "15px",

                borderRadius: "10px",

                textAlign:
                  message.role === "user"
                    ? "right"
                    : "left"
              }}
            >

              {message.content}

            </div>

            {message.role === "assistant" &&
              message.metadata && (

                <>

                  <div
                    style={{
                      marginTop: "10px",
                      padding: "10px",
                      border:
                        "1px solid #444",
                      borderRadius: "10px"
                    }}
                  >

                    <h4>
                      Query Analysis
                    </h4>

                    <p>
                      <strong>
                        Query Type:
                      </strong>{" "}
                      {
                        message.metadata
                          .query_type
                      }
                    </p>

                    <p>
                      <strong>
                        Route:
                      </strong>{" "}
                      {
                        message.metadata
                          .route
                      }
                    </p>

                    <p>
                      <strong>
                        Version:
                      </strong>{" "}
                      {
                        message.metadata
                          .version ||
                        "N/A"
                      }
                    </p>

                    <p>
                      <strong>
                        Normalized:
                      </strong>{" "}
                      {
                        message.metadata
                          .normalized_query
                      }
                    </p>

                  </div>

                  <div
                    style={{
                      marginTop: "10px",
                      padding: "10px",
                      border:
                        "1px solid #444",
                      borderRadius: "10px"
                    }}
                  >

                    <h4>
                      Sources Used
                    </h4>

                    {
                      message.metadata
                        .sources?.map(
                          (
                            source,
                            idx
                          ) => (

                            <div
                              key={idx}
                              style={{
                                marginBottom:
                                  "10px"
                              }}
                            >

                              <strong>
                                {
                                  source.title
                                }
                              </strong>

                              <br />

                              {
                                source.section
                              }

                            </div>

                          )
                        )
                    }

                  </div>

                </>

              )}

          </div>

        ))}

        {loading && (

          <div
            style={{
              padding: "15px"
            }}
          >

            Thinking...

          </div>

        )}

      </div>

      <div
        style={{
          display: "flex",
          gap: "10px"
        }}
      >

        <input
          type="text"
          value={query}
          onChange={(e) =>
            setQuery(
              e.target.value
            )
          }
          placeholder="Ask a FastAPI question..."
          style={{
            flex: 1,
            padding: "12px"
          }}
          onKeyDown={(e) => {

            if (
              e.key === "Enter"
            ) {

              sendQuery();
            }
          }}
        />

        <button
          onClick={sendQuery}
        >
          Send
        </button>

      </div>

    </div>
  );
}

export default App;
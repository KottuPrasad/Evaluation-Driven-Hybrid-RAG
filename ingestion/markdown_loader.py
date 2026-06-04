from pathlib import Path


class MarkdownLoader:

    def __init__(self, docs_path):

        self.docs_path = docs_path

    def load_documents(self):

        documents = []

        markdown_files = Path(self.docs_path).rglob("*.md")

        for file_path in markdown_files:

            try:

                with open(file_path, "r", encoding="utf-8") as file:

                    content = file.read()

                documents.append({

                    "file_name": file_path.name,

                    "file_path": str(file_path),

                    "content": content

                })

            except Exception as e:

                print(f"Error reading {file_path}")

                print(e)

        return documents
import re


class Chunker:

    def create_chunks(self, documents):

        structure_chunks = []

        chunk_id = 1

        for document in documents:

            file_name = document["file_name"]

            content = document["content"]

            title = ""

            section = ""

            subsection = ""

            current_text = []

            lines = content.split("\n")

            inside_code_block = False

            for line in lines:

                line = line.strip()

                if line.startswith("```"):

                    current_text.append(line)

                    inside_code_block = not inside_code_block

                    continue

                if inside_code_block:

                    current_text.append(line)

                    continue

                if not line:

                    continue

                if line.startswith("# ") and not line.startswith("##"):

                    if current_text:

                        structure_chunks.append({
                            "chunk_id": chunk_id,
                            "file_name": file_name,
                            "title": title,
                            "section": section,
                            "subsection": subsection,
                            "text": "\n".join(current_text)
                        })

                        chunk_id += 1

                        current_text = []

                    title = re.sub(
                        r"\s*\{.*?\}",
                        "",
                        line[2:]
                    ).strip()

                elif line.startswith("## ") and not line.startswith("###"):

                    if current_text:

                        structure_chunks.append({
                            "chunk_id": chunk_id,
                            "file_name": file_name,
                            "title": title,
                            "section": section,
                            "subsection": subsection,
                            "text": "\n".join(current_text)
                        })

                        chunk_id += 1

                        current_text = []

                    section = re.sub(
                        r"\s*\{.*?\}",
                        "",
                        line[3:]
                    ).strip()

                    subsection = ""

                elif line.startswith("### "):

                    if current_text:

                        structure_chunks.append({
                            "chunk_id": chunk_id,
                            "file_name": file_name,
                            "title": title,
                            "section": section,
                            "subsection": subsection,
                            "text": "\n".join(current_text)
                        })

                        chunk_id += 1

                        current_text = []

                    subsection = re.sub(
                        r"\s*\{.*?\}",
                        "",
                        line[4:]
                    ).strip()

                else:

                    current_text.append(line)

            if current_text:

                structure_chunks.append({
                    "chunk_id": chunk_id,
                    "file_name": file_name,
                    "title": title,
                    "section": section,
                    "subsection": subsection,
                    "text": "\n".join(current_text)
                })

                chunk_id += 1

        final_chunks = []

        new_chunk_id = 1

        for chunk in structure_chunks:

            words = chunk["text"].split()

            if len(words) <= 500:

                final_chunks.append({
                    "chunk_id": str(new_chunk_id),
                    "file_name": chunk["file_name"],
                    "title": chunk["title"],
                    "section": chunk["section"],
                    "subsection": chunk["subsection"],
                    "text": chunk["text"]
                })

                new_chunk_id += 1

                continue

            start = 0

            part_number = 1

            while start < len(words):

                end = start + 500

                split_text = " ".join(words[start:end])

                final_chunks.append({
                    "chunk_id": f"{new_chunk_id}_{part_number}",
                    "file_name": chunk["file_name"],
                    "title": chunk["title"],
                    "section": chunk["section"],
                    "subsection": chunk["subsection"],
                    "text": split_text
                })

                part_number += 1

                start += 450

            new_chunk_id += 1

        return final_chunks
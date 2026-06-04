import re


class MarkdownCleaner:

    def clean(self, text):

        lines = text.split("\n")

        cleaned_lines = []

        skip_tab_block = False

        for line in lines:

            stripped = line.strip()

            # -------------------------
            # REMOVE HTML COMMENTS
            # -------------------------
            if stripped.startswith("<!--"):
                continue

            # -------------------------
            # REMOVE TAB DIRECTIVES
            # -------------------------
            if stripped.startswith("//// tab"):
                continue

            # -------------------------
            # REMOVE EMPTY TAB MARKERS
            # -------------------------
            if stripped == "////":
                continue

            # -------------------------
            # NORMAL LINE
            # -------------------------
            cleaned_lines.append(line)

        cleaned_text = "\n".join(cleaned_lines)

        return cleaned_text
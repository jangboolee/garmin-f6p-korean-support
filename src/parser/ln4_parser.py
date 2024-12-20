from pathlib import Path


class Ln4Parser:

    def __init__(self, language: str) -> None:

        self.language = language
        # Use headers for ukrainia.ln4
        self.header = "006-D7752-35|v04.70"
        # Generate file path for the ln4 file to parse
        base_path = Path(".") / "files" / "ln4" / "f6p" / "original"
        self.file_path = base_path / f"{self.language}.ln4"
        self.parsed = {}

    def parse_file(self) -> int:
        """Parse the contents of an ln4 file as a dictionary

        Returns:
            int: Count of items parsed
        """

        # Read contents of ln4 file as raw strings
        with open(self.file_path, "r", encoding="utf-8") as f:
            f_contents = [line.rstrip() for line in f.readlines()]

        # Parse out hexadecimal key and translation values
        for i in range(1, len(f_contents)):  # Skip first header line
            # Separate key and value per line
            line_content = f_contents[i]
            key, value = line_content[:8], line_content[9:]
            # Add as key-value pairs to dictionary
            self.parsed[key] = value

        parsed_count = len(self.parsed.keys())

        # Print results of parsing
        print(f"Parsed {parsed_count} items")

        return parsed_count

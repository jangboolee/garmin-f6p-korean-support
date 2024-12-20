from pathlib import Path
from csv import DictReader


class Ln4Parser:

    def __init__(self, language: str, is_epix: bool = False) -> None:

        self.language = language
        # Use headers for ukrainia.ln4
        self.header = "006-D7752-35|v04.70"
        # Generate file path for the ln4 file to parse
        if is_epix:
            base_path = Path(".") / "files" / "ln4" / "epix"
        else:
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
            # Ignore seemingly incorrect item only found in Ukrainian file
            if key == "ст-но %1":
                continue
            # Add as key-value pairs to dictionary
            self.parsed[key] = value

        parsed_count = len(self.parsed.keys())

        # Print results of parsing
        print(f"Parsed {parsed_count} items")

        return parsed_count

    def get_value(self, key: str) -> str:
        """Getter method to get the value of a given key

        Args:
            key (str): Hexadecmial key to use for lookup

        Returns:
            str: The value of the key if found, None if not
        """

        return self.parsed.get(key, None)

    def export_file(self) -> bool:
        """Method to export a LN4 file based on manual translations

        Returns:
            bool: True after completion
        """

        read_path = Path(".") / "files" / "kr_translated.csv"

        # Read manual Korean translation results
        f = open(read_path, encoding="utf-8-sig")
        reader = DictReader(f)

        base_path = Path(".") / "files" / "ln4" / "f6p" / "modified"
        write_path = base_path / f"{self.language}.ln4"

        with open(write_path, "w", encoding="utf-8") as f:
            # Write header
            f.write(self.header + "\n")
            # Convert each key-value pair to a single string
            lines = [f"{line['key']} {line['KR']}\n" for line in reader]
            # Write all items
            f.writelines(lines)

        f.close()

        return True


parser = Ln4Parser("ukrainia")
parser.export_file()

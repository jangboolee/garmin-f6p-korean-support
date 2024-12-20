from pathlib import Path

import pandas as pd

from src.parser.ln4_parser import Ln4Parser


def parse_files() -> tuple[Ln4Parser]:

    # Instantiate custom parsers for two Fenix 6 Pro European ln4 files
    ua = Ln4Parser("ukrainia")
    nl = Ln4Parser("dutch")
    # Instantiate custom parser for Epix Korean ln4 file
    kr = Ln4Parser(language="korean", is_epix=True)

    # Use parser to parse each file
    ua.parse_file()
    nl.parse_file()
    kr.parse_file()

    return ua, nl, kr


def map_epix_to_fenix(
    ua: Ln4Parser, nl: Ln4Parser, kr: Ln4Parser
) -> dict[str, str]:

    # Get unique list of Fenix 6 Pro items from Ukranian and Dutch files
    all_fenix = list(ua.parsed.keys())
    for nl_item in nl.parsed.keys():
        if nl_item not in all_fenix:
            all_fenix.append(nl_item)

    # Map as many Korean items as possible from Epix ln4 file
    mapped_fenix = {}
    none_count = 0

    for fenix_item in all_fenix:
        epix_value = kr.get_value(fenix_item)
        if epix_value:
            mapped_fenix[fenix_item] = epix_value
        else:
            mapped_fenix[fenix_item] = None
            none_count += 1

    # Calculate statistics of mapping results
    total = len(mapped_fenix.keys())
    mapped_count = total - none_count
    mapped_per = mapped_count / total * 100

    print(f"{mapped_per:.1f}% item(s) mapped. {none_count} item(s) missing.")

    return mapped_fenix


def get_dutch_missing_items(mapped: dict[str, str], nl: Ln4Parser):

    # Create dictionary of F6P keys missing Epix Korean translations
    missing = {k: None for k, v in mapped.items() if v is None}

    # Get F6P Dutch translations for F6P keys missing translations
    none_count = 0
    for k in missing.keys():
        dutch_value = nl.get_value(k)
        if dutch_value:
            missing[k] = dutch_value
        else:
            missing[k] = None
            none_count += 1

    # Calculate statistics of mapping results
    total = len(missing.keys())
    mapped_count = total - none_count
    mapped_per = mapped_count / total * 100

    print(f"{mapped_per:.1f}% item(s) mapped. {none_count} item(s) missing.")

    return missing


def export_csv(epix_mapped: dict, nl_mapped: dict):

    # Combine Korean mapping from Epix and Dutch mapping from F6P into a
    # single dataframe
    to_write = []
    for key, kr_mapping in epix_mapped.items():
        if kr_mapping:
            to_write.append((key, kr_mapping, None))
        else:
            dutch_value = nl_mapped.get(key, None)
            if dutch_value:
                to_write.append((key, None, dutch_value))
            else:
                to_write.append((key, None, None))

    df = pd.DataFrame(data=to_write, columns=["key", "KR", "NL"])

    # Export results to a CSV file
    file_path = Path(".") / "files" / "output" / "ln4_mapped.csv"
    df.to_csv(file_path, encoding="utf-8-sig")


def main():

    ua_parser, nl_parser, kr_parser = parse_files()
    kr_mapped = map_epix_to_fenix(ua_parser, nl_parser, kr_parser)
    kr_nl_mapped = get_dutch_missing_items(kr_mapped, nl_parser)
    export_csv(kr_mapped, kr_nl_mapped)
    pass


if __name__ == "__main__":

    main()

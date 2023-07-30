import pandas as pd
import os


def open_outfile(filename: str) -> pd.DataFrame:
    """Open json outfile data as pandas dataframe."""
    json_path = os.path.join(os.getcwd(), "backend", "json", f"{filename}.json")
    df = pd.read_json(json_path)
    return df


def create_outfile(data: pd.DataFrame, filename: str) -> None:
    """Serialize a pandas dataframe in JSON format and save in ".\\backend\\json" directory."""
    serialized_json = data.to_json()
    outfile_path = os.path.join(os.getcwd(), "backend", "json", f"{filename}.json")

    with open(outfile_path, "w") as outfile:
        outfile.write(serialized_json)

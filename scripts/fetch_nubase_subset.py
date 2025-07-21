import pandas as pd
import requests


def fetch_nubase_subset():
    url = "https://www-nds.iaea.org/nubase/nubase2020.csv"
    response = requests.get(url)
    response.raise_for_status()

    # Load CSV into DataFrame
    df = pd.read_csv(pd.compat.StringIO(response.text))

    # Filter relevant columns
    columns = [
        "Z",
        "N",
        "Symbol",
        "A",
        "HalfLife",
        "BindingEnergyMeV",
        "QαMeV",
        "QβMeV",
        "IsStable",
    ]
    df = df[columns]

    # Save to isotopes.csv
    df.to_csv("examples/periodic_table/isotopes.csv", index=False)


if __name__ == "__main__":
    fetch_nubase_subset()

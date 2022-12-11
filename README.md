## Parser for ICA recipts

As ICA customer, you have the ability to access the receipt through Kivra.
However the data is presented in a PDF file. The parser in this repocitorie will
help extract the useful information from the receipt for further analysis. It
will create a dictionary the receipt with the useful information. Example of
such data object:

``` json
{
    "id": "4400244203032182061123224",
    "store_name": "ICA Karlskrona Cityhallen",
    "product_columns": [
        "Beskrivning",
        "Art. nr.",
        "Pris",
        "Mängd",
        "Summa(SEK)"
    ],
    "products": [
        [
            "Banan Eko",
            "94232",
            27.95,
            "1.09 kg",
            30.47
        ],
        [
            "Mellanmjölk",
            "7310865001818",
            19.9,
            "1 st",
            19.9
        ]
    ],
    "date": "2022-11-23",
    "total": 50.37
}
```

This object can be converted to a dataframe in the following way:
``` python
def to_csv(receipt: dict) -> pd.DataFrame:

    df = pd.DataFrame(
        columns=receipt['product_columns'],
        data=receipt['products']
    )

    df['date'] = [receipt['date']]*len(df)
    df['store_name'] = [receipt['store_name']]*len(df)
    return df
```

Running `main.py` the first time will create two folders, `parsed` and
`unparsed`. It will also create a `database.json` file. When the main program is
executed the second time, pdf files will be read from unparsed, saved to
database.json and moved to parsed.

---
## Applications
This data can be used to track prices over time. It could also be used to gain
more insight in your every day shopping. 
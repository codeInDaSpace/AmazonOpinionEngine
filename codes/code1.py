import pandas as pd
import os
import re

def cleanTxt(text):
    if not isinstance(text, str):
        return ""
    text = text.replace("\\'", "'")
    text = text.strip("'")
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("\\n", " ")
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def test(df, queries):
    results = {}
    for key in queries:
        aWord, oWord = queries[key]
        aWordSet = set(aWord)

        test1 = df["tokens_set"].apply(lambda tokens: len(tokens.intersection(aWordSet)) > 0)
        test2 = df["tokens_set"].apply(lambda tokens: (len(tokens.intersection(aWordSet)) > 0) and any(word in tokens for word in oWord))
        test3 = df["tokens_set"].apply(lambda tokens: (len(tokens.intersection(aWordSet)) > 0) or any(word in tokens for word in oWord))

        results[key] = {
            1: df.loc[test1, "review_id"].tolist(),
            2: df.loc[test2, "review_id"].tolist(),
            3: df.loc[test3, "review_id"].tolist()
        }
    return results

def main():
    df = pd.read_pickle("pythonFolder/reviews_segment.pkl")
    df["clean_text"] = df["review_text"].apply(cleanTxt)
    df["tokens_set"] = df["clean_text"].str.split().apply(set)

    queries = {
        "audio quality": (["audio","quality"], ["poor"]),
        "wifi signal": (["wifi","signal"], ["strong"]),
        "mouse button": (["mouse", "button"], ["click", "problem"]),
        "gps map": (["gps","map"], ["useful"]),
        "image quality": (["image","quality"], ["sharp"]),
    }

    results = test(df, queries)

    for q, t in results.items():
        print(f"Results for '{q}':")
        for i, ids in t.items():
            print(f" Test {i} found {len(ids)} reviews.")
        print()

  
    """
    directory = "../outputs/baseline"

    for a, t in results.items():
        aFile = a.replace(" ", "_")
        for i, ids in t.items():
            filename = f"{aFile}_test{i}.txt"
            filepath = os.path.join(directory, filename)
            with open(filepath, "w") as f:
                for r in ids:
                    f.write(f"{r}\n")
    """
    
if __name__ == "__main__":
    main()

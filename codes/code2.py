import pandas as pd
from code1 import cleanTxt 
import os

def proximity(tokens, aWord, oWord, maxi=5):
    aPos = [i for i, token in enumerate(tokens) if token in aWord]
    oPos = [i for i, token in enumerate(tokens) if token in oWord]

    i, j = 0, 0
    while i < len(aPos) and j < len(oPos):
        aCur = aPos[i]
        oCur = oPos[j]
        if abs(aCur - oCur) <= maxi:
            return True
        if aCur < oCur:
            i += 1
        else:
            j += 1
    return False

def sentiment(tokens,aWord,oWord,rating,maxi=5):
    posOp = {"strong","useful","sharp"}
    negOp = {"poor","problem","click"}

    aPos = [i for i, token in enumerate(tokens) if token in aWord]
    oPos = [i for i, token in enumerate(tokens) if token in oWord]

    rating = int(rating)

    i, j = 0, 0
    while i < len(aPos) and j < len(oPos):
        aCur = aPos[i]
        oCur = oPos[j]
        dist = abs(aCur - oCur)
        if dist <= maxi:
            oSent = tokens[oCur]
            if oSent in posOp and rating >= 4:
                return True
            if oSent in negOp and rating <= 2:
                return True
   
        if aCur < oCur:
            i += 1
        else:
            j += 1
    
    return False

        
def main():
    df = pd.read_pickle("pythonFolder/reviews_segment.pkl")
    df["clean_text"] = df["review_text"].apply(cleanTxt)
    df["tokens_list"] = df["clean_text"].str.split()
    
    queries = {
        "audio quality": (["audio", "quality"], ["poor"]),
        "wifi signal": (["wifi", "signal"], ["strong"]),
        "mouse button": (["mouse", "button"], ["click", "problem"]),
        "gps map": (["gps", "map"], ["useful"]),
        "image quality": (["image", "quality"], ["sharp"]),
    }

    results = {}

    for key in queries:
        aWord, oWord = queries[key]

        proxTest = df["tokens_list"].apply(lambda tokens: proximity(tokens, aWord, oWord))
        proxResults = df.loc[proxTest, "review_id"].tolist()

        sentTest = df.apply(lambda row: sentiment(row["tokens_list"],aWord,oWord,row["customer_review_rating"]), axis=1)
        sentResults = df.loc[sentTest, "review_id"].tolist()

        results[key] = {
            "method1": proxResults,
            "method2": sentResults            
                        }


    for q, m in results.items():
        print(f"Results for '{q}':")
        for i, ids in m.items():
            print(f" {i} found {len(ids)} reviews.")
        print()
   
    """
    base = "../outputs"
    metDir = {
        "method1": os.path.join(base,"method1"),
        "method2": os.path.join(base,"method2")
    }

    for a,m in results.items():
        aFile = a.replace(" ","_")
        for i,ids in m.items():
            filename = f"{aFile}_test{4}.txt"
            filepath = os.path.join(metDir[i],filename)
        
            with open(filepath, "w") as f:
                for r in ids:
                    f.write(f"{r}\n")

    """

if __name__ == "__main__":
    main()

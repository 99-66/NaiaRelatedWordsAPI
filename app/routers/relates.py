from fastapi import APIRouter, HTTPException
from app.core.database import els_connector
from app.core.analyzer.related_words import word_network

router = APIRouter()


@router.get("/related/{word}", tags=["related"])
def related_words(word: str):
    df = els_connector.get_related_words(word)

    if df.empty:
        raise HTTPException(status_code=404, detail="not found")

    try:
        res = word_network(df)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    else:
        return {
            "code": 200,
            "message": res
        }


@router.get("/related/list/{word}", tags=["related"])
def related_list(word: str):
    if not word:
        raise HTTPException(status_code=400, detail="bad request")

    df = els_connector.get_related_tweets(word)

    if df.empty:
        raise HTTPException(status_code=404, detail="not found")
    try:
        res = df.to_dict(orient='records')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    else:
        return {
            "code": 200,
            "message": res
        }
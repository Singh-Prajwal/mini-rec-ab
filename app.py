from fastapi import FastAPI, Request
from rec_engine import MiniRec
from ab import choose_variant, log_event

rec = MiniRec("data/movies.csv")
app = FastAPI()

@app.get("/recommend")
async def recommend(request: Request, q: str):
    variant = choose_variant(request)

    # Variant logic: same engine, different 'k'
    k = 3 if variant == "A" else 5
    results = rec.recommend(q, k=k)

    log_event(request.client.host, variant, q)
    response = {"variant": variant, "results": results}
    # Persist variant in cookie for consistency
    from fastapi.responses import JSONResponse
    resp = JSONResponse(content=response)
    resp.set_cookie("variant", variant)
    return resp
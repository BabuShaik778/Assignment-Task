
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
import uvicorn
import os
from .auth import create_access_token, verify_token
from .rate_limiter import token_bucket, get_redis
from .cache import cache_response
from .logging_config import logger

app = FastAPI(title="HighPerf API Gateway")

@app.on_event("startup")
async def startup():
    await get_redis()
    logger.info("startup complete")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/token")
def token():
    # Demo token endpoint: in real world, validate creds
    token = create_access_token({"sub": "test-user"})
    logger.info("token issued")
    return {"access_token": token, "token_type": "bearer"}

@app.get("/proxy/data")
async def proxy_data(request: Request, _ = Depends(token_bucket), payload=Depends(verify_token)):
    """
    Example proxied endpoint: protected + rate-limited
    Cache frequent expensive responses
    """
    # simple cached expensive operation
    @cache_response(ttl=60, key_builder=lambda *a, **k: "cache:proxy_data:v1")
    async def expensive():
        # simulate CPU/IO work; in real, call backend microservice
        return {"items": list(range(1000)), "note": "generated"}

    result = await expensive()
    logger.info("served /proxy/data", extra={"cached": result["cached"]})
    return JSONResponse(result["data"])

# open test endpoint (no auth)
@app.get("/public")
async def public():
    return {"msg": "public endpoint"}

if __name__ == "__main__":
    workers = int(os.getenv("WORKERS", "4"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, workers=workers)



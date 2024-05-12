from fastapi import Header, HTTPException

async def token_authenticator(token: str = Header(None)):
    if not token or token != "secret-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token
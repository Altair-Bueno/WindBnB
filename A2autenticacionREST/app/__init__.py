from fastapi import Depends, FastAPI, Response, status
from fastapi.security import HTTPBearer
from .utils import VerifyToken 


# Scheme for the Authorization header
token_auth_scheme = HTTPBearer()
 
# Creates app instance
app = FastAPI()

@app.get("/validate")
def private(response: Response, token: str = Depends(token_auth_scheme)):  
    """A valid access token is required to access this route"""
    print(response)
    print(token.credentials)


    result = VerifyToken(bytes(token.credentials.encode("utf-8")))
    print(result)

    if result.get("status"):
       response.status_code = status.HTTP_400_BAD_REQUEST
       return result
 
    return result
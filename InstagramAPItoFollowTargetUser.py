from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, UserNotFound, PleaseWaitFewMinutes
import uvicorn

app = FastAPI(title="Instagram Follow API", description="API to follow Instagram users using instagrapi")


@app.get("/instagram")
def follow_user(
    sessionid: str = Query(..., description="Instagram sessionid cookie"),
    id: str = Query(..., description="Instagram user id or username")
):
    try:
        cl = Client()
        cl.login_by_sessionid(sessionid)

        # If user provided username instead of pk/id
        if id.isdigit():
            user_id = int(id)
        else:
            user_id = cl.user_id_from_username(id)

        result = cl.user_follow(user_id)

        return JSONResponse({
            "status": "success",
            "message": f"Followed user {id}",
            "user_id": user_id,
            "result": result
        })

    except LoginRequired:
        return JSONResponse({"status": "error", "message": "Invalid sessionid, login required"}, status_code=401)
    except UserNotFound:
        return JSONResponse({"status": "error", "message": "User not found"}, status_code=404)
    except PleaseWaitFewMinutes:
        return JSONResponse({"status": "error", "message": "Rate limited by Instagram, please wait"}, status_code=429)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import APIRouter

# router instance
router = APIRouter()

@router.get("/hello")
def test():
	return {"massage": "hi from ai!"}
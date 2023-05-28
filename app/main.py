from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ai 

from fastapi.responses import UJSONResponse

# create fast-api instance
app = FastAPI(default_response_class=UJSONResponse)

# cors settings
origins = [
    '*',
]

# middleware settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register router
app.include_router(ai.router)
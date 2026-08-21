from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth import router
import asyncpg
# import asyncio

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# async def root():
#     return {"message": "Hello World!"}



app.include_router(router, prefix="/auth", tags=["auth"])

# async def get_db_connection():


#     db_config = {
#         "user": "cloudhopper",
#         "password": "password",
#         "database": "cloudhopper",
#         "host": "localhost",
#         "port": 5432,
#     }

#     return await asyncpg.connect(
#             user=db_config["user"],
#             password=db_config["password"],
#             database=db_config["database"],
#             host=db_config["host"],
#             port=db_config["port"],
#         )


# @app.post("/login/{username}/{password}")
# async def login(username: str, password: str):
#     # Placeholder for login logic
#     # In a Database - user_table1 --> user_id, user_name, user_password

#     connection = await get_db_connection()

#     try :
#         query = 'SELECT * FROM user_data1 WHERE user_name = $1 AND user_password = $2'
#         result = await connection.fetchrow(query, username, password)

#     finally:
#         await connection.close()

#     if result is None:
#         raise HTTPException(status_code=401, detail="Invalid username or password")
#     return {"message": "Login successful!"}


# listening to server on port 8000

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="localhost", port=4000)
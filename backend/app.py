"""
last change: 24.06.2024
author: Vincent Guttmann

description: api application for the chatbot
"""

from datetime import datetime
import json
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from BotSession import BotSession

# create fastapi instance
app = FastAPI(
  title="IT-Project Knowledge-DB API",
  version="0.1.0"
)

# edit middleware to allow connections
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# store sessions
sessions: dict[int, BotSession] = {}

# returns welcome message
@app.get("/")
async def root():
  return BotSession.greet()

# returns an unique session id
@app.get("/sid")
async def create_sid():
  session = BotSession()
  sessions[session.sid] = session
  return session.sid

# returns current time
@app.get("/time")
async def get_time():
  return datetime.strftime(datetime.now(), "%H:%M")

# returns the answer to a text of a session
@app.get("/compute/{sid}/{text}")
async def compute_text(sid: int, text: str):
  if sid in sessions:
    return sessions[sid].generate_answer(text + " ")
  else:
    session = BotSession()
    sessions[sid] = session
    return compute_text()

# returns the complete evaluation of a session
@app.get("/evaluation/{sid}")
async def get_evaluation(sid: int):
  if sid in sessions.keys():
    return json.dumps(sessions[sid].evaluation)
  else:
    return []

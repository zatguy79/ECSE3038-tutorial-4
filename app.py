from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Device(BaseModel):
    name: str
    room: str
    temp: float
    online: bool


readings = [
    {"name": "front-door", "room": "hall",    "temp": 27.4, "online": True},
    {"name": "hall-lamp",  "room": "hall",    "temp": 26.1, "online": True},
    {"name": "attic",      "room": "attic",   "temp": 31.9, "online": True},
    {"name": "fridge",     "room": "kitchen", "temp": 4.2,  "online": False},
    {"name": "patio",      "room": "outside", "temp": 29.8, "online": True},
]


@app.get("/devices")
def get_devices():
    return readings


@app.get("/devices/{name}")
def get_device(name: str):
    for device in readings:
        if device["name"] == name:
            return device
    raise HTTPException(status_code=404, detail="No device called " + name)


@app.post("/devices", status_code=201)
def create_device(device: Device):
    new_device = device.model_dump()
    readings.append(new_device)
    return new_device

@app.put("/devices/{name}")
def put_device(name: str, updated_device: Device):
    for index, device in enumerate(readings):   #enumerate means u get the index of readings along with the device
        if device["name"] == name:                 #device["name"] doesn't work as it isn't a dictionary
            readings[index] = updated_device.model_dump()   #.model_dump() changes it to a dictionary
            return readings[index]
    raise HTTPException(status_code=404, detail="No device called " + name)

from typing import List

from fastapi import FastAPI, HTTPException
from starlette import status
from sqlalchemy import func
from session import session as session_
from datetime import datetime, timedelta
import models as models_
import random
from models import *

app = FastAPI()

console_flag = False


# CRUD operations for Satellite
@app.post("/satellites/", tags=["satellite"])
async def create_satellite(title: str = "",
                            country: str = "",
                            expire_date: datetime = datetime.utcnow(),
                            orbit_radius: float = 0.0):
    satellite = Satellite(title=title, country=country, expireDate=expire_date, orbitRadius=orbit_radius)
    session_.add(satellite)
    session_.commit()
    session_.refresh(satellite)
    return f"Satellite successfully created. SatelliteID: {satellite.satelliteId}, Title: {satellite.title}."

@app.get("/satellites/{satellite_id}", tags=["satellite"])
async def read_satellite(satellite_id: int):
    satellite = session_.query(Satellite).filter(Satellite.satelliteId == satellite_id).first()
    if satellite is None:
        raise HTTPException(status_code=404, detail="Satellite not found")
    return satellite

@app.get("/satellites/", tags=["satellite"])
async def read_satellites(skip: int = 0, limit: int = 10):
    satellites = session_.query(Satellite).offset(skip).limit(limit).all()
    return satellites

@app.put("/satellites/{satellite_id}", tags=["satellite"])
async def update_satellite(satellite_id: int, title: str = "",
                           country: str = "", expire_date: datetime = None,
                           orbit_radius: float = 0.0):
    satellite = session_.query(Satellite).filter(Satellite.satelliteId == satellite_id).first()
    if satellite:
        satellite.title = title or satellite.title
        satellite.country = country or satellite.country
        satellite.expireDate = expire_date or satellite.expireDate
        satellite.orbitRadius = orbit_radius or satellite.orbitRadius
        session_.commit()
        session_.refresh(satellite)
        return f"Satellite successfully updated. SatelliteID: {satellite.satelliteId}, Title: {satellite.title}."
    else:
        raise HTTPException(status_code=404, detail="Satellite not found")

@app.delete("/satellites/{satellite_id}", tags=["satellite"])
async def delete_satellite(satellite_id: int):
    satellite = session_.query(Satellite).filter(Satellite.satelliteId == satellite_id).first()
    if satellite:
        session_.delete(satellite)
        session_.commit()
        return f"Satellite successfully deleted. SatelliteID: {satellite.satelliteId}, Title: {satellite.title}."
    else:
        raise HTTPException(status_code=404, detail="Satellite not found")


# CRUD operations for TVChannel
@app.post("/tvchannels/", tags=["tvchannel"])
async def create_tv_channel(title: str = "",
                            broadcasting_language: str = "",
                            country: str = "",
                            telecompany: str = "",
                            channel_type: str = ""):
    tv_channel = TVChannel(title=title, broadcastingLanguage=broadcasting_language,
                           country=country, telecompany=telecompany, type=channel_type)
    session_.add(tv_channel)
    session_.commit()
    session_.refresh(tv_channel)
    return f"TV Channel successfully created. ChannelID: {tv_channel.tvChannelId}, Title: {tv_channel.title}."
@app.get("/tvchannels/{tv_channel_id}", tags=["tvchannel"])
async def read_tv_channel(tv_channel_id: int):
    tv_channel = session_.query(TVChannel).filter(TVChannel.tvChannelId == tv_channel_id).first()
    if tv_channel is None:
        raise HTTPException(status_code=404, detail="TV Channel not found")
    return tv_channel

@app.get("/tvchannels/", tags=["tvchannel"])
async def read_tv_channels(skip: int = 0, limit: int = 10):
    tv_channels = session_.query(TVChannel).offset(skip).limit(limit).all()
    return tv_channels

@app.put("/tvchannels/{tv_channel_id}", tags=["tvchannel"])
async def update_tv_channel(tv_channel_id: int, title: str = "",
                            broadcasting_language: str = "", country: str = "",
                            telecompany: str = "", channel_type: str = ""):
    tv_channel = session_.query(TVChannel).filter(TVChannel.tvChannelId == tv_channel_id).first()
    if tv_channel:
        tv_channel.title = title or tv_channel.title
        tv_channel.broadcastingLanguage = broadcasting_language or tv_channel.broadcastingLanguage
        tv_channel.country = country or tv_channel.country
        tv_channel.telecompany = telecompany or tv_channel.telecompany
        tv_channel.type = channel_type or tv_channel.type
        session_.commit()
        session_.refresh(tv_channel)
        return f"TV Channel successfully updated. ChannelID: {tv_channel.tvChannelId}, Title: {tv_channel.title}."
    else:
        raise HTTPException(status_code=404, detail="TV Channel not found")

@app.delete("/tvchannels/{tv_channel_id}", tags=["tvchannel"])
async def delete_tv_channel(tv_channel_id: int):
    tv_channel = session_.query(TVChannel).filter(TVChannel.tvChannelId == tv_channel_id).first()
    if tv_channel:
        session_.delete(tv_channel)
        session_.commit()
        return f"TV Channel successfully deleted. ChannelID: {tv_channel.tvChannelId}, Title: {tv_channel.title}."
    else:
        raise HTTPException(status_code=404, detail="TV Channel not found")

# CRUD operations for Broadcasting
@app.post("/broadcastings/", tags=["broadcasting"])
async def create_broadcasting(tv_channel_id: int = 0,
                               satellite_id: int = 0,
                               frequency: float = 0.0,
                               zone_start: int = 0,
                               zone_end: int = 0):
    broadcasting = Broadcasting(tvChannelId=tv_channel_id, satelliteId=satellite_id,
                                frequency=frequency, zoneStart=zone_start, zoneEnd=zone_end)
    session_.add(broadcasting)
    session_.commit()
    session_.refresh(broadcasting)
    return f"Broadcasting successfully created. BroadcastingID: {broadcasting.broadcasting_id}."

@app.get("/broadcastings/{broadcasting_id}", tags=["broadcasting"])
async def read_broadcasting(broadcasting_id: int):
    broadcasting = session_.query(Broadcasting).filter(Broadcasting.broadcasting_id == broadcasting_id).first()
    if broadcasting is None:
        raise HTTPException(status_code=404, detail="Broadcasting not found")
    return broadcasting

@app.get("/broadcastings/", tags=["broadcasting"])
async def read_broadcastings(skip: int = 0, limit: int = 10):
    broadcastings = session_.query(Broadcasting).offset(skip).limit(limit).all()
    return broadcastings

@app.put("/broadcastings/{broadcasting_id}", tags=["broadcasting"])
async def update_broadcasting(broadcasting_id: int, tv_channel_id: int = 0,
                              satellite_id: int = 0, frequency: float = 0.0,
                              zone_start: int = 0, zone_end: int = 0):
    broadcasting = session_.query(Broadcasting).filter(Broadcasting.broadcasting_id == broadcasting_id).first()
    if broadcasting:
        broadcasting.tvChannelId = tv_channel_id or broadcasting.tvChannelId
        broadcasting.satelliteId = satellite_id or broadcasting.satelliteId
        broadcasting.frequency = frequency or broadcasting.frequency
        broadcasting.zoneStart = zone_start or broadcasting.zoneStart
        broadcasting.zoneEnd = zone_end or broadcasting.zoneEnd
        session_.commit()
        session_.refresh(broadcasting)
        return f"Broadcasting successfully updated. BroadcastingID: {broadcasting.broadcasting_id}."
    else:
        raise HTTPException(status_code=404, detail="Broadcasting not found")

@app.delete("/broadcastings/{broadcasting_id}", tags=["broadcasting"])
async def delete_broadcasting(broadcasting_id: int):
    broadcasting = session_.query(Broadcasting).filter(Broadcasting.broadcasting_id == broadcasting_id).first()
    if broadcasting:
        session_.delete(broadcasting)
        session_.commit()
        return f"Broadcasting successfully deleted. BroadcastingID: {broadcasting.broadcasting_id}."
    else:
        raise HTTPException(status_code=404, detail="Broadcasting not found")

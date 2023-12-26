import random
from faker import Faker
from datetime import datetime, timedelta

from sqlalchemy import func

import session
from models import Satellite, TVChannel, Broadcasting
_session = session.session
fake = Faker()

# Function to generate random date within a given range
def random_date(start_date, end_date):
    return fake.date_time_between_dates(datetime_start=start_date, datetime_end=end_date)

# Function to create and add a Satellite record with random data
def create_satellite():
    return Satellite(
        title=fake.word(),
        country=fake.country(),
        expireDate=random_date(datetime.utcnow(), datetime.utcnow() + timedelta(days=365)),
        orbitRadius=random.uniform(100, 1000)
    )

# Function to create and add a TVChannel record with random data
def create_tv_channel():
    return TVChannel(
        title=fake.word(),
        broadcastingLanguage=fake.language_name(),
        country=fake.country(),
        telecompany=fake.company(),
        type=fake.word()
    )

# Function to create and add a Broadcasting record with random data
def create_broadcasting(tv_channel_id, satellite_id):
    return Broadcasting(
        tvChannelId=tv_channel_id,
        satelliteId=satellite_id,
        frequency=random.uniform(100, 1000),
        zoneStart=random.randint(1, 24),
        zoneEnd=random.randint(1, 24)
    )

for _ in range(10):
        satellite = create_satellite()
        _session.add(satellite)
        _session.flush()  # Ensure the satellite record is added to the database before using its ID
        for _ in range(2):  # Generate 2 TV channels for each satellite
            tv_channel = create_tv_channel()
            tv_channel.satelliteId = satellite.satelliteId
            _session.add(tv_channel)
_session.commit()
print("Random data added to TVChannel and Satellite tables.")

# Generate and add random data to the Broadcasting table
for _ in range(10):
    # Get random TV channel and satellite IDs from the existing records
    tv_channel_id = _session.query(TVChannel.tvChannelId).order_by(func.random()).first()[0]
    satellite_id = _session.query(Satellite.satelliteId).order_by(func.random()).first()[0]
    _session.add(create_broadcasting(tv_channel_id, satellite_id))

_session.commit()
print("Random data added to Broadcasting table.")

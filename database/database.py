# (©)CodeXBotz

import motor.motor_asyncio
from config import DB_URI, DB_NAME
import time

# Create an asynchronous MongoDB client
dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']
verification_data = database['verification']

# Ensure the '_id' field is indexed in both collections
user_data.create_index('user_id', unique=True)
verification_data.create_index('user_id', unique=True)

async def present_user(user_id: int):
    """Check if a user is present in the database."""
    try:
        found = await user_data.find_one({'_id': user_id})
        return bool(found)
    except Exception as e:
        print(f"Error checking user presence: {e}")
        return False

async def add_user(user_id: int):
    """Add a new user to the database."""
    try:
        await user_data.insert_one({'_id': user_id})
    except Exception as e:
        print(f"Error adding user: {e}")

async def full_userbase():
    """Retrieve the full list of users from the database."""
    try:
        user_docs = user_data.find()
        user_ids = []
        async for doc in user_docs:
            user_ids.append(doc['_id'])
        return user_ids
    except Exception as e:
        print(f"Error fetching user base: {e}")
        return []

async def del_user(user_id: int):
    """Delete a user from the database."""
    try:
        await user_data.delete_one({'_id': user_id})
    except Exception as e:
        print(f"Error deleting user: {e}")

# Additional functions for new features

async def add_verification(user_id: int, shortlink: str, expire_at: int):
    """Add a verification entry for a user."""
    try:
        verification_entry = {
            '_id': user_id,
            'shortlink': shortlink,
            'expire_at': expire_at
        }
        await verification_data.insert_one(verification_entry)
    except Exception as e:
        print(f"Error adding verification: {e}")

async def check_verification(user_id: int):
    """Check if a user has a valid verification entry."""
    try:
        verification_entry = await verification_data.find_one({'_id': user_id, 'expire_at': {'$gte': int(time.time())}})
        return verification_entry is not None
    except Exception as e:
        print(f"Error checking verification: {e}")
        return False

async def remove_verification(user_id: int):
    """Remove a user's verification entry."""
    try:
        await verification_data.delete_one({'_id': user_id})
    except Exception as e:
        print(f"Error removing verification: {e}")

import motor.motor_asyncio
from config import DB_URI, DB_NAME
from pytz import timezone
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an async client with Motor
dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]
collection = database['premium-users']

# Check if the user is a premium user
async def is_premium_user(user_id):
    try:
        user = await collection.find_one({"user_id": user_id})  # Async query
        logger.info(f"Checked premium status for user_id {user_id}: {'Found' if user else 'Not found'}")
        return user is not None
    except Exception as e:
        logger.error(f"Error checking premium status for user_id {user_id}: {str(e)}")
        return False

# Remove premium user
async def remove_premium(user_id):
    try:
        result = await collection.delete_one({"user_id": user_id})  # Async removal
        logger.info(f"Removed premium status for user_id {user_id}: {result.deleted_count} documents deleted")
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Error removing premium user {user_id}: {str(e)}")
        return False

# Remove expired users
async def remove_expired_users():
    ist = timezone("Asia/Kolkata")
    current_time = datetime.now(ist)
    logger.info("Checking for expired premium users...")

    try:
        async for user in collection.find({}):
            expiration = user.get("expiration_timestamp")
            if not expiration:
                logger.warning(f"User {user.get('user_id')} has no expiration_timestamp, skipping")
                continue

            try:
                expiration_time = datetime.fromisoformat(expiration).astimezone(ist)
                if expiration_time <= current_time:
                    await collection.delete_one({"user_id": user["user_id"]})
                    logger.info(f"Removed expired premium user {user['user_id']}")
            except Exception as e:
                logger.error(f"Error removing user {user.get('user_id')}: {str(e)}")
    except Exception as e:
        logger.error(f"Error in remove_expired_users: {str(e)}")

# List active premium users
async def list_premium_users():
    ist = timezone("Asia/Kolkata")
    current_time = datetime.now(ist)
    premium_user_list = []

    try:
        async for user in collection.find({}):
            user_id = user["user_id"]
            expiration_timestamp = user.get("expiration_timestamp")

            if not expiration_timestamp:
                logger.warning(f"User {user_id} has no expiration_timestamp, skipping")
                continue

            try:
                expiration_time = datetime.fromisoformat(expiration_timestamp).astimezone(ist)
                remaining_time = expiration_time - current_time

                if remaining_time.total_seconds() > 0:  # Only active users
                    days, hours, minutes, seconds = (
                        remaining_time.days,
                        remaining_time.seconds // 3600,
                        (remaining_time.seconds // 60) % 60,
                        remaining_time.seconds % 60,
                    )
                    expiry_info = f"{days}d {hours}h {minutes}m {seconds}s left"
                    formatted_expiry_time = expiration_time.strftime('%Y-%m-%d %H:%M:%S %p IST')
                    premium_user_list.append(
                        f"UserID: {user_id} - Expiry: {expiry_info} (Expires at {formatted_expiry_time})"
                    )
                    logger.info(f"Listed active premium user {user_id}: {expiry_info}")
                else:
                    logger.info(f"User {user_id} premium expired, removing")
                    await collection.delete_one({"user_id": user_id})
            except Exception as e:
                logger.error(f"Error processing user {user_id}: {str(e)}")
                premium_user_list.append(f"UserID: {user_id} - Error: Unable to process ({str(e)})")
    except Exception as e:
        logger.error(f"Error listing premium users: {str(e)}")
        premium_user_list.append(f"Error listing users: {str(e)}")

    return premium_user_list

# Add premium user
async def add_premium(user_id, time_value, time_unit):
    """
    Add a premium user for a specific duration.
    
    Args:
        user_id (int): The ID of the user to add premium access for.
        time_value (int): The numeric value of the duration.
        time_unit (str): Time unit - 's'=seconds, 'm'=minutes, 'h'=hours, 'd'=days, 'y'=years.
    """
    logger.info(f"Adding premium for user_id {user_id}: {time_value} {time_unit}")
    time_unit = time_unit.lower()
    ist = timezone("Asia/Kolkata")
    now = datetime.now(ist)

    try:
        # Calculate expiration time
        if time_unit == 's':
            expiration_time = now + timedelta(seconds=time_value)
        elif time_unit == 'm':
            expiration_time = now + timedelta(minutes=time_value)
        elif time_unit == 'h':
            expiration_time = now + timedelta(hours=time_value)
        elif time_unit == 'd':
            expiration_time = now + timedelta(days=time_value)
        elif time_unit == 'y':
            expiration_time = now + timedelta(days=365 * time_value)
        else:
            logger.error(f"Invalid time unit: {time_unit}")
            raise ValueError("Invalid time unit. Use 's', 'm', 'h', 'd', or 'y'.")

        # Prepare premium data
        premium_data = {
            "user_id": user_id,
            "expiration_timestamp": expiration_time.isoformat(),
        }

        # Update database
        result = await collection.update_one(
            {"user_id": user_id},
            {"$set": premium_data},
            upsert=True
        )
        logger.info(f"Updated premium status for user_id {user_id}: {result.modified_count} modified, {result.upserted_id} upserted")

        # Format and return
        formatted_expiration = expiration_time.strftime('%Y-%m-%d %H:%M:%S %p IST')
        logger.info(f"Premium added for user_id {user_id}, expires on {formatted_expiration}")
        return formatted_expiration
    except Exception as e:
        logger.error(f"Error adding premium for user_id {user_id}: {str(e)}")
        raise

# Check if a user has an active premium plan
async def check_user_plan(user_id):
    try:
        user = await collection.find_one({"user_id": user_id})  # Async query for user
        if user:
            expiration_timestamp = user["expiration_timestamp"]
            expiration_time = datetime.fromisoformat(expiration_timestamp).astimezone(timezone("Asia/Kolkata"))
            remaining_time = expiration_time - datetime.now(timezone("Asia/Kolkata"))

            if remaining_time.total_seconds() > 0:  # If the user is still active
                days, hours, minutes, seconds = (
                    remaining_time.days,
                    remaining_time.seconds // 3600,
                    (remaining_time.seconds // 60) % 60,
                    remaining_time.seconds % 60,
                )
                validity_info = f"Your premium plan is active. {days}d {hours}h {minutes}m {seconds}s left."
                logger.info(f"Checked plan for user_id {user_id}: {validity_info}")
                return validity_info
            else:
                logger.info(f"Premium plan expired for user_id {user_id}")
                return "Your premium plan has expired."
        else:
            logger.info(f"No premium plan found for user_id {user_id}")
            return "You do not have a premium plan."
    except Exception as e:
        logger.error(f"Error checking plan for user_id {user_id}: {str(e)}")
        return f"Error checking plan: {str(e)}"
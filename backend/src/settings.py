import os

import motor.motor_asyncio
from dotenv import load_dotenv
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

# ----------------- Environment Variables ----------------- #

load_dotenv()
PYTHONUNBUFFERED = os.getenv("PYTHONUNBUFFERED")
DB_URL = os.getenv("DB_URL")
SECRET = os.getenv("SECRET")

# ----------------- PATHS --------------------------

PATH_PREDICTED_IMG = os.getenv("PATH_PREDICTED_IMG")

PATH_RAW_SIGNS = os.getenv("PATH_RAW_SIGNS")
PATH_RAW_NUMPY = os.getenv("PATH_RAW_NUMPY")

PATH_CHECKPOINTS_LOAD = os.getenv("PATH_CHECKPOINTS_LOAD")
PATH_CHECKPOINTS_SAVE = os.getenv("PATH_CHECKPOINTS_SAVE")

# ----------------- Database variables (MongoDB) --------------------------

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
db = client.TesisDB
signal_table = db.signals
user_table = db.users
callback_table = db.callbacks

# ----------------- Database variables (MongoDB) --------------------------

serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), "TinyDate")

PATH_DB = os.getenv("PATH_DB")
tinydb = TinyDB(PATH_DB + "/db.json", storage=serialization)
signal_table_tinydb = tinydb.table("signals")
user_table_tinydb = tinydb.table("users")
callback_table_tinydb = tinydb.table("callbacks")

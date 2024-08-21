from fastapi import FastAPI
from contextlib import asynccontextmanager
import aiosqlite


@asynccontextmanager
async def lifespan(app: FastAPI):
    global connection, cursor
    connection = await aiosqlite.connect(":memory:")
    cursor = await connection.cursor()
    await cursor.execute(
        """
        CREATE TABLE weatherdata (
            date date,
            city text,
            avg_temp real,
            min_temp real,
            max_temp real,
            avg_humidity real
        )
    """
    )

    await connection.commit()

    app.state.connection = connection
    app.state.cursor = cursor

    yield

    await connection.close()


def get_db():
    return connection, cursor

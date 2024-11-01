from sqlalchemy import delete, insert, select, exc

from database import async_session_maker


class BaseDAO:
    model = None

    # @classmethod
    # async def find_by_id(cls, model_id: int):
    #     async with async_session_maker() as session:
    #         query = select(cls.model).filter_by(id=model_id)
    #         result = await session.execute(query)
    #         return result.scalar_one_or_none()
    #         # return result.mappings().one_or_none()


    @classmethod
    async def find_one_or_none(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()  # return result.mappings().one_or_none()


    @classmethod
    async def find_all(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()  # return result.mappings().all()

    @classmethod
    async def add_one(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()


    @classmethod
    async def delete(cls, **filters):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filters).returning(cls.model)
            deleted_resource = await session.execute(query)
            await session.commit()
            return deleted_resource.mappings().one_or_none()

            # try:
            #     return deleted_resource.mappings().one()
            # except exc.NoResultFound:
            #     return None

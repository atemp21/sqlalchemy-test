from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column, Integer, MetaData, Table, create_engine
from sqlalchemy.orm import sessionmaker


class Base(DeclarativeBase):
    id: any


class TestModel(Base):
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(primary_key=True)
    # make annotation not nullable
    code: Mapped[int]


if __name__ == "__main__":
    engine = create_engine("sqlite:///:memory:")
    # Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # create table test (id INTEGER NOT NULL, code INTEGER, PRIMARY KEY (id))
    meta = MetaData()

    test_table = Table(
        "test",
        meta,
        Column("id", Integer, primary_key=True),
        Column("code", Integer, nullable=True),
    )

    meta.create_all(engine)

    session.add(TestModel(code=1))
    session.commit()

    test1 = session.query(TestModel).filter(TestModel.code == 1).first()
    print(f"test1 code: {test1.code}")

    # I expect this to break because model is not nullable
    session.add(TestModel(code=None))
    session.commit()

    test_null = session.query(TestModel).filter(TestModel.code == None).first()
    print(f"test_null code: {test_null.code}")

    print("finished")

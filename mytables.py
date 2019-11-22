from sqlalchemy import create_engine
from sqlalchemy import Column, BigInteger, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation, backref
from sqlalchemy.ext.declarative import declared_attr


class Base(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=Base)


class some_table(Base):
    decl = Column(String, primary_key=True, autoincrement=False)

    def __init__(self, decl):
        self.decl = decl


class some_other_table2(Base):
    alpha = Column(String, primary_key=True, autoincrement=False)

    def __init__(self, alpha):
        self.alpha = alpha


class some_related_table(Base):
    a_col = Column(Integer, primary_key=True, autoincrement=False)
    decl = Column(String, ForeignKey('some_table.decl'))

    def __init__(self, a_col, decl):
        self.a_col = a_col
        self.decl = decl


class yet_another_table(Base):
    a_col = Column(Integer, primary_key=True, autoincrement=False)

    def __init__(self, b_col):
        self.b_col = b_col


def make_database(dbinfo):
    '''
    dbinfo is something like this: postgresql://xxxxx:yyyyy@zzz.zzz.zzz.zz/dbname
    '''
    # engine = create_engine('sqlite:///:memory:', echo=True)
    # engine = create_engine('sqlite:///pfs_proto.sqlite', echo=False)
    engine = create_engine(dbinfo)

    print("table={}".format(some_table.__table__))

    Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    Session()


if __name__ == '__main__':
    import sys
    dbinfo = sys.argv[1]
    print(dbinfo)
    make_database(dbinfo)

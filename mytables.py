from sqlalchemy import create_engine
from sqlalchemy import Column, BigInteger, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation, backref

Base = declarative_base()


class Proposal(Base):
    __tablename__ = 'Proposal'

    proposalId = Column(String, primary_key=True, autoincrement=False)

    def __init__(self, proposalId):
        self.proposalId = proposalId


def make_database(dbinfo):
    '''
    dbinfo is something like this: postgresql://xxxxx:yyyyy@zzz.zzz.zzz.zz/dbname
    '''
    # engine = create_engine('sqlite:///:memory:', echo=True)
    # engine = create_engine('sqlite:///pfs_proto.sqlite', echo=False)
    engine = create_engine(dbinfo)

    Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    Session()


if __name__ == '__main__':
    import sys
    dbinfo = sys.argv[1]
    print(dbinfo)
    make_database(dbinfo)

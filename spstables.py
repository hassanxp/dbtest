from sqlalchemy import create_engine
from sqlalchemy import Column, BigInteger, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation, backref

Base = declarative_base()


# From Yabe-san's core schema
class pfi_visit(Base):
    __tablename__ = 'pfi_visit'

    pfi_visit_id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    pfi_visit_description = Column(String)

    def __init__(self, pfi_visit_id, pfi_visit_description):
        self.pfi_visit_id = pfi_visit_id
        self.pfi_visit_description = pfi_visit_description


class pfs_site(Base):
    __tablename__ = 'pfs_site'

    site_id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    site_description = Column(String)

    def __init__(self, site_id, site_description):
        self.site_id = site_id
        self.site_description = site_description


class visit_set(Base):
    __tablename__ = 'visit_set'

    set_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    cmd_str = Column(String)

    def __init__(self, set_id):
        self.set_id = set_id


class visit_info(Base):
    __tablename__ = 'visit_info'

    visit_id = Column(Integer, ForeignKey('pfi_visit.pfi_visit_id'), primary_key=True)
    set_id = Column(Integer, ForeignKey('visit_set.set_id'))
    visit_type = Column(String)

    def __init__(self, set_id, visit_id, visit_type):
        self.visit_id = visit_id
        self.set_id = set_id
        self.visit_type = visit_type


class sps_annotation(Base):
    __tablename__ = 'sps_annotation'

    annotation_id = Column(Integer, primary_key=True, autoincrement=False)
    set_id = Column(Integer, ForeignKey('visit_set.set_id'))
    visit = Column(Integer, ForeignKey('pfi_visit.pfi_visit_id'))
    comment = Column(String)
    anomaly = Column(String)

    def __init__(self, annotation_id, set_id, visit, comment, anomaly):
        self.annotation_id = annotation_id
        self.set_id = set_id
        self.visit = visit
        self.comment = comment
        self.anomaly = anomaly


class sps_camera(Base):
    __tablename__ = 'sps_camera'

    camera_id = Column(Integer, primary_key=True, autoincrement=False)
    set_id = Column(Integer, ForeignKey('visit_set.set_id'))
    sps_module = Column(Integer)
    arm = Column(String)

    def __init__(self, camera_id, set_id, sps_module, arm):
        self.camera_id = camera_id
        self.set_id = set_id
        self.sps_module = sps_module
        self.arm = arm


class sps_anomalies(Base):
    __tablename__ = 'sps_anomalies'

    anomaly_id = Column(Integer, primary_key=True, autoincrement=False)
    visit_id = Column(Integer, ForeignKey('pfi_visit.pfi_visit_id'))
    site_id = Column(Integer, ForeignKey('pfs_site.site_id')) 
    sps_module = Column(Integer)
    arm = Column(String)
    description = Column(String)

    def __init__(self, anomaly_id, visit_id, site_id, sps_module, arm, description):
        self.anomaly_id = anomaly_id
        self.visit = visit_id
        self.site_id = site_id
        self.sps_module = sps_module
        self.arm = arm
        self.description = description


class processing_status(Base):
    __tablename__ = 'processing_status'

    status_id = Column(Integer, primary_key=True, autoincrement=False)
    set_id = Column(Integer, ForeignKey('visit_set.set_id'), unique=True)
    visit = Column(Integer, ForeignKey('pfi_visit.pfi_visit_id'))
    data_ok = Column(Boolean)

    def __init__(self, status_id, set_id, visit, data_ok):
        self.status_id = status_id
        self.set_id = set_id
        self.visit = visit
        self.data_ok = data_ok


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

from sqlalchemy import create_engine
from sqlalchemy import Column, BigInteger, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation, backref

Base = declarative_base()


# From Yabe-san's core schema
# class pfi_visit(Base):
#     __tablename__ = 'pfi_visit'

#     pfi_visit_id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
#     pfi_visit_description = Column(String)

#     def __init__(self, pfi_visit_id, pfi_visit_description):
#         self.pfi_visit_id = pfi_visit_id
#         self.pfi_visit_description = pfi_visit_description


# class pfs_site(Base):
#     __tablename__ = 'pfs_site'

#     pfs_site_id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
#     site_description = Column(String)

#     def __init__(self, pfs_site_id, site_description):
#         self.pfs_site_id = pfs_site_id
#         self.site_description = site_description


# class sps_arm(Base):
#     __tablename__ = 'sps_arm'

#     sps_arm_id = Column(String, primary_key=True, unique=True, autoincrement=False)
#     sps_arm_description = Column(String)

#     def __init__(self, sps_arm_id, sps_arm_description):
#         self.sps_arm_id = sps_arm_id
#         self.sps_arm_description = sps_arm_description


# class sps_anomalies(Base):
#     __tablename__ = 'sps_anomalies'

#     anomaly_id = Column(Integer, primary_key=True, autoincrement=False)
#     pfi_visit_id = Column(Integer, ForeignKey('pfi_visit.pfi_visit_id'))
#     pfs_site_id = Column(Integer, ForeignKey('pfs_site.pfs_site_id'))
#     sps_module = Column(Integer)
#     sps_arm_id = Column(String, ForeignKey('sps_arm.sps_arm_id'))
#     description = Column(String)

#     def __init__(self, anomaly_id, visit_id, pfs_site_id, sps_module, sps_arm_id, description):
#         self.anomaly_id = anomaly_id
#         self.visit = visit_id
#         self.pfs_site_id = pfs_site_id
#         self.sps_module = sps_module
#         self.sps_arm_id = sps_arm_id
#         self.description = description

class visit_set(Base):
    __tablename__ = 'visit_set'

    visit_set_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    cmd_str = Column(String)

    def __init__(self, visit_set_id):
        self.visit_set_id = visit_set_id


class sps_visit(Base):
    __tablename__ = 'sps_visit'

    pfi_visit_id = Column(Integer, primary_key=True)  # Link to pfi_visit_id later
    visit_set_id = Column(Integer, ForeignKey('visit_set.visit_set_id'))
    visit_type = Column(String) # BIAS, DFLAT etc - another table defining them?

    def __init__(self, pfi_visit_id, visit_set_id, visit_type):
        self.pfi_visit_id = pfi_visit_id
        self.visit_set_id = visit_set_id
        self.visit_type = visit_type


class sps_annotation(Base):
    __tablename__ = 'sps_annotation'

    sps_annotation_id = Column(Integer, primary_key=True, autoincrement=False)
    visit_set_id = Column(Integer, ForeignKey('visit_set.visit_set_id'))
    pfi_visit_id = Column(Integer) # Connect to pfi_visit_id table later
    comment = Column(String)
    anomaly = Column(String)

    def __init__(self, annotation_id, visit_set_id, pfi_visit_id, comment, anomaly):
        self.sps_annotation_id = annotation_id
        self.visit_set_id = visit_set_id
        self.pfi_visit_id = pfi_visit_id
        self.comment = comment
        self.anomaly = anomaly


class sps_camera(Base):
    __tablename__ = 'sps_camera'

    sps_camera_id = Column(Integer, primary_key=True, autoincrement=False)
    visit_set_id = Column(Integer, ForeignKey('visit_set.visit_set_id'))
    sps_module = Column(Integer) # Foreign key to module table?
    sps_arm_id = Column(String) # Foreign key to arm table?

    def __init__(self, camera_id, visit_set_id, sps_module, sps_arm_id):
        self.sps_camera_id = camera_id
        self.visit_set_id = visit_set_id
        self.sps_module = sps_module
        self.sps_arm_id = sps_arm_id


class processing_status(Base):
    __tablename__ = 'processing_status'

    status_id = Column(Integer, primary_key=True, autoincrement=False)
    visit_set_id = Column(Integer, ForeignKey('visit_set.visit_set_id'))
    pfi_visit_id = Column(Integer) # Link to pfi_visit table later
    data_ok = Column(Boolean)

    def __init__(self, status_id, visit_set_id, pfi_visit_id, data_ok):
        self.status_id = status_id
        self.visit_set_id = visit_set_id
        self.pfi_visit_id = pfi_visit_id
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

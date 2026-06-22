"""
Legacy remote `clients` DB models — read-only access to `clients.alloc`
(nightly program schedule on the opal server).
"""
from sqlalchemy import Column, Date, Integer, String, Time
from sqlalchemy.orm import declarative_base

LegacyClientsBase = declarative_base()


class ClientAlloc(LegacyClientsBase):
    """
    `clients.alloc` — one row per allocated observation night.

    Queried by `datein` to get the list of programs scheduled for a given
    summit log date ("OPAL Programs for {date}").
    """

    __tablename__ = "alloc"

    idno = Column(Integer, primary_key=True, autoincrement=True)
    gid = Column(String(10))
    propid = Column(String(15))
    instr = Column(String(10))
    first = Column(String(30))          # PI first name
    last = Column(String(30))           # PI last name
    observers = Column(String(100))     # on-site observers
    remote = Column(String(100))        # remote observers
    staff = Column(String(100))         # support astronomers / staff
    datein = Column(Date, index=True)   # scheduled observation date
    dateout = Column(Date)
    sem = Column(String(4))
    nights = Column(Integer)
    comment = Column(String(100))
    ao1 = Column(String(10), name="order1")   # AO primary
    ao2 = Column(String(10), name="order2")   # AO secondary
    in1 = Column(Time)
    out1 = Column(Time)
    idno2 = Column(Integer)

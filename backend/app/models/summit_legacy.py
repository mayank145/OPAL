"""
Summit Logging — legacy MariaDB `sumlogs` schema (days, items, progs, itemreqs).

The modern API maps onto these tables directly; no Postgres normalization layer.
"""
from sqlalchemy import Column, Date, DateTime, Integer, String, Text

from app.db.session import SummitBase


class Day(SummitBase):
    """Legacy `days` table — one row per summit log date."""

    __tablename__ = "days"

    idno = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    day = Column(String(10))
    history = Column(Text)

    to1 = Column(String(40))
    to2 = Column(String(40))
    io1 = Column(String(40))
    io2 = Column(String(40))
    dc1 = Column(String(40))
    dc2 = Column(String(40))
    to1loc = Column(String(30))
    to2loc = Column(String(30))
    io1loc = Column(String(30))
    io2loc = Column(String(30))
    toin = Column(DateTime)
    toout = Column(DateTime)
    ioin = Column(DateTime)
    ioout = Column(DateTime)
    dcin = Column(DateTime)
    dcout = Column(DateTime)

    sky = Column(Text)
    seeing = Column(Text)
    temp = Column(Text)
    wind = Column(Text)
    humid = Column(Text)
    comment = Column(Text)

    mailed = Column(String(1))
    mailtime = Column(DateTime)
    mailsmoka = Column(String(1))
    smokatime = Column(DateTime)
    mailday = Column(String(1))
    maildtime = Column(DateTime)


class Item(SummitBase):
    """Legacy `items` table — log entries and work plans (logcrew='WP')."""

    __tablename__ = "items"

    idno = Column(Integer, primary_key=True, autoincrement=True)
    dayidno = Column(Integer, index=True)
    date = Column(Date, index=True)
    day = Column(String(10))
    logcrew = Column(String(10), index=True)
    itemtime = Column(DateTime)
    itemtitle = Column(String(200))
    itemtext = Column(Text)
    user = Column(String(20))
    type = Column(String(16))
    downtime = Column(Integer)
    subsystem = Column(String(10))
    status = Column(String(15))
    timestamp = Column(DateTime)
    history = Column(Text)
    oldidno = Column(Integer)
    comment = Column(Text)
    endtime = Column(DateTime)
    realstart = Column(DateTime)
    realend = Column(DateTime)
    niteeffect = Column(String(100))
    dayeffect = Column(String(100))
    location = Column(String(20))
    assigned1 = Column(String(30))
    dcassist = Column(String(10))
    location2 = Column(String(20))
    location3 = Column(String(20))
    comptitle = Column(String(200))
    contact2 = Column(String(50))
    others = Column(String(50))
    master = Column(Integer)
    assigned2 = Column(String(50))
    notify = Column(String(20))
    comptext = Column(Text)
    melco = Column(String(20))
    fai = Column(String(20))
    contact1 = Column(String(40))
    otherreq = Column(String(40))
    seats = Column(Integer)
    seats2 = Column(Integer)
    residno = Column(Integer)
    residno2 = Column(Integer)
    residno3 = Column(Integer)
    residno4 = Column(Integer)
    residno5 = Column(Integer)
    residno6 = Column(Integer)
    pass_ = Column("pass", String(80))
    rpass = Column(String(80))
    pseats = Column(Integer)
    updatestamp = Column(DateTime)
    intervene = Column(String(20))


class Prog(SummitBase):
    """Legacy `progs` table — observation programs for a night."""

    __tablename__ = "progs"

    idno = Column(Integer, primary_key=True, autoincrement=True)
    dayidno = Column(Integer, index=True)
    date = Column(Date, index=True)
    day = Column(String(10))
    seq = Column(String(2))
    instr = Column(String(10))
    alloc = Column(String(10))
    pi = Column(String(50))
    ao1 = Column(String(10))
    ao2 = Column(String(10))
    intime = Column(DateTime)
    outtime = Column(DateTime)
    gid = Column(String(10))
    propid = Column(String(20))
    obs1 = Column(String(50))
    obs1loc = Column(String(10))
    obs2 = Column(String(50))
    obs2loc = Column(String(10))
    obs3 = Column(String(50))
    obs3loc = Column(String(10))
    obs4 = Column(String(50))
    obs4loc = Column(String(10))
    ss = Column(String(30))
    ssloc = Column(String(10))
    ss2 = Column(String(30))
    ss2loc = Column(String(10))
    others1 = Column(String(50))
    others1loc = Column(String(10))
    others2 = Column(String(50))
    others2loc = Column(String(10))
    comment = Column(String(100))


class ItemReq(SummitBase):
    """Legacy `itemreqs` — required / lockout flags for work plans."""

    __tablename__ = "itemreqs"

    idno = Column(Integer, primary_key=True, autoincrement=True)
    planidno = Column(Integer, index=True)
    code = Column(String(40))

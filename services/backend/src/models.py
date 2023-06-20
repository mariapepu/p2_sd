from sqlalchemy import Boolean, Column, create_engine, Date, DateTime, Enum, Float, ForeignKey, Integer, MetaData, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base

categories_list = ("Senior", "Junior")
sports_list = ("Volleyball", "Football", "Basketball", "Futsal")
teams_in_competitions = Table("teams_in_competitions", Base.metadata, Column("id", Integer, primary_key=True), Column("team_id", Integer, ForeignKey("teams.id")), Column("competition_id", Integer, ForeignKey("competitions.id")))

class Team(Base):
    __tablename__ = 'teams' #This is table name

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False, index=True)
    country = Column(String(30), nullable=False)
    description = Column(String(100))

class Competition(Base):
    __tablename__ = 'competitions'  # This is table name
    __table_args__ = (UniqueConstraint('name', 'category', 'sport'),)

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    category = Column(Enum(*categories_list), nullable=False)
    sport = Column(Enum(*sports_list), nullable=False)
    teams = relationship("Team", secondary=teams_in_competitions, backref="competitions")

class Match(Base):
    __tablename__ = 'matches' #This is table name
    __table_args__ = (UniqueConstraint('local_id', 'visitor_id', 'competition_id', 'date'),)

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False) #date = Column(Date, nullable=False) #codi original: import Date // Column(DateTime)
    price = Column(Float, nullable=False)
    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)
    competition = relationship("Competition", backref="matches")

    local_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    visitor_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    local = relationship("Team", foreign_keys=local_id)
    visitor = relationship("Team", foreign_keys=visitor_id)
    total_available_tickets = Column(Integer)
    #Finalment, afegiu un camp nou total_available_tickets al model de Match
    # que per defecte sigui el nombre de localitats del lloc on s'està fent
    # i feu les actualitzacions necessàries al constructor.

class Account(Base):
    __tablename__ = 'accounts'

    username = Column(String(30), primary_key=True, unique=True, nullable=False)
    password = Column(String(), nullable=False)
    # 0 not admin/ 1 is admin
    is_admin = Column(Integer, nullable=False)
    available_money = Column(Float, nullable=False)
    orders = relationship('Order', backref='orders', lazy=True)

    def __init__(self, username, available_money=200, is_admin=0):
        self.username = username
        self.available_money = available_money
        self.is_admin = is_admin

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), ForeignKey('accounts.username'), nullable=False)
    match_id = Column(Integer, nullable=False)
    tickets_bought = Column(Integer, nullable=False)

    def __init__(self, match_id, tickets_bought):
        self.match_id = match_id
        self.tickets_bought = tickets_bought
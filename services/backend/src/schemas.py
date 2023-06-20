from datetime import datetime
import enum
from pydantic import BaseModel, Field
from typing import Optional
import models

#########
# TEAMS #
#########

class TeamBase(BaseModel):
    name: str
    country: str
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True

################
# COMPETITIONS #
################

class CompetitionBase(BaseModel):
    name: str
    category: enum.Enum('category', dict(zip(models.categories_list, models.categories_list)))
    sport: enum.Enum('sport', dict(zip(models.sports_list, models.sports_list)))

class CompetitionCreate(CompetitionBase):
    pass

class Competition(CompetitionBase):
    id: int
    teams: list[Team] = []

    class Config:
        orm_mode = True

###########
# MATCHES #
###########

class MatchBase(BaseModel):
    date: datetime
    price: float
    local: TeamBase
    visitor: TeamBase
    competition: CompetitionBase
    total_available_tickets: int = 0 #que per defecte sigui el nombre de localitats del lloc on s'està fent (???)

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    local: Team
    visitor: Team
    competition: Competition

    class Config:
        orm_mode = True

##########
# ORDERS #
##########

class OrderBase(BaseModel):
    match_id: int
    tickets_bought: int

class OrderCreate(OrderBase):
    username: str #= Field(..., description="username")

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True

############
# ACCOUNTS #
############

class AccountBase(BaseModel):
    is_admin: int
    available_money: float

class AccountCreate(AccountBase):
    username: str = Field(..., description="username")
    password: str = Field(..., min_length=8, max_length=24 ,description="user password")

class Account(AccountBase):
    orders: list[Order] = []

    class Config:
        orm_mode = True

##########
# TOKENS #
##########
"""
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

class SystemAccount(models.Account):
    password: str
"""
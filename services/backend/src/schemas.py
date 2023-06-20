from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from models import sports_list, categories_list, Category, Sports
from typing import List


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
    category: Category
    sport: Sports


class CompetitionCreate(CompetitionBase):
    pass


class Competition(CompetitionBase):
    id: int
    teams: List[Team] = []

    class Config:
        orm_mode = True


###########
# MATCHES #
###########

class MatchBase(BaseModel):
    date: datetime
    price: float
    local: Team
    visitor: Team
    competition: Competition
    total_available_tickets: int


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int

    class Config:
        orm_mode = True


##########
# ORDERS #
##########

class OrderBase(BaseModel):
    match_id: int
    tickets_bought: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    username: str

    class Config:
        orm_mode = True


############
# ACCOUNTS #
############

class AccountBase(BaseModel):
    username: str
    password: str
    available_money: float
    is_admin: int
    orders: List[Order] = []


class AccountCreate(AccountBase):
    username: str = Field(..., description="username")
    password: str = Field(..., min_length=8, max_length=24, description="user password")

    class Config:
        orm_mode = True

    pass


class Account(AccountBase):
    class Config:
        orm_mode = True


##########
# TOKENS #
##########

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class SystemAccount(Account):
    password: str

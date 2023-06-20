from fastapi import HTTPException
from numpy import select
from sqlalchemy.orm import Session
from models import Competition, Match, Team, Order, Account
from schemas import CompetitionCreate, MatchCreate, TeamCreate, OrderCreate
from sqlalchemy import select, or_
from utils import get_hashed_password


#########
# TEAMS #
#########

def get_team(db: Session, team_id: int):
    return db.query(Team).filter(Team.id == team_id).first()


def get_team_by_name(db: Session, name: str):
    return db.query(Team).filter(Team.name == name).first()


def get_teams(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(Team).offset(skip).limit(limit).all()


def create_team(db: Session, team: TeamCreate):
    db_team = Team(name=team.name, country=team.country, description=team.description)
    try:
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return db_team
    except:
        db.rollback()
        return {"message": "An error occurred inserting the teams."}, 500


def delete_team(db: Session, team_id: int):
    db_team = get_team(db, team_id)
    if db_team:
        try:
            db.delete(db_team)
            db.commit()
            return db_team
        except:
            db.rollback()
            return {"message": "An error occurred deleting the teams."}, 500
    return db_team


def update_team(db: Session, team_id: int, team: TeamCreate):
    db_team = get_team(db, team_id)
    if db_team:
        try:
            db_team.name = team.name
            db_team.country = team.country
            db_team.description = team.description
            db.commit()
            db.refresh(db_team)
            return db_team
        except:
            db.rollback()
            return {"message": "An error occurred inserting the teams."}, 500
    return db_team

def update_team_by_name(db: Session, team_name: str, team: TeamCreate):
    db_team = get_team_by_name(db, team_name)
    if not db_team:
        return None
    db_team.name = team.name
    db_team.country = team.country
    db_team.description = team.description
    db.commit()
    db.refresh(db_team)
    return db_team

def get_matches_team(db: Session, team_name: str):
    team = get_team_by_name(db, team_name)
    if not team:
        return None
    team_id = team.id
    return db.query(Match).filter(
        or_(
            Match.local_id == team_id,
            Match.visitor == team_id
        )
    ).all()


def get_competitions_team(db: Session, team_name: str):
    team = get_team_by_name(db, team_name)
    if not team:
        return None
    team_id = team.id
    compes = []
    competitions = get_competitions(db, 0, 100)
    for comp in competitions:
        if any(team.id == t.id for t in comp.teams):
            compes.append(comp)
    return compes


################
# COMPETITIONS #
################

def get_competition(db: Session, competition_id: int):
    return db.query(Competition).filter(Competition.id == competition_id).first()


def get_competition_by_name(db: Session, name: str):
    return db.query(Competition).filter(Competition.name == name).first()


def get_competitions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Competition).offset(skip).limit(limit).all()


def create_competition(db: Session, competition: CompetitionCreate):
    db_competition = Competition(name=competition.name, category=competition.category, sport=competition.sport)
    try:
        db.add(db_competition)
        db.commit()
        db.refresh(db_competition)
        return db_competition
    except:
        db.rollback()
        return {"message": "An error occurred inserting the competitions."}, 500


def delete_competition(db: Session, competition_id: int):
    db_competition = get_competition(db, competition_id)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    try:
        db.delete(db_competition)
        db.commit()
        return {"message": f"Competition with id {competition_id} has been deleted successfully."}
    except:
        db.rollback()
        return {"message": "An error occurred deleting the competitions."}, 500


def update_competition(db: Session, competition_id: int, competition: Competition):
    db_competition = get_competition(db, competition_id)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    try:
        db_competition.name = competition.name
        db_competition.category = competition.category
        db_competition.sport = competition.sport
        db_competition.teams = competition.teams
        db.commit()
        db.refresh(db_competition)
        return db_competition
    except:
        db.rollback()
        return {"message": "An error occurred deleting the competitions."}, 500


def get_matches_competition(db: Session, competition_name: str):
    db_competition = get_competition_by_name(db, competition_name)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    matches = db_competition.match
    return matches


def get_teams_competition(db: Session, competition_name: str):
    db_competition = get_competition_by_name(db, competition_name)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    teams = db_competition.teams
    return teams


###########
# MATCHES #
###########

def get_match(db: Session, match_id: int):
    return db.query(Match).filter(Match.id == match_id).first()


def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Match).offset(skip).limit(limit).all()


def get_matches_by_date(db: Session, date: str):
    return db.query(Match).filter(Match.date == date).all()


def create_match(db: Session, match: MatchCreate):
    local_team = get_team_by_name(db, match.local.name)
    if local_team is None:
        raise HTTPException(status_code=422, detail="Local team not found")
    visitor_team = get_team_by_name(db, match.visitor.name)
    if visitor_team is None:
        raise HTTPException(status_code=422, detail="Visitor team not found")
    competition = get_competition_by_name(db, match.competition.name)

    if competition is None:
        # Si la competición no existe, la creamos
        db_competition = Competition(
            name=match.competition.name,
            category=match.competition.category,
            sport=match.competition.sport
        )
        db.add(db_competition)
        db.commit()
        db.refresh(db_competition)
        competition = db_competition

    db_match = Match(
        date=match.date,
        price=match.price,
        total_available_tickets=match.total_available_tickets,
        competition=competition,
        local=local_team,
        visitor=visitor_team
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def delete_match(db: Session, match_id: int):
    db_match = get_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    try:
        db.delete(db_match)
        db.commit()
        return {"message": f"Match with id {match_id} has been deleted successfully."}
    except:
        db.rollback()
        return {"message": "An error occurred deleting the competitions."}, 500


def update_match(db: Session, match_id: int, match: MatchCreate):
    db_match = get_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    try:
        db_match.name = match.date
        db_match.country = match.price
        db_match.description = match.local
        db_match.description = match.visitor
        db_match.description = match.competition
        db_match.description = match.total_available_tickets
        db.commit()
        db.refresh(db_match)
        return db_match
    except:
        db.rollback()
        return {"message": "An error occurred deleting the competitions."}, 500


def get_teams_match(db: Session, match_id: int):
    db_match = get_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    local_id = db_match.local_id
    visitor_id = db_match.visitor_id
    local = get_team(db, local_id)
    visitor = get_team(db, visitor_id)
    teams = [local, visitor]
    return teams


def get_competition_match(db: Session, match_id: int):
    db_match = get_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    competition_id = db_match.competition_id
    competition = get_competition(db, competition_id)
    return competition


##########
# ORDERS #
##########
def get_orders_by_username(db: Session, username: str):
    # acc = select(models.Account).where(models.Account.username == username)
    # account: schemas.Account = db.execute(acc).scalar()
    # return account.orders
    acc = db.query(Account).filter(Account.username == username).first()
    return acc.orders


def get_account_by_username(db: Session, username: str):
    return db.query(Account).filter(Account.username == username).first()


def create_account(db: Session, account: dict):
    db_account = Account(
        username=account['username'],
        available_money=account['available_money'],
        is_admin=account['is_admin']
    )
    db_account.password = get_hashed_password(account['password'])

    try:
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account
    except:
        db.rollback()
        return "couldn't create the account"


def create_orders(db: Session, username: str, order: OrderCreate):
    db_order = Order(match_id=order.match_id, tickets_bought=order.tickets_bought)

    # para seleccionar una account y no la lista de accounts
    acc = select(Account).where(Account.username == username)
    # para que la account sea una Account y no un Select
    account: Account = db.execute(acc).scalar()

    # para seleccionar un Match y no la lista de Matches
    match = select(Match).where(Match.id == order.match_id)
    # para que el Match sea un Match y no un Select
    game: Match = db.execute(match).scalar()
    if account.available_money < (game.price * db_order.tickets_bought):
        return "you don't have enough money"

    if game.total_available_tickets < db_order.tickets_bought:
        return "there are not enough tickets. Only " + account.available_money.toString() + "remaining"

    else:
        game.total_available_tickets -= db_order.tickets_bought
        account.available_money -= (game.price * db_order.tickets_bought)

        account.orders.append(db_order)
        try:
            db.add(db_order)
            db.commit()
            db.refresh(db_order)
            return db_order
        except:
            db.rollback()
            return "couldn't create the order"


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()


def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Account).offset(skip).limit(limit).all()


def delete_account(db: Session, username: str):
    account = get_account_by_username(db, username)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(account)
    db.commit()
    return {"message": f"{account.username} has been deleted successfully."}


def update_account(db: Session, username: str, acc: Account):
    db_account = get_account_by_username(db, username)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    try:
        db_account.username = acc.username
        db_account.password = get_hashed_password(acc.password)
        db_account.available_money = acc.available_money
        db_account.is_admin = acc.is_admin
        db_account.orders = acc.orders
        db.commit()
        db.refresh(db_account)
        return db_account
    except:
        db.rollback()
        return {"message": "couldn't update the account"}

from sqlalchemy.orm import Session
import models, schemas

#########
# TEAMS #
#########

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_team_by_name(db: Session, name: str):
    return db.query(models.Team).filter(models.Team.name == name).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()

#TODO check if this works
def get_teams_by_competition(db: Session, competition_id: int):
    competition = get_competition(db, competition_id)
    return competition.teams

#TODO check if this works
def get_teams_by_match(db: Session, match_id: int):
    match = get_match(db, match_id)
    return list[match.local, match.visitor]

def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(name=team.name, country=team.country, description=team.description)
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
            db.refresh(db_team)
            return db_team
        except:
            db.rollback()
            return {"message": "An error occurred deleting the teams."}, 500
    return db_team

def update_team(db: Session, team_id: int, team: schemas.TeamCreate):
    db_team = get_team(db, team_id)
    if db_team:
        try:
            if team.name:
                db_team.name = team.name
            if team.country:
                db_team.country = team.country
            if team.description:
                db_team.description = team.description
            db.commit()
            db.refresh(db_team)
            return db_team
        except:
            db.rollback()
            return {"message": "An error occurred inserting the teams."}, 500
    return db_team

################
# COMPETITIONS #
################

def get_competition(db: Session, competition_id: int):
    return db.query(models.Competition).filter(models.Competition.id == competition_id).first()

def get_competition_by_name(db: Session, name: str):
    return db.query(models.Competition).filter(models.Competition.name == name).first()

def get_competitions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Competition).offset(skip).limit(limit).all()

#TODO check if this works
def get_competitions_by_team(db: Session, team_id: int):
    return db.query(models.Competition).filter(team_id in [team.id for team in models.Competition.teams])

#TODO check if this works
def get_competition_by_match(db, match_id):
    match = get_match(db, match_id)
    return get_competition(db, match.competition_id)

def create_competition(db: Session, competition: schemas.CompetitionCreate):
    db_competition = models.Competition(name=competition.name, category=competition.category, sport=competition.sport)
    if db_competition:
        try:
            db.add(db_competition)
            db.commit()
            db.refresh(db_competition)
            return db_competition
        except:
            db.rollback()
            return {"message": "An error occurred inserting the competitions."}, 500
    return db_competition

def delete_competition(db: Session, competition_id: int):
    db_competition = get_competition(db, competition_id)
    try:
        db.delete(db_competition)
        db.commit()
        db.refresh(db_competition)
        return db_competition
    except:
        db.rollback()
        return {"message": "An error occurred deleting the competitions."}, 500

def update_competition(db: Session, competition_id: int, competition: schemas.CompetitionCreate):
    db_competition = get_competition(db, competition_id)
    if db_competition:
        try:
            if competition.name:
                db_competition.name = competition.name
            if competition.category:
                db_competition.category = competition.category
            if competition.sport:
                db_competition.sport = competition.sport
            db.commit()
            db.refresh(db_competition)
            return db_competition
        except:
            db.rollback()
            return {"message": "An error occurred deleting the competitions."}, 500
    return db_competition

###########
# MATCHES #
###########

def get_match(db: Session, match_id: int):
    return db.query(models.Match).filter(models.Match.id == match_id).first()

def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Match).offset(skip).limit(limit).all()

# TODO check if this works
def get_matches_by_team(db: Session, team_id: int):
    return db.query(models.Match).filter(team_id == models.Match.local_id or team_id == models.Match.visitor_id)

# TODO check if this works
def get_matches_by_competition(db: Session, competition_id: int):
    return db.query(models.Match).filter(competition_id == models.Match.competition_id)

def create_match(db: Session, match: schemas.MatchCreate):
    db_match = models.Match(date=match.date, price=match.price, local=match.local, visitor=match.visitor, competition=match.competition, total_available_tickets=match.total_available_tickets)
    try:
        db.add(db_match)
        db.commit()
        db.refresh(db_match)
        return db_match
    except:
        db.rollback()
        return {"message": "An error occurred inserting the matches."}, 500

def delete_match(db: Session, match_id: int):
    db_match = get_match(db, match_id)
    if db_match:
        try:
            db.delete(db_match)
            db.commit()
            db.refresh(db_match)
            return db_match
        except:
            db.rollback()
            return {"message": "An error occurred deleting the competitions."}, 500
    return db_match

def update_match(db: Session, match_id: int, match: schemas.MatchCreate):
    db_match = get_match(db, match_id)
    if db_match:
        try:
            if match.date:
                db_match.name = match.date
            if match.price:
                db_match.country = match.price
            if match.local:
                db_match.description = match.local
            if match.visitor:
                db_match.description = match.visitor
            if match.competition:
                db_match.description = match.competition
            if match.total_available_tickets:
                db_match.description = match.total_available_tickets
            db.commit()
            db.refresh(db_match)
            return db_match
        except:
            db.rollback()
            return {"message": "An error occurred deleting the competitions."}, 500
    return db_match

##########
# ORDERS #
##########

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_order_by_username(db: Session, username: str):
    return db.query(models.Order).filter(models.Order.name == username).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(name=order.match_id, tickets_bought=order.tickets_bought)
    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    except:
        db.rollback()
        return {"message": "An error occurred inserting the orders."}, 500

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if db_order:
        try:
            db.delete(db_order)
            db.commit()
            db.refresh(db_order)
            return db_order
        except:
            db.rollback()
            return {"message": "An error occurred deleting the competitions."}, 500
    return db_order

def update_order(db: Session, order_id: int, order: schemas.OrderCreate):
    db_order = get_order(db, order_id)
    if db_order:
        try:
            if order.match_id:
                db_order.match_id = order.match_id
            if order.tickets_bought:
                db_order.tickets_bought = order.tickets_bought
            db.commit()
            db.refresh(db_order)
            return db_order
        except:
            db.rollback()
            return {"message": "An error occurred deleting the competitions."}, 500
    return db_order

############
# ACCOUNTS #
############

def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()

def get_account_by_name(db: Session, username: str):
    return db.query(models.Account).filter(models.Account.name == username).first()

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(is_admin=account.is_admin, available_money=account.available_money)
    try:
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account
    except:
        db.rollback()
        return {"message": "An error occurred inserting the accounts."}, 500

def delete_account(db: Session, account_id: int):
    db_account = get_account(db, account_id)
    if db_account:
        try:
            db.delete(db_account)
            db.commit()
            db.refresh(db_account)
            return db_account
        except:
            db.rollback()
            return {"message": "An error occurred deleting the competitions."}, 500
    return db_account

def update_account(db: Session, account_id: int, account: schemas.AccountCreate):
    db_account = get_account(db, account_id)
    if db_account:
        try:
            if account.is_admin:
                db_account.is_admin = account.is_admin
            if account.available_money:
                db_account.available_money = account.available_money
            db.commit()
            db.refresh(db_account)
            return db_account
        except:
            db.rollback()
            return {"message": "An error occurred deleting the competitions."}, 500
    return db_account

#TODO these specefications:
#Comproveu si l'usuari té prou diners per comprar el bitllet

#Comproveu si hi ha entrades disponibles

#Actualitzeu les entrades disponibles a Match (- entrades comprades)

#Actualitzeu els diners de l'usuari després de comprar els bitllets (-preu * bitllets comprat)

#Afegiu la comanda a la relació d'usuari `user.orders.append(new_order)`

#Deseu els canvis fets a  comanda, match i l'usuari a la BD. **Atenció!** amb les condicions de carrera!.
# Feu un sol commit per a totes les operacions i comproveu si es provoca algun error,
# en aquest cas caldrà fer un rollback i tornar-ho a intentar o retornar un error.

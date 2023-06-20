from datetime import datetime
from fastapi import Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import repository, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)  # Creem la base de dades amb els models que hem definit a SQLAlchemy

app = FastAPI()

app.mount("/static", StaticFiles(directory="../../frontend/dist/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="../../frontend/dist")
@app.get("/")
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="../../frontend/dist")

@app.get("/")
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

"""@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get('/python')
def like_python():
    return {'I like Python!'}"""


#########
# TEAMS #
#########

#@app.get(): s’utilitza per sol·licitar informació
@app.get("/team/{team_name}", summary="Get details of team given its name", response_model=schemas.Team)
def read_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@app.get("/teams/", summary="Get details of teams with id from skip to skip+limit", response_model=list[schemas.Team])
def read_teams(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_teams(db, skip=skip, limit=limit)

#@app.post(): s’utilitza per afegir nous elements a la nostra estructura de dades
@app.post("/teams/", summary="Create new team", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = repository.get_team_by_name(db, team.name)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already exists, use put for updating")
    return repository.create_team(db, team)

#@app.delete(): s'utilitza per eliminar elements de la nostra estructura de dades
@app.delete("/team/{team_name}", summary="Delete team given its name", response_model=schemas.Team)
def delete_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return repository.delete_team(db, team.id)

#@app.put(): s’utilitza per modificar els elements existents a la nostra estructura de dades
@app.put("/team/{team_name}", summary="Update team given its name and updated data", response_model=schemas.Team)
def update_team(team_name: str, team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = repository.get_team_by_name(db, team_name)
    if not db_team:
        return create_team(db, team)
    team_with_updated_name = repository.get_team_by_name(db, team.name)
    if team_with_updated_name != db_team: #Check that there isn't another team with the same name we are updating
        raise HTTPException(status_code=400, detail="Team name already in use")
    return repository.update_team(db, db_team.id, team)

#GET /competitions/{competition_name}/teams: retorna tots els equips d'una competició, donada el seu nom.
@app.get("/competitions/{competition_name}/teams", summary="Get all teams of a competition given its name", response_model=list[schemas.Team])
def read_teams_of_competition(competition_name: str, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_name(db, competition_name)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return repository.get_teams_by_competition(db, competition.id)

#GET /matches/{match_id}/teams: retorna l'equip local i visitant d'un partit, donat el seu id.
@app.get("/matches/{match_id}/teams", summary="Get both teams of a match given its id", response_model=list[schemas.Team])
def read_teams_of_match(match_id: int, db: Session = Depends(get_db)):
    match = repository.get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return repository.get_teams_by_match(db, match_id)


################
# COMPETITIONS #
################

@app.get("/competitions/", summary="Get competitions with id from skip to skip+limit", response_model=list[schemas.Competition])
def read_competitions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_competitions(db, skip=skip, limit=limit)

@app.post("/competitions/", response_model=schemas.Competition)
def create_competition(competition: schemas.Competition,db: Session = Depends(get_db)):
    db_competition = repository.get_competition_by_name(db, name=competition.name)
    if db_competition:
        raise HTTPException(status_code=400, detail="Competition already Exists, Use put for updating")
    else:
        return repository.create_competition(db=db, competition=competition)

@app.put("/competitions/", response_model=schemas.Competition)
def update_competition(competition: schemas.Competition,db: Session = Depends(get_db)):
    db_competition = repository.get_competition_by_name(db, name=competition.name)
    if db_competition:
        return repository.update_competition(db=db, competition = competition)
    else:
        raise HTTPException(status_code=400, detail="Competition doesn't Exists")


@app.get("/competition/{competition_id}", response_model=schemas.Competition)
def get_competition(competition_id: str, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_id(db, competition_id)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return competition


@app.delete("/competition/{competition_id}", response_model=schemas.Competition)
def delete_match(competition_id: str, db: Session = Depends(get_db)):
    competition = repository.get_match_by_id(db, competition_id)
    if competition:
        repository.delete_competition(db=db, competition=competition)
        return competition
    else:
        raise HTTPException(status_code=400, detail="Competition not found")
@app.get("/competition/{competition_name}", summary="Get details of competition given its name", response_model=schemas.Competition)
def read_competition(competition_name: str, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_name(db, competition_name)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return competition

@app.delete("/competition/{competition_name}", response_model=schemas.Competition)
def delete_competition(competition_name: str,db: Session = Depends(get_db)):
    competition = repository.get_competition_by_name(db, name=competition_name)
    if competition:
        repository.delete_competition(db=db, competition = competition)
        return competition
    else:
        raise HTTPException(status_code=400, detail="Competition not found")


@app.put("/competition/{competition_name}", summary="Update competition given its id and updated data", response_model=schemas.Competition)
def update_competition(competition_name: str, competition: schemas.CompetitionCreate, db: Session = Depends(get_db)):
    db_competition = repository.get_competition_by_name(db, competition_name)
    if not db_competition:
        return create_competition(db, competition)
    #Competition names aren't unique according to the given code in models.py, but a mandatory method uses a search of competition by name, so it must be unique
    competition_with_updated_name = repository.get_competition_by_name(db, competition.name)
    if competition_with_updated_name != db_competition: #Check that there isn't another competition with the same name we are updating
        raise HTTPException(status_code=400, detail="Competition name already in use")
    return repository.update_competition(db, db_competition.id, competition)

#GET /teams/{team_name}/competitions: retorna totes les competicions d'un equip, donat el seu nom.
@app.get("/teams/{team_name}/competitions", summary="Get competitions of a team given its name", response_model=list[schemas.Competition])
def read_competitions_of_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return repository.get_competitions_by_team(db, team.id)

#GET /matches/{match_id}/competition: retorna la competició d'un partit, donat el seu id.
@app.get("/matches/{match_id}/competition", summary="Get competition of a game given its id", response_model=schemas.Competition)
def read_competitions_of_match(match_id: int, db: Session = Depends(get_db)):
    match = repository.get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return repository.get_competition_by_match(db, match_id)


###########
# MATCHES #
###########

@app.get("/matches/", summary="Get matches with id from skip to skip+limit", response_model=list[schemas.Match])
def read_matches(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_matches(db, skip=skip, limit=limit)
@app.post("/matches/", summary="Create new match", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    db_match = repository.get_match(db, match.id)
    if db_match:
        raise HTTPException(status_code=400, detail="Match already exists, use put for updating")
    return repository.create_match(db, match)

@app.put("/matches/", response_model=schemas.Match)
def update_match(match: schemas.Match,db: Session = Depends(get_db)):
    db_match = repository.get_match_by_team(db= db,  team_l=match.local, team_v=match.visitor)
    if db_match:
        return repository.update_match(db=db, match = match)
    else:
        raise HTTPException(status_code=400, detail="Match doesn't Exists")

@app.get("/match/{match_id}", summary="Get details of match with id match_id", response_model=schemas.Match)
def read_match(match_id: int, db: Session = Depends(get_db)):
    match = repository.get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

#GET /teams/{team_name}/matches: retorna tots els partits d'un equip, donat el seu nom.
@app.get("/teams/{team_name}/matches", summary="Get matches of a team given its name", response_model=list[schemas.Match])
def read_matches_of_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return repository.get_matches_by_team(db, team.id)

#GET /competitions/{competition_name}/matches: retorna tots els partits d'una competició, donada el seu nom.
@app.get("/competitions/{competition_name}/matches", summary="Get matches of a competition given its name", response_model=list[schemas.Match])
def read_matches_of_competition(competition_name: str, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_name(db, competition_name)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return repository.get_matches_by_competition(db, competition.id)

@app.get("/match/{match_id}", response_model=schemas.Match)
def get_match(match_id: str,db: Session = Depends(get_db)):
    match = repository.get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match whith teams not found")
    return match

@app.delete("/match/{match_id}", summary="Delete match with id match_id", response_model=schemas.Match)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    match = repository.get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return repository.delete_match(db, match.id)

@app.put("/match/{match_id}", summary="Update new match with id match_id, with data on match", response_model=schemas.Match)
def update_match(match_id: int, match: schemas.MatchCreate, db: Session = Depends(get_db)):
    db_match = repository.get_match(db, match_id)
    if not db_match:
        return create_match(db, match)
    return repository.update_match(db, db_match.id, match)

##########
# ORDERS #
##########

@app.get('/orders/{username}', response_model=schemas.Order)
def get_ordre(user_name: str,db: Session = Depends(get_db)):
    ordre = repository.get_order_by_name(db, name=user_name)
    if not ordre:
        raise HTTPException(status_code=404, detail="Order not found")
    return ordre

@app.post('/orders/{username}', response_model=schemas.Order)
def create_order(order: schemas.OrderCreate,db: Session = Depends(get_db)):
    db_order = repository.get_order_by_match(db, match=order.match_id)
    if db_order:
        raise HTTPException(status_code=400, detail="Order with this match already Exists")
    else:
        order = repository.create_order(db=db, order=order)
        if order == "No":
            raise HTTPException(status_code=400,
                                detail="Order no completada, comprova si tens suficient diners o si hi ha suficients entrades")

        elif order == "Error":
            raise HTTPException(status_code=500,
                                detail="Error al guardar a la base de dades")
        else:
            return order

@app.get('/orders', response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_orders(db, skip=skip, limit=limit)

############
# ACCOUNTS #
############
"""
@app.get('/account', summary='Get details of currently logged in user', response_model=schemas.SystemAccount)
async def get_me(user: schemas.SystemAccount = Depends(dependencies.get_current_user)):
    return user
"""
#obtenir informació del compte amb un nom d'usuari
@app.get('/account/{username}', response_model=schemas.Account)
def read_account(username: str, db: Session = Depends(get_db)):
    account = repository.get_account_by_username(db, username)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

#obtenir informació sobre tots els comptes
@app.get('/accounts')
def read_accounts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_accounts(db, skip=skip, limit=limit)

#creeu un compte nou passant `username` i `password' Utilitzeu `hash_ password` quan creeu un compte (primer heu de crear un usuari nou i després afegir una contrasenya hash mitjançant el mètode `.hash_ password (password)`).
@app.post('/account', response_model=schemas.Account)
def create_account(account: schemas.AccountCreate,db: Session = Depends(get_db)):
    db_account = repository.get_account_by_name(db, name=account.username)
    if db_account:
        raise HTTPException(status_code=400, detail="User already Exists, Use put for updating")
    else:
        return repository.create_account(db=db, account=account)

#suprimiu un compte relacionat amb un nom d'usuari (recordeu també suprimir totes les comandes relacionades).
@app.delete('/account/{username}')
def delete_account(account_name: str, db: Session = Depends(get_db)):
    account = repository.get_account_by_name(db, account_name)
    if not account:
        raise HTTPException(status_code=404, detail="account not found")
    return repository.delete_account(db, account.id)

#actualitzeu la informació del compte amb un nom d'usuari
@app.put('/account/{username}')
def update_account(account_name: str, account: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = repository.get_account_by_name(db, account_name)
    if not db_account:
        return create_account(db, account)
    account_with_updated_name = repository.get_account_by_name(db, account.name)
    if account_with_updated_name != db_account: #Check that there isn't another account with the same name we are updating
        raise HTTPException(status_code=400, detail="account name already in use")
    return repository.update_account(db, db_account.id, account)

"""
##########
# TOKENS #
##########
@app.post('/login', summary="Create access and refresh tokens for user", response_model=schemas.TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
   username = form_data.username
   password = form_data.password
   db_account = repository.get_account_by_name(db, username)
   if not db_account:
       raise HTTPException(status_code=400, detail="account doesn´t exist")
   if not verify_password(password, db_account.password):
       raise HTTPException(status_code=400, detail="passwordn't")
   return{
        "access_token": utils.create_access_token(db_account.username),
        "refresh_token": utils.create_refresh_token(db_account.username),
}
"""
#TODO optional
#Protegiu tots els endpoints perquè només puguin ser accedits per usuaris registrats. Deixeu només els gets que no tinguin informació sensible (p.ex compte d'usuari, comandes, etc) com a públics.
#Modifiqueu la dependència per tal que si un usuari és admin pugui accedir a tots els endpoints.
"""def test_create_match():
    competition = {
        "name": "Test Barça",
        "category": "Senior",
        "sport": "Football"
    }
    local = {
        "name": "Barça",
        "country": "Spain"
    }
    visitor = {
        "name": "Madrid",
        "country": "Spain"
    }
    match = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price": 100.00,
        "local": local,
        "visitor": visitor,
        "competition": competition,
        "total_available_tickets": 100,

    }
    @app.post("/teams/", json=local)
    @app.post("/teams/", json=visitor)
    @app.post("/competitions/", json=competition)
    @app.post("/matches/", json=match)

    local1 = {
        "name": "UD Las Palmas",
        "country": "Spain"
    }
    visitor1 = {
        "name": "Atletico de Madrid",
        "country": "Spain"
    }
    match1 = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price": 60.00,
        "local": local1,
        "visitor": visitor1,
        "competition": competition,
        "total_available_tickets": 100,

    }
    @app.post("/teams/", json=local1)
    @app.post("/teams/", json=visitor1)
    @app.post("/competitions/", json=competition)
    @app.post("/matches/", json=match1)

    local2 = {
        "name": "Espanyol",
        "country": "Spain"
    }
    visitor2 = {
        "name": "Tenerife",
        "country": "Spain"
    }
    match2 = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price": 3.00,
        "local": local2,
        "visitor": visitor2,
        "competition": competition,
        "total_available_tickets": 50,

    }
    @app.post("/teams/", json=local2)
    @app.post("/teams/", json=visitor2)
    @app.post("/competitions/", json=competition)
    @app.post("/matches/", json=match2)"""
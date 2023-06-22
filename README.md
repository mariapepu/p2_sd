---
author:
- Maria Perez,  Quim Lagunas
date: Juny 2023
title: Pràctica 2 - FastAPI and Vue application (Software distribuït)
---

Sessió de Test
=========

En la sessió de test vem provar els programes de 3 grups diferents: A05, A12 i A13.

Pel que fa a cada programa:
-A05: el programa del grup A05 era responsive i tenia el frontend i el backend correctament enllaçats, a més complia totes les funcionalitats mencionades en la sessió de test (navegar pel catàleg, afegir productes a la cistella, logar-se, registrar-se, fer la compra i tancar la sessió, en tots els ordres que vem provar); i el nombre de tickets decrementava amb cada compra.

-A12: el programa del grup A12 tenia frontend i backend correctament enllaçats però els elements del frontend eren poc responsive, va fallar el logout i calia actualitzar la pàgina per a poder veure la quantitat de diners actualitzada però totes les demes funcionalitats funcionaven correctament (inclús bloquejava la compra una vegada els tickets baixaven a 0.

-A13: el grup A13 no ens va poder mostrar el seu frontend ja que els ordinadors de la universitat no permeten instal·lar els imports necessaris per a poder visualitzar el frontend sense permisos d'administrador. Pel que fa a backend ens va mostrar el seu correcte funcionament de la majoria de mètodes a Postman.

A nosaltres ens va fallar el codi aquell mateix dia de test per raons desconegudes, ens donaven errors imports que eren correctes i que fins el dia anterior ens funcionaven; fins a tal punt que vem haver de començar de nou perquè ens seguia donant error fins i tot en programes guardats d'anteriors sesions previament testejades correctament a diferents dispositius.
Així amb el codi des de 0, vem anar injectant poc a poc les parts de codi que ja teniem (i corregint errors, esperant trobar-nos errors que obstaculitzesin el funcionament del programa, però només vem trobar errors menors).
El múltiples canvis d'estructura a través de les sessions van fer aquest procediment més lent i tediós.

Intruccions de compilació
=========
No sabem perque el docker no ens acaba de funcionar però ho hem intentat. Per tal de pasar a producció, en el fitxer .env haurem de posar el booleà production a true, i en utils.py haurem de descomenta la linia 29 i comentar la 30.

En cas que no funcioni el docker, executarem dins de `services/backend/src` la comanda `uvicorn main:app --env-file ./.env`. Un cop tenim el backend funcionant podem executar el fontend situant-nos a la carpeta de frontend i executant `npm run dev`.

Per algun motiu que desconeixem el .env no es puja a github, aixi que facilitem aqui el contingut:
```
JWT_SECRET_KEY="Alguna cosa secreta"
JWT_REFRESH_SECRET_KEY="Alguna altra cosa secreta"
VUE_APP_BACKEND_URL=http://0.0.0.0:8000/
PRODUCTION=True
```
Per a la producció i en general sempre que volguem corre per primer cop el backend, haurem de fer `npm run build` en el frontend, ja que sense la carpeta obtinguda del buils, el backend no es pot linkejar bé al frontend.

Feina feta per cada integrant:
=========
- Sessio 1 i 2: Maria i posteriorment Quim
- Sessio 3 i 4: 
    -  Front: Maria 
    -  Back: Quim
- Sessio 5: 
    -  Front: Maria 
    -  Back: Quim (i Maria només per mirar d'arreglar problemes)
- Sessio 6: Intent de deploy: Maria

Com hem comentat en fer el deploy vam començar a tenir molts problemes que no vam poder resoldre ni amb ajuda del professor. Vam decidir fer un rollback, i finalment vam haver d'anar fins la sessió 2. Llavors el Quim va continuar amb el que ens faltava de la sessió5 i arreglant problemes que detectava en el backend metre la Maria va anar sessió per sessió assegurant-se que el codi funcionés. Finalment no hem aconseguit asegurar el funcionament de tot pero no hem tingut temps de fer més, despres del fallo en el deploy.

##### **FEINA RECUPERACIÓ:**
- Tots els bug fixes que s'han fet així com els dockers, els hem fet conjuntament, normalment en videoconferencia. Primer vam asegurar-nos que el backend i les seves funcions anaven correctament ja que algunes no ho feien, i vam crear un test_main.py per tal d'omplir la base de dades. Després d'aixó ens vam centrar en que el frontend reflectís la informació i s'actualitzés correctament. Finalment vam intentar implamentar els dockers.

- Per tal de treballar conjuntament, vam haver d'obrir un repositori al nostre propi github per poder seguir fent feina. Quan se'ns obri el github penjarem tota la feina feta.

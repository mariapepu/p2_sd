<template>
  <div id="app">
    <div class="header">
      <h1> {{ message }} </h1>
      <div class="header-right">
        <button class="btn-vc header-btn" @click="is_showing_cart = !is_showing_cart">Veure cistella
          <div class="svg-wrapper-1">
            <div class="svg-wrapper">
              <!--aqui iria el icono-->
              <div v-if="is_showing_cart" class="closebox"></div>
            </div>
          </div>
        </button>
        <button class="btn-vc header-btn" @click="login">Iniciar sessió</button>
      </div>
    </div>
    <hr class="gradient">
    <div v-if="is_showing_cart" class="container" style="margin-top: 3%">
      <h2 class="text-center">Cistella</h2>
      <div class=" cart-container">
        <div v-if="matches_added.length > 0">
          <table class="table-r table table-striped">
            <thead>
            <tr class="table-light">
              <th scope="col">ID</th>
              <th scope="col">Esport</th>
              <th scope="col">Competició</th>
              <th scope="col">Partit</th>
              <th scope="col">Quantitat</th>
              <th scope="col">Preu(&euro;)</th>
              <th scope="col">Total</th>
              <th scope="col"></th>
            </tr>
            </thead>
            <tbody v-for="(cart) in matches_added" :key="cart.id">
            <tr class="table-light">
              <th scope="row">{{ cart.match.id }}</th>
              <td class="table-light">{{ cart.match.competition.sport }}</td>
              <td class="table-light">{{ cart.match.competition.name }}</td>
              <td class="table-light">{{ cart.match.local.name }} vs {{ cart.match.visitor.name }}</td>
              <td class="table-light">
                <div class="input-group">
                        <span class="input-group-prepend">
                          <button class="btn-less btn btn-outline-secondary btn-number" data-type="plus" type="button"
                                  v-on:click="cart.quantity > 1 ? cart.quantity -= 1 : ''">
                            -
                          </button>
                        </span>
                  <input :value=cart.quantity class="form-control text-center" max="10" min="0" readonly>
                  <span class="input-group-append">
                          <button class="btn-add btn btn-outline-secondary btn-number" data-type="plus" type="button"
                                  v-on:click="cart.quantity += 1">
                            +
                          </button>
                        </span>
                </div>
              </td>
              <td class="table-light">{{ cart.match.price }}&euro;</td>
              <td class="table-light">{{ (cart.match.price * cart.quantity).toFixed(2) }}&euro;</td>
              <td class="align-middle table-light">
                <button class="btn btn-danger" type="button" @click="deleteEvent(cart.id)">Eliminar</button>
              </td>
            </tr>
            </tbody>
          </table>
          <div class="row justify-content-center align-items-center">
            <button class="btn btn-secondary btn-group" type="button" @click="is_showing_cart = !is_showing_cart">
              Enrere
            </button>
            <button class="btn btn-success btn-group" type="submit">Finalitza la compra</button>
          </div>
        </div>
        <div v-else>
          <p class="text-center">La teva cistella és buida.</p>
          <div class="row justify-content-center align-items-center">
            <button class="btn btn-secondary btn-group" type="button" @click="is_showing_cart = !is_showing_cart">
              Enrere
            </button>
            <button class="btn btn-success btn-group disabled" style="cursor: not-allowed" type="submit">Finalitza la
              compra
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="!is_showing_cart" class="container">
      <div class="row">
        <div v-for="(match, index) in matches" :key="match.id" class="col-lg-4 col-md-6 mb-4">
          <br>
          <div class="card bg-dark text-black">
            <div class="card-header">
              <h5>{{ match.competition.sport }} - {{ match.competition.category }}</h5>
              <h6>{{ match.competition.name }}</h6>
            </div>
            <img :src="cardImages[index]" alt="Card image" class="card-img">
            <div class="card-img-overlay card-body">
              <h6><strong>{{ match.local.name }}</strong> ({{ match.local.country }}) <br>vs<br> <strong>{{
                  match.visitor.name
                }}</strong> ({{ match.visitor.country }})</h6>
              <h6>{{ match.date.substring(0, 10) }}</h6>
              <h6>{{ match.price }} &euro;</h6>
              <button class="btn btn-success btn-lg card-btn" v-on:click="addEventToCart(match)">Afegeix a la cistella
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      message: 'Sport Matches',
      tickets_bought: 0,
      is_showing_cart: false,
      matches_added: [],
      cardImages: [
        'https://media.istockphoto.com/id/626535710/es/foto/jugador-de-voleibol-de-la-escuela-secundaria-asi%C3%A1tica-dispara-voleibol-contra-oponentes.jpg?s=612x612&w=0&k=20&c=Zt90sNrGqg_2utf3CDdF4sddEEM2sQ76a2Vwzqt-z6I=',
        'https://5corunafs.com/web2022/wp-content/uploads/2021/01/SAVE_20210121_074852-1-768x552.jpg',
        'https://5corunafs.com/web2022/wp-content/uploads/2021/01/SAVE_20210121_074852-1-768x552.jpg'
        // Agrega más URLs de imágenes según sea necesario
      ],
      matches: [
        {
          'id': 1,
          'local': {
            'id': 3,
            'name': 'Club Juventut Les Corts',
            'country': 'Spain'
          },
          'visitor': {
            'id': 2,
            'name': 'CE Sabadell',
            'country': 'Spain'
          },
          'competition': {
            'name': 'Women\'s European Championship',
            'category': 'Senior',
            'sport': 'Volleyball'
          },
          'date': '2022-10-12T00:00:00',
          'price': 4.3
        },
        {
          'id': 2,
          'local': {
            'id': 3,
            'name': 'Club Juventut Les Corts',
            'country': 'Spain'
          },
          'visitor': {
            'id': 2,
            'name': 'CE Sabadell',
            'country': 'Spain'
          },
          'competition': {
            'name': '1st Division League',
            'category': 'Junior',
            'sport': 'Futsal'
          },
          'date': '2022-07-10T00:00:00',
          'price': 129.29
        },
        {
          'id': 3,
          'local': {
            'id': 1,
            'name': 'CV Vall D\'Hebron',
            'country': 'Spain'
          },
          'visitor': {
            'id': 4,
            'name': 'Volei Rubi',
            'country': 'Spain'
          },
          'competition': {
            'name': '1st Division League',
            'category': 'Junior',
            'sport': 'Futsal'
          },
          'date': '2022-08-10T00:00:00',
          'price': 111.1
        }
      ]
    }
  },
  methods: {
    login () {
      this.$router.push({path: '/userlogin'})
    },
    addEventToCart (match) {
      this.var_loop = true
      var eventAdded = {
        'match': match,
        'quantity': 1
      }
      for (var i = 0; i < this.matches_added.length; i++) {
        if (this.matches_added[i].match === match) {
          this.matches_added[i].quantity += 1
          this.var_loop = false
        }
      }
      if (this.var_loop) {
        this.matches_added.push(eventAdded)
      }
    },
    deleteEvent (event) {
      this.matches_added.splice(event, 1)
    },
    buyTicket () {
      this.tickets_bought += 1
    },
    getMatches () {
      const pathMatches = 'http://localhost:8000/matches/'
      const pathCompetition = 'http://localhost:8000/competition/'

      axios.get(pathMatches)
        .then((res) => {
          var matches = res.data.filter((match) => {
            return match.competition_id != null
          })
          var promises = []
          for (let i = 0; i < matches.length; i++) {
            const promise = axios.get(pathCompetition + matches[i].competition_id)
              .then((resCompetition) => {
                delete matches[i].competition_id
                matches[i].competition = {
                  'name': resCompetition.data.competition.name,
                  'category': resCompetition.data.competition.category,
                  'sport': resCompetition.data.competition.sport
                }
              })
              .catch((error) => {
                console.error(error)
              })
            promises.push(promise)
          }
          Promise.all(promises).then((_) => {
            this.matches = matches
          })
        })
        .catch((error) => {
          console.error(error)
        })
    }
  },
  created () {
    this.getMatches()
  }
}

</script>

<style>

.card {
  border-radius: 15px;
  height: 400px;
  border: none;
  color: #000000;
  overflow: hidden;
  box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.3);
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0px 0px 15px 15px;
}

.card-img-overlay {
  transition: 0.3s;
  border-radius: 15px;
}

.card:hover .card-img-overlay {
  backdrop-filter: blur(5px) brightness(35%);
  color: #fff;
  border-radius: 15px;
}

.card-body {
  flex-direction: column;
  justify-content: center;
  display: flex;
  position: absolute;
  background-color: rgba(166, 165, 165, 0.5);
  padding-bottom: 3%;
  padding-top: 3%;
  backdrop-filter: opacity(50%);
  border-radius: 15px;
  width: 100%;
  height: 100%;
  top: -100%;
  right: 0;
  transition: 1s;
}

.card:hover .card-body {
  top: 0;
}

.card-btn {
  color: #ffffff;
  font-weight: bold;
}

.card-header {
  font-weight: 600;
  background-color: white;
  padding-top: 3%;
  padding-bottom: 2%;
}

.header {
  overflow: hidden;
  padding-top: 5%;
//margin-bottom: 5%; padding-bottom: 2%; padding-left: 5%; padding-right: 5%; background-color: white;
}

.header > h1 {
  font-size: xxx-large;
  font-family: "DejaVu Sans Light", serif;
  font-size-adjust: v-bind();
  float: left;
  color: black;
  text-align: left;
  padding: 12px;
  text-decoration: none;
  line-height: 25px;
  border-radius: 4px;
}

.header-btn {
  margin-right: 5%;
  vertical-align: center;
  color: sandybrown;
  font-family: sans-serif;
  font-weight: 530;
  padding: 0;
  width: fit-content;
  background-color: #ffffff;
  border-color: sandybrown;
  border-width: medium;
  min-width: 150px;
  transition-duration: .3s;
  margin-left:2%;
  margin-top:2%;
  margin-bottom:2%;
}

.header .header-btn {
  float: left;
  text-align: center;
  padding: 12px;
  text-decoration: none;
  font-size: 18px;
  line-height: 20px;
  border-radius: 8px;
  width: fit-content;
}

.header .header-btn:hover {
  background-color: peachpuff;
  color: black;
}

.header-right {
  float: right;
}

@media screen and (max-width: 500px) {
  .header a {
    float: none;
    display: block;
    text-align: left;
  }

  .header-right {
    float: none;
  }
}

hr.gradient {
  height: 3px;
  border: none;
  border-radius: 6px;
  margin-top: 0;
  padding-top: 0;
  background: linear-gradient(
    270deg,
    rgb(255, 166, 87) 0%,
    #FFDAB9FF 50%,
    rgb(255, 166, 87) 100%
  );
}

.table-r {
  overflow-y: hidden;
}

.cart-container {
  overflow-y: hidden;
  align-content: center;
  vertical-align: center;
}

.btn-group {
  float: left;
  margin: 5%;
}

.btn-less {
  background-color: #bd2130;
  font-weight: bold;
  font-size: large;
  font-size-adjust: v-bind();
  color: white;
  border: none;
}

.btn-add {
  background-color: #1e7e34;
  font-weight: bold;
  font-size: large;
  font-size-adjust: v-bind();
  color: white;
  border: none;
}

.btn-vc {
  background-color: sandybrown;
  font-weight: inherit;
  font-size: large;
  font-size-adjust: v-bind();
  color: #151515;
  border: none;
}

.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-vc:active {
  transform: translateY(4px);
}

</style>

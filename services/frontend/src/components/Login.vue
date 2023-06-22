<template>
  <div id="app" style="min-height: 600px">
    <div class="header">
      <h1> {{ message }} </h1>
      <div class="header-right"></div>
    </div>
    <hr class="gradient">
    <div v-if="ini_crear">
      <div class="uwu" style="margin-bottom: 5%">
        <h4>Inicia sessió</h4>
        <form>
          <div class="form-label-group">
            <label for="username">Username</label>
        <input
          type="text"
          id="username"
          v-model="username"
          class="form-control"
          placeholder="Username"
          required autofocus
          :style="{ color: username === '' ? '#999999' : '' }"
        />
          </div>
          <div class="form-label-group">
            <br>
             <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          class="form-control"
          placeholder="Password"
          required
          :style="{ color: password === '' ? '#999999' : '' }"
        />
          </div>
          <button class="btn btn-primary" style="margin-top: 8%; width: 100%" type="button" @click="checkLogin">Iniciar sessió</button>
          <button class="btn btn-add" style="margin-top: 2%; width: 100%; font-weight: normal;" type="button"
                  @click="ini_crear = !ini_crear">Crear Compte
          </button>
          <button class="btn btn-secondary" style="margin-top: 2%; width: 100%" type="button" @click="atras">Tornar a
            Matches
          </button>
        </form>
      </div>
    </div>
    <div v-else>
      <div class="uwu" style="margin-bottom: 5%">
        <h4>Crea un compte</h4>
        <form>
          <div class="form-label-group">
            <label for="create-username">Username</label>
        <input
          type="text"
          id="create-username"
          v-model="createUsername"
          class="form-control"
          placeholder="Username"
          required
          :style="{ color: addUserForm.username === '' ? '#999999' : '' }"
        />
          </div>
          <div class="form-label-group">
            <br>
            <label for="create-password">Password</label>
        <input
          type="password"
          id="create-password"
          v-model="createPassword"
          class="form-control"
          placeholder="Password"
          required
          :style="{ color: addUserForm.password === '' ? '#999999' : '' }"
        />
          </div>
          <button class="btn btn-primary" style="margin-top: 8%; width: 100%" type="button" @click="submitAccount">Crear Compte</button>
          <button class="btn btn-secondary" style="margin-top: 2%; width: 100%" type="button"
                  @click="ini_crear = !ini_crear">Tornar Iniciar sessió
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      message: 'Sports Matches',
      ini_crear: true,
      logged: false,
      username: null,
      password: null,
      token: null,
      createUsername: null,
      createPassword: null,
      addUserForm: {
        username: this.createUsername,
        password: this.createPassword
      },
      show: true
    }
  },
  methods: {
    atras () {
      this.$router.push({path: '/'})
    },
    created () {
      // this.getShows()
    },
    checkLogin () {
      const formData = new FormData()
      formData.append('username', this.username)
      formData.append('password', this.password)
      const parameters = 'username=' + encodeURIComponent(this.username) + '&password=' + encodeURIComponent(this.password)
      console.log('Dintre CheckLogin')
      console.log(this.username)
      const config = {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
      const path = 'http://127.0.0.1:8000/login'
      console.log('Checklogin comprobaciones:')
      console.log(path)
      console.log(parameters)
      console.log(config)
      axios.post(path, parameters, config)
        .then((res) => {
          console.log(parameters)
          console.log('Dentro del .then')
          this.logged = true
          this.token = res.data.token
          this.$router.push({
            path: '/',
            query: {username: this.username, logged: this.logged.toString(), token: this.token}
          })
        })
        .catch((error) => {
          console.error(error)
          alert('Username or Password incorrect')
        })
    },
    initCreateForm () {
      this.creatingAccount = true
      this.addUserForm.username = null
      this.addUserForm.password = null
    },
    submitAccount () {
      if (this.createUsername.length < 8) {
        alert('La contrasseña ha de tenir com a mínim 8 caracters')
      }
      this.alertMessage = null
      this.alertMessagePwd = null
      this.addUserForm.username = this.createUsername
      this.addUserForm.password = this.createPassword
      console.log('Submit account clicked')
      const parameters = {
        username: this.createUsername,
        password: this.createPassword,
        available_money: 200.0,
        is_admin: 1,
        orders: []
      }
      this.postAccount(parameters)
    },
    postAccount (parameters) {
      const path = 'http://127.0.0.1:8000/account'
      // el post esta mal però no sé pq. le paso un
      // schema de account idk pq no va
      axios.post(path, parameters)
        .then(() => {
          alert('Account Created Successfully ')
          this.onReset()
          this.initCreateForm()
          this.$router.push({
            path: '/',
            query: {username: parameters.username, logged: this.logged.toString(), token: this.token}
          })
        })
        .catch((error) => {
          console.log(error)
          if (parameters.password.length > 24 || parameters.password.length < 8) {
            this.alertMessagePwd = 'La contraseña tiene que tener entre 8 i 24 caracteres'
          } else {
            this.alertMessage = 'El usuario ya existe'
          }
        })
    },
    onReset () {
      this.createUsername = null
      this.createPassword = null
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
      this.create_acc = !this.create_acc
    },
    getAccount () {
      const path = 'http://127.0.0.1:8000/account/' + this.createUsername
      const config = {
        headers: {
          Authorization: 'Bearer ' + this.token
        }
      }
      axios.get(path, config)
        .then((res) => {
          this.is_admin = res.data.is_admin
          this.available_money = res.data.available_money
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>

<style>

.header {
  overflow: hidden;
  padding-top: 5%;
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

.uwu {
  vertical-align: center;
  margin: 5% 20%;
  padding: 5%;
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.3);
}

.btn-add {
  background-color: #1e7e34;
  border: none;
  color: white;
  font-weight: normal;
  font-size: medium;
}

.btn-add:hover {
  background-color: #165b25;
  color: white;
  font-weight: normal;
  font-size: medium;
}
</style>

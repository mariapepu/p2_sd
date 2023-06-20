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
            <label for="inputEmail">Username</label>
            <input id="inputUsername" v-model="username" autofocus
                   class="form-control" placeholder="Username" required type="username">
          </div>
          <div class="form-label-group">
            <br>
            <label for="inputPassword">Password</label>
            <input id="inputPassword" v-model="password" class="form-control"
                   placeholder="Password" required type="password">
          </div>
          <button class="btn btn-primary" style="margin-top: 8%; width: 100%" type="submit">Iniciar sessió</button>
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
            <label for="inputEmail">Username</label>
            <input id="inputUsername" v-model="username" autofocus
                   class="form-control" placeholder="Username" required type="username">
          </div>
          <div class="form-label-group">
            <br>
            <label for="inputPassword">Password</label>
            <input id="inputPassword" v-model="password" class="form-control"
                   placeholder="Password" required type="password">
          </div>
          <button class="btn btn-primary" style="margin-top: 8%; width: 100%" type="submit">Crear Compte</button>
          <button class="btn btn-secondary" style="margin-top: 2%; width: 100%" type="button"
                  @click="ini_crear = !ini_crear">Tornar Iniciar sessió
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      message: 'Sports Matches',
      ini_crear: true,
      logged: false,
      username: null,
      password: null,
      token: null
    }
  },
  methods: {
    atras () {
      this.$router.push({path: '/'})
    }
  }
}

</script>

<style>

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

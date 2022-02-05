<template>
  <div class="container">

    <div 
      class="alert" 
      :class='alertColor' 
      role="alert"
    >{{message.value}}</div>

    <form 
      class="form-register"
      @submit.prevent="loginUser"
    >
      <div class='row row-content justify-content-center mt-2'>
        <h1 class="h3 mb-3 font-weight-normal">
          Login
        </h1>
      </div>
      <br>
      <div class='row row-content justify-content-center textfield'>
       
        <username-input 
          name="Username"
          type="text"
          autocomplete="username"
          :value="username.value"
          @inputEvent="updateFields"
        />

        <username-input 
          name="Password"
          type='password'
          autocomplete="current-password"
          :value="password.value"
          @inputEvent="updateFields"
        />
      </div>

      <div class="justify-content-center">
        <button class="btn btn-primary" type="submit">Login</button>
      </div>

      <div class="row row-content justify-content-end col-sm-10 mt-4">
        <h6>Don't have an account?</h6>
      </div>
      <div class='row row-content justify-content-end col-sm-10'>
        <router-link to="/register">Register</router-link>
      </div>
    </form>
  </div>

</template>

<script>
import axios from 'axios'
import UsernameInput from './UsernameInput.vue'

export default {
  components: { UsernameInput },
  data() {
    return {
      username:{
        value: ''
      },
      password: {
        value: ''
      },
      message: {
        value: '',
        color: ''
      },
      token: null,
    }
  },

  methods: {
    loginUser() {
      console.log("login")
      // POST REQUEST - request.username, request.password
      // flask endpoint -> axios/ajax
      const path = 'http://127.0.0.1:5000/api/login'      
            
      const config = {
        username: this.username.value,
        password: this.password.value
      }

      axios.interceptors.request.use(function (config) {
        console.log(config)
        return config
      }, function (error) {
        // Do something with request error
        return Promise.reject(error)
      })



      axios.post(path, config)
      .then(response => {
        console.log(response)
        const data = response.data
        if (response.status == 200) {
          console.log(data.userid)
          this.message.value = data.message
          this.message.color = 'success'
          this.$store.commit('tasks/setToken', data.token)
          this.$store.commit('tasks/setUser', data.userid)
          this.$store.commit('tasks/setUsername', this.username.value)
          console.log('token: ' + this.$store.state.tasks.token)
          this.$router.push('/tasks')
        }
      })
      .catch(err => {
        console.log(err)
      })
      
    },

    updateFields(payload) {
      console.log("update")
      this[payload.name] = {
        value: payload.value,
      }
    }
  },

  computed: {
    alertColor() {
      return "alert-" + this.message.color
    }
  }
}
</script>

<style scoped>

</style> 
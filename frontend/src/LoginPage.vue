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
      }
    }
  },

  methods: {
    loginUser() {
      console.log("login")
      // POST REQUEST - request.username, request.password
      // flask endpoint -> axios/ajax
      const path = 'http://127.0.0.1:5000/api/login'
      axios.post(path, {
        username: this.username,
        password: this.password
      })
      .then(response => {
        console.log(response)
        const data = response.data
        if (data.status == 200) {
          this.message.value = data.message
          this.message.color = 'success'
          this.$store.commit('tasks/setUser', this.username)
          this.$store.dispatch('tasks/save')
          console.log('user: ' + this.$store.tasks.state.username)
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
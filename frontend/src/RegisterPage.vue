<template>
  <div class="container">
    <div 
      class="alert" 
      :class='alertColor' 
      role="alert"
    >{{message.value}}</div>

    <form 
      class="form-register"
      @submit.prevent="registerUser"
    >
      <div class='row row-content justify-content-center mt-2'>
        <h1 class="h3 mb-3 font-weight-normal">
          Register
        </h1>
      </div>
      <br>
      <div class='row row-content justify-content-center textfield'>
       
        <username-input 
          name="Username"
          :value="username.value"
          type="text"
          @inputEvent="update"
        />

        <username-input 
          name="Email"
          :value="email.value"
          type="text"
          @inputEvent="update"
        />

        <username-input 
          name="Password"
          :value="password.value"
          type='password'
          @inputEvent="update"
        />

        <username-input
          name="Confirm Password"
          :value="confirm.value"
          type="password"
          @inputEvent="update"
        />
      </div>

      <div class="">
        <button class="btn btn-primary" type="submit">Register</button>
      </div>

      <div class="row row-content justify-content-end col-sm-10 mt-4">
        <h6>Already have an account?</h6>
      </div>
      <div class='row row-content justify-content-end col-sm-10'>
        <router-link to="/login">Log in</router-link>
      </div>
    </form>
  </div>

</template>

<script>
import UsernameInput from './UsernameInput.vue'
import axios from 'axios'

export default {
  components: { UsernameInput },
  data() {
    return {
      username: {
        value: '',
      },
      password: {
        value: '',
      },
      confirm: {
        value: '',
      },
      email: {
        value: '',
      },
      message: {
        value: '',
        color: ''
      }
    }
  },

  methods: {
    registerUser() {

      if (this.password == this.confirm) {
        const path = 'http://127.0.0.1:5000/api/register'
        axios.post(path, {
          username: this.username.value,
          password: this.password.value,
          email: this.email.value
        })
        .then(response => {
          console.log(response)
        })
        .catch(err => {
          console.log(err)
        })

        this.$router.push('/login')
      } else {
        this.message.value = "Passwords must match."
        this.color = 'danger'
      }
    },

    update(payload) {
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
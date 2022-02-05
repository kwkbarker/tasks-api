<template>

<nav class="navbar navbar-expand-md navbar-dark bg-dark">
    <a class="navbar-brand" href="/">ToDo</a>
    <!-- FOR USER IMPLEMENTATION WITH API -->
      
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav mr-auto">
            <li class="nav-item">
                <router-link to="/tasks" class="nav-link">Tasks</router-link>
            </li>
        </ul>

        
      <div v-if="authenticated">
        <ul class="navbar-nav">
            <li class="nav-item">
                <div class="nav-link">Welcome, {{ username }}</div>
            </li>
            <li class="nav-item">
                <div class="nav-link" @click="logout">Logout</div>
            </li>
        </ul>
      </div>
      <div v-else>
        <ul class="navbar-nav">
            <li class="nav-item">
                <router-link to="/login" class="nav-link">Login</router-link>
            </li>
            <li class="nav-item">
                <router-link to="/register" class="nav-link">Register</router-link>
            </li>
        </ul>
      </div>
    </div> 
  </nav>
  

  <router-view></router-view>

</template>

<script>


export default {
  data() {
    return {

    }
  },

  methods: {
    logout() {
      console.log('logout')
      this.$store.commit('tasks/logoutUser')
      this.$router.push('/login')
    }
  },

  computed: {
    authenticated() {
      if (this.username) {
        return true
      } else {
        return false
      }
    },

    username() {
      return this.$store.state.tasks.username
    }
  }
}
</script>

<style scoped>

</style>
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

        
      <div v-if="current_user.is_authenticated">
        <ul class="navbar-nav">
            <li class="nav-item">
                <div class="nav-link">Welcome, <router-link>{{ current_user.username }}</router-link></div>
            </li>
            <li class="nav-item">
                <button class="nav-link" @click="logout">Logout</button>
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
      current_user: Object,
    }
  },

  methods: {
    logout() {
      axios.get('http://127.0.0.1:5000/api/logout')
    }
  }
}
</script>

<style scoped>

</style>
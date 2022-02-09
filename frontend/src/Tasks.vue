<template>
  <div class="wrapper">
    <div 
      class="alert" 
      :class='alertColor' 
      role="alert"
    >{{message.value}}</div>

    <div class="tasks-list">
      <h2 class="grey">Tasks</h2>
      <div
           v-if="tasks.length > 0"
        >
          <div class="tasks"
            v-for="task in tasks"
            :key="task.id"
          >
            <task :task="task"
            @refreshTasks='refreshTasks'
            @showMessage='showMessage'
            />
          </div>
      </div>
      <div
          v-else
        >
        <h5>No tasks to show.</h5>
      </div>
    </div>
  <div class="new-task">
    <h2 class="grey">New Task</h2>
    <form @submit.prevent="addTask">
      <task-input
        v-model:title="title"
        v-model:description="description"
        v-model:importance="importance"
      />
      <button
        type="submit"
        class="btn btn-primary"
      >
        Submit
      </button>
    </form>
  </div>
  </div>
</template>

<script>

import Task from './Task.vue'
import TaskInput from './TaskInput.vue'
import axios from 'axios'
import { checkJwt } from './utils'


export default {
  components: {
    Task,
    TaskInput,
  },

  data() {
    return {
      title: null,
      description: null,
      importance: null,
      tasks: [],
      message: {
        value: '',
        color: ''
      }
    }
  },

  // // fetch tasks from local storage
  // or initialize empty storage
  mounted() {
    this.refreshTasks()
  },

  watch: {
    '$route': 'refreshTasks'
  },

  methods: {
    async addTask() {
      if (!this.title) {
        return
      }

      const newTask = {
        title: this.title,
        description: this.description,
        importance: this.importance,
        user: this.$store.state.tasks.user
      }

      const path = '/api/tasks'
      await axios({
        method: 'post',
        url: path, 
        data: newTask,
        baseURL: 'http://127.0.0.1:5000',
        headers: {
          'Authorization': `Bearer: ${this.$store.state.tasks.token}`
        }
      })
      .then(response => {
        console.log(response)
        if (response.status == 200) {
          this.message.value = response.data.message
          this.message.color = 'success'
          this.title = null
          this.description = null
          this.importance = null
          this.refreshTasks()
        }
      })
      .catch(err => {
        console.log(err)
      })

    },

    async refreshTasks() {

      if (!this.$store.state.tasks.user) {
        this.$router.push('/login')
      }

      const config = {
        username: this.$store.state.tasks.username,
        password: this.$store.state.tasks.password
      }

      // refresh expired jwt
      if (!checkJwt(this.$store.state.tasks.token)) {
        this.refreshToken()
      } else {
        console.log('valid: ' + this.$store.state.tasks.token)
      }

      const path = '/api/tasks'
      await axios({
        method: 'get',
        url: path,
        baseURL: 'http://127.0.0.1:5000',
        headers: {
          'Authorization': `Bearer: ${this.$store.state.tasks.token}`,
          'User': `${this.$store.state.tasks.user}`
        }
      })
      .then((response) => {
        console.log(response)
        if (response.data.tasks) {
          this.tasks = response.data.tasks
        }

      })
      .catch(err => {
        console.log(err)
      })

      this.title = null
      this.description = null
      this.importance = null
    },

    showMessage(newMessage) {
      this.message.value = newMessage.value
      this.message.color = newMessage.color
    },

    async refreshToken() {
      console.log('new jwt')
      const path = 'http://127.0.0.1:5000/api/login'
      const config = {
        username: this.$store.state.tasks.username,
        password: this.$store.state.tasks.password
      } 
      await axios.post(path, config)
      .then(response => {
        console.log(response)
        const data = response.data
        if (data.userid) {
          this.$store.commit('tasks/setToken', data.token)
          this.$store.commit('tasks/setUser', data.userid)
          this.$store.commit('tasks/setPassword', this.$store.state.tasks.password)
          this.$store.commit('tasks/setUsername', this.$store.state.tasks.username)
          console.log('token: ' + this.$store.state.tasks.token)
          this.$router.push('/tasks', this.message)
        } else {
          this.message.value = data.message
          this.message.color = 'danger'
        }
      })
      .catch(err => {
        console.log(err)
        return err
      })
    },

  },

  computed: {
    alertColor() {
      return "alert-" + this.message.color
    }
  }

}
</script>

<style scoped>

button {
  margin-left: 30px;
}

.wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.tasks {
  width: 100%;
}

edit-input {
  margin:0;
}

.grey {
  color: rgb(110, 110, 110);
}

h2, h5 {
  margin-left: 30px;
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>
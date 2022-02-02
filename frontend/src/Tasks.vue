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
    addTask() {
      if (!this.title) {
        return
      }

      const newTask = {
        id: this.$store.getters['tasks/nextId'],
        title: this.title,
        description: this.description,
        importance: this.importance
      }

      const path = '/api/tasks'
      axios({
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
          this.$router.push('/tasks')
        }
      })
      .catch(err => {
        console.log(err)
      })
      // this.$store.commit('tasks/addTask', newTask)
      // this.$store.dispatch('tasks/save')
      this.title = null
      this.description = null
      this.importance = null

      this.$emit('refreshTasks')
    },

    async refreshTasks() {
      const path = '/api/tasks'
      await axios({
        method: 'get',
        url: path,
        baseURL: 'http://127.0.0.1:5000',
        headers: {
          'Authorization': `Bearer: ${this.$store.state.tasks.token}`
        }
      })
      .then((response) => {
        console.log(response)
        this.tasks = response.data.tasks

      })
      .catch(err => {
        console.log(err)
      })
      // this.$store.dispatch('tasks/fetch')
      // this.tasks = data.tasks
      this.title = null
      this.description = null
      this.importance = null
    },

    showMessage(newMessage) {
      this.message.value = newMessage.value
      this.message.color = newMessage.color
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
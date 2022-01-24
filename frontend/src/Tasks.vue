<template>
  <div class="wrapper">
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
      tasks: []
    }
  },

  // // fetch tasks from local storage
  // or initialize empty storage
  mounted() {
    this.refreshTasks()
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

      const path = 'http://127.0.0.1:5000/tasks'
      axios({
        method: 'post',
        url: path, 
        data: newTask
      })
      .then(response => {
        console.log(response)
        if (response.status == 200) {
          this.message.value = response.message
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
      const path = 'http://127.0.0.1:5000/tasks'
      axios({
        url: path
      })
      .then((response) => {
        const data = response.data
        console.log(data)
      })
      .catch(err => {
        console.log(err)
      })
      // this.$store.dispatch('tasks/fetch')
      this.tasks = data.tasks
      this.title = null
      this.description = null
      this.importance = null
    },

  },

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
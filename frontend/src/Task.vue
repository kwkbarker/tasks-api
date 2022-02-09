<template>

<div class='accordion' id='accordion-tasks'>
  <div 
    class="card"
    @submit.prevent="editTask"
  >
    <div 
      class="card-header"
      :class='bgColor'
      role='tab' 
    >
      <div class="row row-content align-items-center">
        <div class='col-8 text-left'>
          <h4 class='mb-0 text-white'>
            <a 
              class='btn btn-outline-dark btn-lg collapsed'
              data-bs-toggle='collapse' 
              :data-bs-target='tabPanelTarget'
            >{{ task.title }}</a>
          </h4>
        </div>

        <div class='col-4 text-right right-buttons'>
          <button type="button" 
            class='btn btn-sm btn-outline-info'
            data-bs-toggle='modal'
            :data-bs-target='modalName'
            @click="prefill(task.id)"
          >Edit</button>
          
          <button 
            class='btn btn-sm btn-outline-dark' 
            @click="deleteClick()"
          >Done!</button>
        </div>
      </div>
      
      <div 
        role='tabpanel' 
        class='collapse text-black-50' 
        :id='tabPanelName' 
        data-parent='#accordion-tasks'
      >
        <div 
          class='card-body' 
        >{{ task.description }}</div>
      </div>
    </div>
  </div>

  <edit-input
    :task="task"
    @editTask='editTask'
  />
</div>
</template>

<script>
import TaskInput from './TaskInput.vue'
import EditInput from './EditInput.vue'
import axios from 'axios'
import { checkJwt } from './utils'

export default {
  components: {
    TaskInput,
    EditInput
  },

  props: {
    task: {
      type: Object
    },
    editTitle: String,
    editDesc: String
  },

  data() {
    return {
      newMessage: {
         value: '',
         color: ''
      }
    }
  },

  methods: {
    async editTask(newTask) {
      // Called on emit from EditInput
      const editedTask = {
        id: this.task.id,
        title: newTask.title,
        description: newTask.description,
        importance: newTask.importance
      }

      // refresh expired jwt
      if (!checkJwt(this.$store.state.tasks.token)) {
        this.refreshToken()
      } else {
        console.log('valid: ' + this.$store.state.tasks.token)
      }

      const path = 'http://127.0.0.1:5000/api/tasks'

      await axios({
        method: 'PUT',
        url: path, 
        data: editedTask,
        headers: {
          'Authorization': `Bearer: ${this.$store.state.tasks.token}`
        }
      })
      .then(response => {
        console.log(response)
        if (response.data.Authenticated) {
          this.newMessage.value = response.data.message
          this.newMessage.color = 'success'
          this.$emit('showMessage', this.newMessage)
          // this.$router.push('/tasks')
          this.$emit('refreshTasks')
        } else {
          this.refreshToken()
          this.newMessage.value = 'There was a problem. Please try again.'
          this.newMessage.color = 'danger'
          this.$emit('showMessage', this.newMessage)
        }
      })
      .catch(err => {
        console.log(err)
      })
      // this.$store.commit('tasks/editTask', editedTask)
      // this.$store.dispatch('tasks/save')
      // this.$emit('refreshTasks')
    },

    async refreshToken() {
      // refresh expired jwt
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
          console.log(data.userid)
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


    async deleteClick() {

      const path = 'http://127.0.0.1:5000/api/tasks'
      await axios({
        url: path,
        method: 'DELETE',
        data: {
          'id' :this.task.id,
        },
        headers: {
          'Authorization': `Bearer: ${this.$store.state.tasks.token}`
        }
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

      // call refreshTasks in parent component (Tasks.vue)
      this.$emit('refreshTasks')
    },

    prefill() {
      // PREFILL EDIT FIELDS WITH SAVED TASK INFO
      // Called on launch of edit modal
      document.getElementById(this.titleInputId).value = this.task.title
      document.getElementById(this.descInputId).value = this.task.description
      if (this.task.importance == "danger") {
        console.log(this.dangBtnId)
        document.getElementById(this.dangBtnId).setAttribute('checked', true)
      } else if (this.task.importance == "warning") {
        document.getElementById(this.warnBtnId).setAttribute('checked', true)
      } else if (this.task.importance == "secondary") {
        document.getElementById(this.secBtnId).setAttribute('checked', true)
      } else {
        document.getElementById(this.dangBtnId).setAttribute('checked', false)
        document.getElementById(this.warnBtnId).setAttribute('checked', false)
        document.getElementById(this.secBtnId).setAttribute('checked', false)
      }
    }

  },

  computed: {

    // compute various IDs for task elements and Bootstrap targeting values

    tabPanelName() {
      return "panel" + this.task.id
    },

    tabPanelTarget() {
      return "#" + this.tabPanelName
    },

    bgColor() {
      return "bg-" + this.task.importance
    },

    modalName() {
      return "#editWindow" + this.task.id
    },

    titleInputId() {
      if (this.task) {
        return 'title-input-field-' + this.task.id
      } else {
        return 'title-input-field-main'
      }
    },

    descInputId() {
      if (this.task) {
        return 'description-input-field-' + this.task.id
      } else {
        return 'description-input-main'
      }
    },

    dangBtnId() {
      if (this.task) {
        return 'dangBtnId-' + this.task.id
      } 
    },

    warnBtnId() {
      if (this.task) {
        return 'warnBtnId-' + this.task.id
      } 
    },

    secBtnId() {
      if (this.task) {
        return 'secBtnId-' + this.task.id
      } 
    },
    
  }
}
</script> 

<style scoped>
.task {
  border: 1px solid black;
  border-radius: 5px;
  padding-right: 10px;
  padding-left: 10px;
  margin: 10px;
  width: 100%;
}


</style>
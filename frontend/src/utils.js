export function login(path, config) {
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
}
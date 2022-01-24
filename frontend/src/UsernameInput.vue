<template>
  <div class="input">
      <label :for="name" class="label">{{ name }}</label>
      
      <input
        :type="type"
        :value="value"
        :id='name'
        :autocomplete="autocomplete"
        @input="inputEvent"
      />
    </div>
</template>

<script>

export default {
  props: {
    value: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: "text"
    },
    autocomplete: {
      type: String,
      default: "off"
    }
  },

  methods: {

    inputEvent($event) {
      this.$emit('inputEvent', {
        name: this.name.toLowerCase(),
        value: $event.target.value,
      })
    }
  }
  
}
</script>


<style scoped>
.input {
  display: flex;
  flex-direction: column;
  margin-top: 10px;
  margin-bottom: 10px;
}
.label {
  display: flex;
  justify-content: space-between;
}
.error {
  color: red;
}

input {
  box-sizing: border-box;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid silver;
  margin: 2px;
  font-size: 16px;
  width: 100%;
  cursor: pointer;
}
</style>
<template>
  <div class="contact-form">
    <h3>{{ isEdit ? 'Edit Contact' : 'Add Contact' }}</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="firstname">First Name </label>
        <input type="text" v-model="localContact.firstname" id="firstname" />
      </div>
      <div class="form-group">
        <label for="lastname">Last Name </label>
        <input type="text" v-model="localContact.lastname" id="lastname" />
      </div>
      <div class="form-group">
        <label for="address">Address </label>
        <input type="text" v-model="localContact.address" id="address" />
      </div>
      <div class="form-group">
        <label for="company">Company </label>
        <input type="text" v-model="localContact.company" id="company" />
      </div>
      <div class="form-group">
        <label for="phone">Phone </label>
        <input type="text" v-model="localContact.phone" id="phone" />
      </div>
      <button class="ContactFormButton" type="submit">{{ isEdit ? 'Update' : 'Add' }}</button>
      <button class="ContactFormButton" type="button" @click="$emit('cancel')">Cancel</button>
    </form>
  </div>
</template>

<script>
export default {
  props: {
    contact: Object,
    isEdit: Boolean
  },
  data() {
    return {
      localContact: { ...this.contact }
    };
  },
  watch: {
    contact(newVal) {
      this.localContact = { ...newVal };
    }
  },
  methods: {
    handleSubmit() {
      this.$emit('submit', this.localContact);
    }
  }
};
</script>

<style scoped>
.contact-form {
  background-color: #fff;
  padding: 0px;
  margin:2px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.5s ease-in-out;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0px;
  text-align: left;
  margin-left: 30px;
}

input[type="text"] {
  width: 80%;
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.5rem 1rem;
  background-color: #4a90e2;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 0.5rem;
}

button:hover {
  background-color: #357ab7;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>

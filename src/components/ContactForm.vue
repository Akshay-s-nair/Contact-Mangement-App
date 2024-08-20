<!-- <template>
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
</style> -->


<!-- need to check. above is working model -->

<template>
  <div class="contact-form">
    <h3>{{ isEdit ? 'Edit Contact' : 'Add Contact' }}</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="firstname">First Name</label>
        <input type="text" v-model="localContact.firstname" id="firstname" />
        <div v-if="errors.firstname" class="error">{{ errors.firstname }}</div>
      </div>
      <div class="form-group">
        <label for="lastname">Last Name</label>
        <input type="text" v-model="localContact.lastname" id="lastname" />
        <div v-if="errors.lastname" class="error">{{ errors.lastname }}</div>
      </div>
      <div class="form-group">
        <label for="address">Address</label>
        <input type="text" v-model="localContact.address" id="address" />
        <div v-if="errors.address" class="error">{{ errors.address }}</div>
      </div>
      <div class="form-group">
        <label for="company">Company</label>
        <input type="text" v-model="localContact.company" id="company" />
        <div v-if="errors.company" class="error">{{ errors.company }}</div>
      </div>
      <div class="form-group">
        <label for="phone">Phone</label>
        <input type="text" v-model="localContact.phone" id="phone" />
        <div v-if="errors.phone" class="error">{{ errors.phone }}</div>
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
      localContact: { ...this.contact },
      errors: {}
    };
  },
  watch: {
    contact(newVal) {
      this.localContact = { ...newVal };
    }
  },
  methods: {
    validate() {
      this.errors = {};

      // Validate that fields are not empty
      if (!this.localContact.firstname || this.localContact.lastname.trim()=='') {
        this.errors.firstname = 'First name is required.';
      }
      if (!this.localContact.lastname || this.localContact.lastname.trim()=='') {
        this.errors.lastname = 'Last name is required.';
      }
      if (!this.localContact.phone) {
        this.errors.phone = 'Phone number is required.';
      }
      if (this.localContact.firstname && this.localContact.firstname.length > 15) {
        this.errors.firstname = 'firstname must be of 15 characters or less.';
      }
      if (this.localContact.lastname && this.localContact.lastname.length > 15) {
        this.errors.lastname = 'lastname must be of 15 characters or less.';
      }
      if (this.localContact.address && this.localContact.address.length > 20) {
        this.errors.address = 'Address must be 20 characters or less.';
      }
      if (this.localContact.company && this.localContact.company.length > 20) {
        this.errors.company = 'Company must be 20 characters or less.';
      }
      // try{
      //   this.localContact.phone=parseInt(this.localContact.phone);
      // }
      // catch{
      //   this.errors.phone = 'Phone number is not valied';
      // }
      if (this.localContact.phone) {
          if (this.localContact.phone.length !== 10) {
              this.errors.phone = 'Phone number must be of ten digits';
          } else if (!/^\d{10}$/.test(this.localContact.phone)) {
              this.errors.phone = 'Phone number must contain only digits';
          }
      }

      return Object.keys(this.errors).length === 0;
    },
    handleSubmit() {
      if (this.validate()) {
        this.$emit('submit', this.localContact);
      }
    }
  }
};
</script>
<style scoped>
.contact-form {
  background-color: #fff;
  padding: 0px;
  margin: 2px;
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

.error {
  color: red;
  font-size: 0.875rem;
  margin:5px;
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


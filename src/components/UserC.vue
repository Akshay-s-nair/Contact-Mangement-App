<template>
    <div class="user-form">
      <h3>Edit User Details</h3>
      <form @submit.prevent="updateUser">
        <div class="form-group">
          <label for="firstname">First Name:</label>
          <input type="text" v-model="user.firstname" id="firstname" />
        </div>
        <div class="form-group">
          <label for="lastname">Last Name:</label>
          <input type="text" v-model="user.lastname" id="lastname" />
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" v-model="user.email" id="email" />
        </div>
        <div class="form-group">
          <label for="phone">Phone:</label>
          <input type="text" v-model="user.phone" id="phone" />
        </div>
        <div class="form-group">
          <label for="dob">Date of Birth:</label>
          <input type="date" v-model="user.dob" id="dob" />
        </div>
        <div class="form-group">
          <label for="gender">Gender:</label>
          <select v-model="user.gender" id="gender">
            <option value="">Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>
        <div class="form-group">
          <label for="address">Address:</label>
          <input type="text" v-model="user.address" id="address" />
        </div>
        <div class="form-group">
          <label for="profile_picture">Profile Picture:</label>
          <input type="file" @change="onFileChange" id="profile_picture" />
        </div>
        <button type="submit">Update</button>
        <button type="button" @click="cancelEdit">Cancel</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        user: {
          firstname: '',
          lastname: '',
          email: '',
          phone: '',
          dob: '',
          gender: '',
          address: '',
          profile_picture: null
        },
        file: null
      };
    },
    created() {
      this.fetchUserDetails();
    },
    methods: {
      async fetchUserDetails() {
        try {
          const response = await axios.get('http://localhost:5000/users', {
            headers: { Authorization: localStorage.getItem('token') }
          });
          this.user = response.data;
        } catch (error) {
          console.error('Error fetching user details:', error.response.data.error);
        }
      },
      async updateUser() {
        const formData = new FormData();
        for (const key in this.user) {
          formData.append(key, this.user[key]);
        }
        if (this.file) {
          formData.append('profile_picture', this.file);
        }
  
        try {
          const response = await axios.put('http://localhost:5000/users', formData, {
            headers: {
              Authorization: localStorage.getItem('token'),
              'Content-Type': 'multipart/form-data'
            }
          });
          console.log(response.data.message);
          this.$emit('updateSuccess');
        } catch (error) {
          console.error('Error updating user details:', error.response.data.error);
        }
      },
      onFileChange(event) {
        this.file = event.target.files[0];
      },
      cancelEdit() {
        this.$emit('cancel-edit');
      }
    }
  };
  </script>
  
  <style scoped>
  .user-form {
    background-color: #fff;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
  }
  
  input[type="text"],
  input[type="email"],
  input[type="date"],
  select {
    width: 100%;
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
  </style>
  
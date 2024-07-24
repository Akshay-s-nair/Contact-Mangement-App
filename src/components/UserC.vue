<template>
    <div class="user-form">
      <h3>User Details</h3>
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
          <div class="profileImg">
            <img v-if="img!=='null'" class="profile-picture" :src="`/profile_pictures/${img}`" alt="Profile Picture" />
          </div>
          <label for="profile_picture">Profile Picture:</label>
          <input type="file" @change="onFileChange" id="profile_picture" />
        </div>
        <div class="msg">{{ msg }}</div>
        <div class="butt">
          <button type="submit">Update</button>
          <button type="button" @click="cancelEdit">Cancel</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
import { mapState } from 'vuex';
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
        file: null,
        msg:''
      };
    },
    created() {
      this.fetchUserDetails();
    },
    computed: {
    ...mapState(['img'])
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
          this.msg="Information Updated Successfully"
          setTimeout(() => {
            this.msg=''
            this.$emit('cancel-edit');
            }, 2000);
          this.$emit('updateSuccess');
        } catch (error) {
          this.msg="Error updating user details"
          setTimeout(() => {
            this.msg=''
            }, 1500);
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
    background-color: #da5b01;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin: 0.5rem;
  }
  
  button:hover {
    background-color: #357ab7;
  }
  .msg{
    text-align: center;
    height: 20px;
    color:#da5b01;
    font-weight: 600;
  }
  .butt{
    display: flex;
  }
  </style>
  
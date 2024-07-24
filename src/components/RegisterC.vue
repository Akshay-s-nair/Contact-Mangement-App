<template>
  <div class="loginnav">
    <router-link class="home-link" to="/"><img src="ContactEase2.png" alt="ContactEase Logo" class="logoLogin"></router-link>
    <router-link class="home-link" to="/">Home</router-link>
  </div>
  <div class="register">
    <h1 class="welcomeText">Get on Board</h1>
    <div class="formHead">
      <div class="formBody">
        <h2>Register</h2>
        <form @submit.prevent="handleRegister">
          <div class="forminputs"></div>
          <div class="form-group">
            <label for="firstname">Firstname<span>*</span></label>
            <input type="text" v-model="form.firstname" id="firstname" />
            <p v-if="validationErrors" class="error">{{ validationErrors.firstname }}</p>
          </div>

          <div class="form-group">
            <label for="lastname">Lastname<span>*</span></label>
            <input type="text" v-model="form.lastname" id="lastname" />
            <p v-if="validationErrors" class="error">{{ validationErrors.lastname }}</p>
          </div>

          <div class="form-group">
            <label for="email">Email<span>*</span></label>
            <input type="text" v-model="form.email" id="email" />
            <p v-if="validationErrors" class="error">{{ validationErrors.email }}</p>
          </div>

          <div class="form-group">
            <label for="password">Password<span>*</span></label>
            <input type="password" v-model="form.password" id="password" />
            <p v-if="validationErrors" class="error">{{ validationErrors.password }}</p>
          </div>

          <div class="form-group">
            <label for="confirmpassword">Confirm Password<span>*</span></label>
            <input type="password" v-model="form.confirmpassword" id="confirmpassword" />
            <p v-if="validationErrors" class="error">{{ validationErrors.confirmpassword }}</p>
          </div>

          <div class="form-group">
            <label for="phone">Phone</label>
            <input type="text" v-model="form.phone" id="phone" />
            <p v-if="validationErrors" class="error">{{ validationErrors.phone }}</p>
          </div>      
          <div class="form-group">
            <label for="profile">Date Of Birth</label>
            <input
                type="date"
                v-model="form.date"
            />
          </div>
          
          <div class="form-group">
            <label for="">Gender</label>
            <select>
              <option disabled value="">Select Gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div class="form-group">
            <label for="address">Address</label>
            <input type="text" v-model="form.address" id="address" />
            <p v-if="validationErrors" class="error">{{ validationErrors.address }}</p>
          </div> 

          <div class="form-group">
            <label for="profile">Profile Photo</label>
            <input
                type="file"
                @change="handleFileUpload"
                id="profile"
              />
          </div>
          
            <!-- <p v-if="validationErrors" class="error">{{ validationErrors }}</p> -->
          
          <div class="error-div">
            <p v-if="success" class="success">{{ success }}</p>
            <p v-if="error" class="error">{{ error }}</p>
          </div>
          <button type="submit" class="button-LoginRegister">Register</button>
        </form>
        <hr>
        <div class="registerFromLogin">
          <p>Already have an Account? <router-link class="LRLinks"  style="color:#da5b01;" to="/login">Signin</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  data() {
    return {
      form: {
        firstname: '',
        lastname: '',
        email: '',
        password: '',
        confirmpassword: '',
        phone: '',
        dob: '',
        gender: '',
        address: '',
        profile_picture: null
      }
    };
  },
  computed: {
    ...mapState(['error', 'success', 'validationErrors'])
  },
  watch: {
    success(newValue) {
      if (newValue) {
        this.redirectAfterSuccess();
      }
    }
  },
  methods: {
    ...mapActions(['register']),
    handleFileUpload(event) {
      this.form.profile_picture = event.target.files[0];
    },
    handleRegister() {
      const formData = new FormData();
      for (const key in this.form) {
        formData.append(key, this.form[key]);
      }
      this.register(formData);
    },
    redirectAfterSuccess() {
      setTimeout(() => {
        this.$router.push('/login');
      }, 1100); // 1 second delay
    }
  }
};
</script>

<style scoped>
@import "./LoginRegister.css";
span{
  color:red;
}
label {
    display: block;
    margin-bottom: 5px;
  }

  input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
  }

  .error-div {
    margin-top: 10px;
  }

  button {
    background-color:#ec7c2c;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
  }

  button:hover {
    background-color: #e86100;
  }
</style>
<template>
    <div class="loginnav">
      <router-link class="home-link" to="/"><img src="ContactEase2.png" alt="ContactEase Logo" class="logoLogin"></router-link>
      <router-link class="home-link" to="/">Home</router-link>
    </div>
    <div class="login">
      <div class="formHead">
        <div class="formBody">
          <h2 class="name-LoginRegister">Forgot Password</h2>
          <form >
            <div class="form-group">
              <label for="email">Enter your mobile phone number:</label>
              <input type="text" id="email" />
            </div>
            <div class="form-group">
              <label for="password">Enter your Email ID:</label>
              <input type="password" id="password" />
            </div>
            <div class="error-div">
              <p v-if="success" class="success">{{ success }}</p>
              <p v-if="error" class="error">{{ error }}</p>
            </div>
            <button class="button-LoginRegister" type="submit">Login</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  
  </script>
  
  
  <style scoped>
  </style>
  
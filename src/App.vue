<template>
  <div id="app">
    <!-- <nav>
      <router-link to="/">Home</router-link>
      <router-link v-if="!isAuthenticated" to="/register">Register</router-link>
      <router-link v-if="!isAuthenticated" to="/login">Login</router-link>
      <router-link v-if="isAuthenticated" to="/contacts">Contacts</router-link>
      <button v-if="isAuthenticated" @click="confirmLogout">Logout</button>
      <span class="welcome" v-if="isAuthenticated">Welcome, {{ user }}</span>
    </nav> -->
    <div class="content-wrapper">
      <router-view></router-view>
    </div>

    <!-- Logout Confirmation Modal -->
    <LogoutConfirmationModal v-if="showLogoutModal" />
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import LogoutConfirmationModal from './components/LogoutConfirmationModal.vue';
import './App.css'

export default {
  components: {
    LogoutConfirmationModal
  },
  computed: {
    ...mapState(['user','token', 'showLogoutModal']),
    isAuthenticated() {
      return !!this.token;
    }
  },
  methods: {
    ...mapActions(['toggleLogoutModal']),
    confirmLogout() {
      this.toggleLogoutModal(true);
    }
  }
};
</script>

<style scoped>

button{
    padding: 0rem 0rem;
    background-color: rgba(139, 69, 19, 0);
    color: #fff;
    cursor: pointer;
}
button:hover{
  background-color: rgba(139, 69, 19, 0);
  color: #ff7878d4;
}




</style>
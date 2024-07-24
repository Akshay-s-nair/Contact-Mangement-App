<template>
  <section v-if="!isAuthenticated" class="call-to-action">
      <h2>Ready to Get Started?</h2>
      <button @click="goToLogin" class="btn-try-now">Try Now</button>
    </section>
    <section v-if="isAuthenticated" class="call-to-action">
      <h4>Seems like Your Contacts are waiting for you..</h4>
      <h2>Need to Get back to your contacts?</h2>
      <button @click="goToContacts" class="btn-try-now">Go to Contacts</button>
    </section>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      wish: ''
    };
  },
  computed: {
    ...mapState(['user','redirectMessage', 'error', 'success','token', 'showLogoutModal']),
    isAuthenticated() {
      return !!this.token;
    }
  },
  methods: {
    goToLogin() {
      this.$router.push('/login');
    },
    goToContacts(){
      this.$router.push('/contacts')
    },
  },
};
</script>

<style>

</style>
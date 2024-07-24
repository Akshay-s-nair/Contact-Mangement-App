<script>
import { mapState, mapMutations } from 'vuex';
import LogoutConfirmationModal from '../components/LogoutConfirmationModal.vue';
import HomeC1 from '../components/HomeC1.vue';
import HomeC2 from '../components/HomeC2.vue';
import HomeC3 from '../components/HomeC3.vue';
import HomeC4 from '../components/HomeC4.vue';

export default {
  data() {
    return {
      wish: ''
    };
  },
  components: {
    LogoutConfirmationModal,
    HomeC1,
    HomeC2,
    HomeC3,
    HomeC4
  },
  computed: {
    ...mapState(['user', 'redirectMessage', 'error', 'success', 'token', 'showLogoutModal']),
    isAuthenticated() {
      return !!this.token;
    }
  },
  watch: {
    redirectMessage(newMessage) {
      if (newMessage) {
        setTimeout(() => {
          this.clearRedirectMessage();
        }, 3000);
      }
    }
  },
  methods: {
    ...mapMutations(['clearRedirectMessage', 'toggleLogoutModal']),
    getTime() {
      const d = new Date();
      const hours = d.getHours();
      if (hours < 12) {
        this.wish = "Good Morning";
      } else if (hours >= 12 && hours < 18) {
        this.wish = "Good Afternoon";
      } else {
        this.wish = "Good Evening";
      }
    },
    confirmLogout() {
      this.toggleLogoutModal(true);
    },
    handleScroll() {
      const heroSection = this.$refs.heroSection;
      const stickyNav = this.$refs.stickyNav;
      const heroHeight = heroSection ? heroSection.offsetHeight : 0;
      if (window.scrollY >= heroHeight) {
        stickyNav.classList.remove('hidden');
        stickyNav.classList.add('visible');
      } else {
        stickyNav.classList.remove('visible');
        stickyNav.classList.add('hidden');
      }
    }
  },
  mounted() {
    this.getTime();
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  }
};
</script>

<template>
  <div class="home">
    <section ref="heroSection" class="hero">
      
      <img src="ContactEase2.png" alt="ContactEase Logo" class="logo">
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>
      <h1 v-if="!isAuthenticated" class="welcometext">Welcome to ContactEase</h1>
      <p v-if="!isAuthenticated" class="para">You are Experiencing ContactEase, a modern, user-friendly application designed to streamline and enhance your contact management experience. Whether you're an individual seeking to organize personal contacts or a professional managing a large network, ContactEase offers a comprehensive set of features to meet your needs.</p>
      <h1 v-if="isAuthenticated" class="welcometext welcometextAuth">{{ wish }}, {{ user }}</h1>
      <p v-if="isAuthenticated" class="para">We are providing a modern, user-friendly application designed to streamline and enhance your contact management experience. Whether you're an individual seeking to organize personal contacts or a professional managing a large network, ContactEase offers a comprehensive set of features to meet your needs.</p>
      <div class="navs">
        <router-link class="links" to="/">Home</router-link>
        <router-link class="links" v-if="!isAuthenticated" to="/register">Register</router-link>
        <router-link class="links" v-if="!isAuthenticated" to="/login">Login</router-link>
        <router-link class="links" v-if="isAuthenticated" to="/contacts">Contacts</router-link>
        <button class="logoutbut" v-if="isAuthenticated" @click="confirmLogout">Logout</button>
      </div>
    </section>
    
    <div ref="stickyNav" class="sticky-nav hidden">
      <div class="sec1">
        <router-link class="links" to="/"><img src="ContactEase2.png" alt="ContactEase Logo" class="sticky-logo"></router-link>
      </div>
      <div class="sec2">
        <router-link class="links" to="/">Home</router-link>
        <router-link class="links" v-if="!isAuthenticated" to="/register">Register</router-link>
        <router-link class="links loginbut" v-if="!isAuthenticated" to="/login">Login</router-link>
        <router-link class="links" v-if="isAuthenticated" to="/contacts">Contacts</router-link>
        <button class="logoutbut logoutbut-nav" v-if="isAuthenticated" @click="confirmLogout">Logout</button>
      </div>
    </div>

    <HomeC1/>
    <HomeC2/>
    <HomeC3/>
    <HomeC4/>
  </div>

  <div class="logout">
    <LogoutConfirmationModal v-if="showLogoutModal" />
  </div>
  <!-- <ul class="social-icons">
      <li><a href="#"><i class="fa fa-instagram"></i></a></li>
      <li><a href="#"><i class="fa fa-twitter"></i></a></li>
      <li><a href="#"><i class="fa fa-linkedin"></i></a></li>
      <li><a href="#"><i class="fa fa-codepen"></i></a></li>
    </ul> -->
</template>


<style scoped>
@import './Home.css';
.welcometextAuth{
  margin-bottom: 80px;
}
/* .social-icons {
  padding: 0;
  list-style: none;
  margin: 1em;
}

.social-icons li {
  display: inline-block;
  margin: 0.15em;
  position: relative;
  font-size: 1em;
}

.social-icons i {
  color: #fff;
  position: absolute;
  top: 0.95em;
  left: 0.96em;
  transition: all 265ms ease-out;
}

.social-icons a {
  display: inline-block;
}

.social-icons a:before {
  transform: scale(1);
  -ms-transform: scale(1);
  -webkit-transform: scale(1);
  content: " ";
  width: 45px;
  height: 45px;
  border-radius: 100%;
  display: block;
  background: linear-gradient(45deg, #ff003c, #da6a1a);
  transition: all 265ms ease-out;
}

.social-icons a:hover:before {
  transform: scale(0);
  transition: all 265ms ease-in;
}

.social-icons a:hover i {
  transform: scale(2.2);
  -ms-transform: scale(2.2);
  -webkit-transform: scale(2.2);
  color: #ff003c;
  background: -webkit-linear-gradient(45deg, #ff003c, #c648c8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  transition: all 265ms ease-in;
} */
</style>
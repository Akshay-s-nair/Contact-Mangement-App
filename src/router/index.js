import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/HomeV.vue';
import Register from '../components/RegisterC.vue';
import Login from '../components/LoginC.vue';
import UnWantedVisit from '../components/UnWantedVisit.vue';
import Contacts from '../views/ContactsV.vue';
import ForgotPassword from '../views/ForgotPassword.vue';
import store from '../store'; // Adjust the path as needed

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresGuest: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/contacts',
    name: 'Contacts',
    component: Contacts,
    meta: { requiresAuth: true }
  },
  {
    path: '/forgot',
    name: 'Forgot Password',
    component: ForgotPassword
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'UnWantedVisit',
    component:UnWantedVisit
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresGuest) && store.state.token) {
    if (from.name === null) {
      // If navigation is triggered by typing in the URL, set the redirect message
      store.commit('setRedirectMessage', 'You need to log out first.');
    }
    next({ name: 'Home' });
  } else if (to.matched.some(record => record.meta.requiresAuth) && !store.state.token) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;

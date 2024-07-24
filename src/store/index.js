import { createStore } from 'vuex';
import axios from 'axios';
import router from '../router';

const store = createStore({
  state: {
    error: null,
    success: null,
    validationErrors: {},
    token: localStorage.getItem('token') || '',
    user: localStorage.getItem('user') || null,
    redirectMessage: null,
    showLogoutModal: false,
    contacts: [],
    search: '', 
    sort: 'id', 
    sortOrder: 'asc',
    total_count: 0,
    currentPage: 1, // Added currentPage state
    perPage: 10, // Added perPage state
    img:localStorage.getItem('img') || null,
  },
  mutations: {
    setError(state, error) {
      state.error = error;
    },
    setSuccess(state, message) {
      state.success = message;
    },
    setValidationErrors(state, errors) {
      state.validationErrors = errors;
    },
    clearMessages(state) {
      state.error = null;
      state.success = null;
      state.validationErrors = {};
    },
    setUser(state, user) {
      state.user = user;
      localStorage.setItem('user', user);
    },
    setImg(state,img) {
      state.img=img
      localStorage.setItem('img', img);
      console.log('mutation',state.img)
    },
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    clearUserData(state) {
      state.token = '';
      state.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      localStorage.removeItem('img');
    },
    setRedirectMessage(state, message) {
      state.redirectMessage = message;
    },
    clearRedirectMessage(state) {
      state.redirectMessage = null;
    },
    toggleLogoutModal(state, show) {
      state.showLogoutModal = show;
    },
    setContacts(state, contacts) {
      state.contacts = contacts;
    },
    clearContacts(state) {
      state.contacts = [];
    },
    addContact(state, contact) {
      state.contacts.push(contact);
    },
    editContact(state, updatedContact) {
      const index = state.contacts.findIndex(contact => contact.id === updatedContact.id);
      if (index !== -1) {
        state.contacts.splice(index, 1, updatedContact);
      }
    },
    deleteContact(state, contactId) {
      state.contacts = state.contacts.filter(contact => contact.id !== contactId);
    },
    setSearch(state, search) {  
      state.search = search;
    },
    setSort(state, sort) {  
      state.sort = sort;
    },
    setSortOrder(state, sortOrder) {  
      state.sortOrder = sortOrder;
    },
    setTotal_count(state, total_count) {
      state.total_count = total_count;
    },
    setCurrentPage(state, page) { // Added setCurrentPage mutation
      state.currentPage = page;
    }
  },
  actions: {
    async register({ commit, dispatch }, formData) {
      try {
        commit('clearMessages');

        const errors = {};
        if (!formData.get('firstname')) errors.firstname = 'First name is required';
        if (!formData.get('lastname')) errors.lastname = 'Last name is required';
        if (!formData.get('email')) {
          errors.email = 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(formData.get('email'))) {
          errors.email = 'Email is invalid';
        }
        if (!formData.get('password')) {
          errors.password = 'Password is required';
        } else if (formData.get('password').length < 6) {
          errors.password = 'Password must be at least 6 characters long';
        }
        if (!formData.get('confirmpassword')) {
          errors.confirmpassword = 'Confirm password is required';
        } else if (formData.get('confirmpassword') !== formData.get('password')) {
          errors.confirmpassword = 'Passwords do not match';
        }
        if (!formData.get('phone')) {
          errors.phone = 'Phone number is required';
        } else if (!/^\d+$/.test(formData.get('phone'))) {
          errors.phone = 'Phone number is invalid';
        }

        if (Object.keys(errors).length > 0) {
          commit('setValidationErrors', errors);
          return;
        }

        const response = await axios.post('http://localhost:5000/register', formData);
        commit('setSuccess', response.data.message);
        dispatch('clearMessagesAfterDelay');
      } catch (error) {
        commit('setError', error.response.data.error || 'An error occurred');
        dispatch('clearMessagesAfterDelay');
      }
    },
    async login({ commit, dispatch }, credentials) {
      try {
        commit('clearMessages');
        const response = await axios.post('http://localhost:5000/login', credentials);
        commit('setToken', response.data.token);
        commit('setUser', response.data.username);
        commit('setImg',response.data.img);
        console.log('index',response.data.img)
        commit('setSuccess', 'Login successful');
        dispatch('fetchContacts');
        dispatch('clearMessagesAfterDelay');
        setTimeout(() => {
          router.push({ name: 'Contacts' });
        }, 1000);
      } catch (error) {
        commit('setError', error.response.data.error || 'An error occurred');
        dispatch('clearMessagesAfterDelay');
      }
    },
    logout({ commit }) {
      commit('clearUserData');
      commit('toggleLogoutModal', false);
      router.push({ name: 'Home' });
    },
    clearMessagesAfterDelay({ commit }) {
      setTimeout(() => {
        commit('clearMessages');
      }, 1000);
    },
    toggleLogoutModal({ commit }, show) {
      commit('toggleLogoutModal', show);
    },
    async fetchContacts({ commit, state }) {
      try {
        const response = await axios.get('http://localhost:5000/contacts', {
          headers: { Authorization: localStorage.getItem('token') },
          params: { 
            search: state.search, 
            sort: state.sort, 
            sort_order: state.sortOrder,
            page: state.currentPage, // Include page parameter
            per_page: state.perPage // Include per_page parameter
          }
        });
        commit('setContacts', response.data.contacts);
        commit('setTotal_count', response.data.total_count);
      } catch (error) {
        commit('setError', error.response.data.error);
      }
    },
    async addContact({ commit, dispatch }, contactData) {
      try {
        const response = await axios.post('http://localhost:5000/contacts', contactData, {
          headers: { Authorization: localStorage.getItem('token') }
        });
        commit('addContact', response.data);
        dispatch('fetchContacts');
        commit('setSuccess', 'Contact added successfully');
        dispatch('clearMessagesAfterDelay');
      } catch (error) {
        // commit('setError', error.response.data.error || 'An error occurred');
      }
    },
    async updateContact({ commit, dispatch }, contact) {
      try {
        await axios.put(`http://localhost:5000/contacts/${contact.id}`, contact, {
          headers: { Authorization: localStorage.getItem('token') }
        });
        dispatch('fetchContacts');
        commit('setSuccess', 'Contact updated successfully');
        dispatch('clearMessagesAfterDelay');
      } catch (error) {
        commit('setError', error.response.data.error || 'An error occurred');
        dispatch('clearMessagesAfterDelay');
      }
    },
    async deleteContact({ commit, dispatch }, contactId) {
      try {
        await axios.delete(`http://localhost:5000/contacts/${contactId}`, {
          headers: { Authorization: localStorage.getItem('token') }
        });
        dispatch('fetchContacts');
        commit('setSuccess', 'Contact Deleted successfully');
        dispatch('clearMessagesAfterDelay');
      } catch (error) {
        commit('setError', error.response.data.error || 'An error occurred');
        dispatch('clearMessagesAfterDelay');
      }
    },
    setSearch({ commit, dispatch }, search) {
      commit('setSearch', search);
      dispatch('fetchContacts');
    },
    setSort({ commit, dispatch }, sort) {
      commit('setSort', sort);
      dispatch('fetchContacts');
    },
    setSortOrder({ commit, dispatch }, sortOrder) {
      commit('setSortOrder', sortOrder);
      dispatch('fetchContacts');
    },
    setCurrentPage({ commit, dispatch }, page) { // Added setCurrentPage action
      commit('setCurrentPage', page);
      dispatch('fetchContacts');
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    user: state => state.user,
    contacts: state => state.contacts,
  }
});

export default store;

<template>
    <div class="modal-overlay">
      <div class="modal">
        <h3 v-if="!redirecting">Are you sure you want to logout?</h3>
        <div v-if="!redirecting" class="modal-buttons">
          <button @click="confirmLogout">Yes</button>
          <button @click="cancelLogout">No</button>
        </div>
        <div v-if="redirecting" class="redirecting-message">
          <h3>Redirecting</h3>
          You will be back to home page in {{ counter }} seconds...
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex';
  
  export default {
    data() {
      return {
        redirecting: false
      };
    },
    methods: {
      ...mapActions(['deleteContact', 'toggleLogoutModal']),
      confirmLogout() {
        this.redirecting = true;
        const countdown = setInterval(() => {
          this.counter -= 1;
          if (this.counter === 0) {
            clearInterval(countdown);
            this.logout();
          }
        }, 1000);
      },
      cancelLogout() {
        this.toggleLogoutModal(false);
      }
    }
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
  }
  
  button {
    padding: 0.5rem 1rem;
    margin: 0.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:first-of-type {
    background-color: #4a90e2;
    color: white;
  }
  
  button:last-of-type {
    background-color: #f44336;
    color: white;
  }
  
  button:hover {
    opacity: 0.8;
  }
  </style>
  
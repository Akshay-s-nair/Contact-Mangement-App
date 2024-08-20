<template>
    <div class="modal-overlay">
      <div class="modal">
        <h3>Are you sure you want to Delete this Contact?</h3>
        <div class="modal-buttons">
          <button @click="confirmLogout">Yes</button>
          <button @click="cancelLogout">No</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex';
  
  export default {
    data() {
      return {
      };
    },
    methods: {
      ...mapActions(['deleteContact', 'toggleDeleteBut']),
      confirmLogout() {
            this.deleteContact();
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
  
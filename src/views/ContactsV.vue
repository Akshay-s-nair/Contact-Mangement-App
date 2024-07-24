<template>
  <nav class="ContactsNav">
    <img src="ContactEase2.png" alt="ContactEase Logo" class="logoInContacts">
    <p class="welcomeMob">Welcome, {{ user }}</p>
  </nav>
  <div class="search-filter-nav">
    <input type="text" v-model="search" @input="handleSearch" placeholder="Search contacts..." class="form-control me-2">
    <select v-model="sort" @change="handleSort" class="form-select me-2">
      <option value="id" disabled>Sort</option>
      <option value="id">Date</option>
      <option value="name">Name</option>
    </select>
    <select v-model="sortOrder" @change="handleSortOrder" class="form-select me-2">
      <option value="asc" disabled>Order</option>
      <option value="asc">Ascending ↑</option>
      <option value="desc">Descending ↓</option>
    </select>
    <!-- <button class="btn btn-primary" @click="$emit('toggle-add-form')">
      Add Contact
    </button> -->
  </div>
  <nav class="ContactsNav">
  </nav>
  
  <div class="contact-management">
    <!-- Sidebar -->
    <div :class="['sidebarmain', { expanded: isSidebarExpanded }]">
      <ContactsSidebar
        @submit="handleSubmit"
        @cancel="handleCancel"
        @edit-contact="editContact"
        @show-user="showUserDetails"
        @toggle-sidebar="toggleSidebar"
        ref="sidebar"
      />
    </div>

    <!-- Main Content -->
    <div class="main-content-container">
      <component :is="currentView"
        @edit-contact="editContact"
        @toggle-add-form="toggleAddForm"
        @user-updated="showContactsMain"
        @cancel-edit="showContactsMain">
      </component>
    </div>
  </div>
</template>

<script>
import ContactsSidebar from '@/components/ContactsSidebar.vue';
import ContactsMain from '@/components/ContactsMain.vue';
import UserC from '@/components/UserC.vue';
import { mapState, mapActions } from 'vuex';

export default {
  components: {
    ContactsSidebar,
    ContactsMain,
    UserC
  },
  data() {
    return {
      search: '',
      sort: 'id',
      sortOrder: 'asc',
      isMobileView: window.innerWidth <= 768,
      currentView: 'ContactsMain', // Initial view
      isSidebarExpanded: false // State to manage sidebar expansion
    };
  },
    computed: {
    ...mapState(['user', 'token', 'contacts', 'error', 'success', 'showLogoutModal'])
  },
  methods: {
    handleResize() {
      this.isMobileView = window.innerWidth <= 768;
    },
    ...mapActions(['addContact', 'updateContact', 'setSearch', 'setSort', 'setSortOrder']),
    async handleSubmit(contact) {
      if (contact.id) {
        await this.updateContact(contact);
      } else {
        await this.addContact(contact);
      }
    },
    handleCancel() {},
    editContact(contact) {
      this.$refs.sidebar.editContact(contact);
    },
    toggleAddForm() {
      this.$refs.sidebar.toggleAddForm();
    },
    showUserDetails() {
      this.currentView = 'UserC';
    },
    showContactsMain() {
      this.currentView = 'ContactsMain';
    },
    toggleSidebar(expanded) {
      this.isSidebarExpanded = expanded;
    },handleSearch() {
      this.setSearch(this.search);
    },
    handleSort() {
      this.setSort(this.sort);
    },
    handleSortOrder() {
      this.setSortOrder(this.sortOrder);
    }
  },
  created() {
    this.$store.dispatch('fetchContacts');
  },
};
</script>

<style scoped>
.contact-management {
  display: flex;
  height: 750px;
  animation: fadesIn 0.5s ease-in-out;
}

.sidebarmain {
  width: 30%;
  bottom: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 20px;
  background-color:#f5f5f5;
  transition: width 0.3s;
}

.sidebarmain.expanded {
  width: 5000px;
}

.main-content-container {
  margin-left: 1%; /* Adjust margin to match sidebar width */
  width: 75%;
  padding: 20px;
  overflow-y: auto;
  overflow-x: hidden;
  height: calc(100vh - 60px);
}

@keyframes fadesIn {
  0%{
    opacity: 0.8;
  }
  100% {
    opacity: 1;
  }
}

@media (max-width: 768px) {
.logoInContacts{
  width: 130px;
}
.contact-management{
  height: 550px;
}
.main-content-container{
  height: 500px;
}
.sidebarmain{
  padding-right:0px ;
}

}
</style>

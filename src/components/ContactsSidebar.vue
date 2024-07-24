<template>
  <div :class="['sidebar', { expanded: isExpanded }]">
    
    <img v-if="!isMobileView" class="ContactEaseinContacts" src="ContactEase2.png" alt="">
    <div class="profileImg">
      <img v-if="(isMobileView && isExpanded && img!=='null') || (!isMobileView && img!=='null')" class="profile-picture" :src="`/profile_pictures/${img}`" alt="Profile Picture" />
    </div>
    <h1 class="welcome" v-if="!isMobileView">Welcome, {{ user }}</h1>
    <p class="ProfileImgName" v-if="isMobileView && isExpanded">{{ user }}</p>
    <section class="" id="contacts">
      <button class="toggle-bt" @click="toggleSidebar" v-if="isMobileView">
      {{ isExpanded ? '<' : '>' }}
    </button>
    <button class="toggle-bt" @click="toggleSidebar" v-if="isExpanded && !isMobileView">
      {{ isExpanded ? '<' : '>' }}
    </button>
      <div v-if="isMobileView && isExpanded" class="ContactNavsPar">
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-if="success" class="alert alert-success">{{ success }}</div>
          <button class="ContactNavs" @click="toggleAddForm">
            {{ showAddForm ? 'Hide Form' : 'Add Contact' }}
          </button>
          <ContactForm
            v-if="showAddForm || currentContact"
            :contact="currentContact || {}"
            :isEdit="isEdit"
            @submit="handleSubmit"
            @cancel="handleCancel"
          />
          <router-link class="homeLink" to="/">Home</router-link>
          <button class="ContactNavs" @click="showUserDetails">Account</button>
          <button v-if="isAuthenticated" class="ContactNavs" @click="confirmLogout">Logout</button>
      </div>
      <div v-if="!isMobileView" class="ContactNavsPar">
        
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-if="success" class="alert alert-success">{{ success }}</div>
          <button class="ContactNavs" @click="toggleAddForm">
            {{ showAddForm ? 'Hide Form' : 'Add Contact' }}
          </button>
          <ContactForm
            v-if="showAddForm || currentContact"
            :contact="currentContact || {}"
            :isEdit="isEdit"
            @submit="handleSubmit"
            @cancel="handleCancel"
          />
          <router-link class="homeLink" to="/">Home</router-link>
          <button class="ContactNavs" @click="showUserDetails">Account</button>
          <button v-if="isAuthenticated" class="ContactNavs" @click="confirmLogout">Logout</button>
      </div>
      <div v-if="isMobileView && !isExpanded" class="ContactNavsPar">
        
            <img class="ContactNavsImages" @click="toggleSidebar" src="../assets/add-user.png" alt=""/>
            <img class="ContactNavsImages" @click="toggleSidebar" src="../assets/home-icon.png" alt=""/>
            <img class="ContactNavsImages" @click="toggleSidebar" src="../assets/user.png" alt=""/>
            <img class="ContactNavsImages" @click="toggleSidebar" src="../assets/logout.png" alt=""/>
      </div>

    </section>
    
    <LogoutConfirmationModal v-if="showLogoutModal" />
  </div>
</template>

<script>
import ContactForm from '@/components/ContactForm.vue';
import { mapState, mapActions } from 'vuex';
import LogoutConfirmationModal from './LogoutConfirmationModal.vue';

export default {
  components: {
    ContactForm,
    LogoutConfirmationModal
  },
  data() {
    return {
      showAddForm: false,
      currentContact: null,
      isEdit: false,
      isExpanded: false, 
      isMobileView: window.innerWidth <= 768 
    };
  },
  computed: {
    ...mapState(['user', 'token', 'contacts', 'error', 'success', 'showLogoutModal','img']),
    isAuthenticated() {
      return !!this.token;
    }
  },
  methods: {handleResize() {
      this.isMobileView = window.innerWidth <= 768;
    },
    ...mapActions(['addContact', 'updateContact', 'toggleLogoutModal']),
    async handleSubmit(contact) {
      try {
        if (this.isEdit) {
          await this.updateContact(contact);
        } else {
          await this.addContact(contact);
        }
        this.resetForm();
      } catch (error) {
        console.log(error);
      }
    },
    confirmLogout() {
      this.toggleLogoutModal(true);
    },
    handleCancel() {
      // if(!this.error)
      this.resetForm();
    },
    toggleAddForm() {
      this.showAddForm = !this.showAddForm;
      if (!this.showAddForm) {
        this.resetForm();
      }
    },
    editContact(contact) {
      if(this.isMobileView){
        this.isExpanded = !this.isExpanded;
        this.$emit('toggle-sidebar', this.isExpanded);
      }
      this.currentContact = contact;
      this.isEdit = true;
      this.showAddForm = true;
    },
    resetForm() {
      this.showAddForm = false;
      this.currentContact = null;
      this.isEdit = false;
    },
    toggleSidebar() {
      this.resetForm();
      this.isExpanded = !this.isExpanded;
      this.$emit('toggle-sidebar', this.isExpanded);
    },
    showUserDetails() {
      if(this.isMobileView)
        this.toggleSidebar()
      this.$emit('show-user');
    }
  },
  mounted() {
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
  }
};
</script>

<style scoped>
@import '../views/Contacts.css';

</style>

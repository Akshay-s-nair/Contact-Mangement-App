<template>
  <div class="main-content">
    
    <div class="search-filter">
      <input type="text" v-model="search" @input="handleSearch" placeholder="Search contacts..." class="form-control me-2">
      <select v-model="sort" @change="handleSort" class="form-select me-2">
        <option value="id">Date</option>
        <option value="name">Name</option>
      </select>
      <select v-model="sortOrder" @change="handleSortOrder" class="form-select me-2">
        <option value="asc">Ascending ↑</option>
        <option value="desc">Descending ↓</option>
      </select>
      <div class="counts">{{ total_count }} contacts found ! </div>
    </div>
    <div class="contacts-list">
      <!-- <div class="message messageMain">
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-if="success" class="alert alert-success">{{ success }}</div>
      </div> -->
      <div class="counts counts-mobView">{{ total_count }} contacts found ! </div>
      <div v-if="contacts.length">
        <div class="contact-grid">
          <div v-for="contact in contacts" :key="contact.id" class="contact-card">
            <div class="s1">
              <img src="../assets/ContactUser.png" class="ContactImg" alt="">
              <h3 class="contactsNames">{{ contact.firstname }} {{ contact.lastname }}</h3>
            </div>
            <div class="contact-info">
              <div class="ContactFields">
                <img class="ContactLogos" src="../assets/phone-call.png" alt=""><p>{{ contact.phone }}</p>
              </div>
              <div class="ContactFields">
                <img class="ContactLogos" src="../assets/Address.png" alt=""><p>{{ contact.address }}</p>
              </div>
              <div class="ContactFields">
                <img class="ContactLogos" src="../assets/building.png" alt=""><p>{{ contact.company }}</p>
              </div>
            </div>
            <hr style="margin: 10px;">
            <div class="contact-actions">
              <img class="editDltBut" @click="$emit('edit-contact', contact)" src="../assets/edit.png" alt="Edit">
              <img class="editDltBut" @click="handleDelete(contact.id)" src="../assets/delete.png" alt="Delete">
            </div>
          </div>
        </div>
        <div class="pagination-buttons">
          <img class="nextPrevBut" v-if="currentPage === 1" src="../assets/previousdis.png" @click="handlePrevious" alt="">
          <img class="nextPrevBut" v-else src="../assets/previous.png" @click="handlePrevious" alt="">
          <p class="paginationText">{{ `${previousLimit} to ${currentPage >= totalPages ? total_count : currentPage * 10} contacts` }}</p>
          <img class="nextPrevBut" v-if="currentPage >= totalPages" src="../assets/nextdis.png" @click="handleNext" alt="">
          <img class="nextPrevBut" v-else src="../assets/next.png" @click="handleNext" alt="">
        </div>
      </div>
      <div v-else>
        <p>No contacts available.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  data() {
    return {
      search: '',
      sort: 'id',
      sortOrder: 'asc',
      currentPage: 1,
      previousLimit:1
    };
  },
  computed: {
    ...mapState(['contacts', 'error', 'success', 'total_count']),
    totalPages() {
      return Math.ceil(this.total_count / this.$store.state.perPage);
    }
  },
  methods: {
    ...mapActions(['deleteContact', 'setSearch', 'setSort', 'setSortOrder', 'setCurrentPage']),
    handleDelete(contactId) {
      this.deleteContact(contactId);
    },
    handleSearch() {
      this.setSearch(this.search);
    },
    handleSort() {
      this.setSort(this.sort);
    },
    handleSortOrder() {
      this.setSortOrder(this.sortOrder);
    },
    handleNext() {
      if (this.currentPage < this.totalPages) {
        this.currentPage += 1;
        this.previousLimit=this.previousLimit+10;
        this.setCurrentPage(this.currentPage);
      }
    },
    handlePrevious() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
        this.previousLimit=this.previousLimit-10;
        this.setCurrentPage(this.currentPage);
      }
    }
  },
  watch: {
    currentPage(newPage) {
      this.setCurrentPage(newPage);
    }
  },
  created() {
    this.$store.dispatch('fetchContacts');
  }
};
</script>

<style scoped>
.main-content {
  width: 100%;
  /* padding: 20px; */
}

.search-filter {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 20px;
  /* position: sticky;
  top: 0;
  background: #f4f4f9; */
  margin-top: 0;
}

.search-filter input,
.search-filter select,
.search-filter button {
  margin-right: 10px;
}

.contacts-list {
  display: flex;
  flex-direction: column;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}

.contact-card {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.contact-info h3 {
  margin: 0;
  font-size: 1.5em;
}
.message{
  height: 30px;
}
.contact-info p {
  margin: 0;
  color: #666;
}

.contact-actions {
  display: flex;
  flex-direction: column;
  padding: 15px;
  width: 60px;
  justify-content:space-between;
}

.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
}

.btn:hover {
  text-decoration: none;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
  margin-right: 10px;
}

.btn-danger {
  background-color: #f44336;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
}

.btn-danger:hover {
  background-color: #d32f2f;
}

.alert {
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
}

.pagination-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  /* position:sticky; */
  bottom: 0%;
  color: #da5b01;
  background-color: #f4f4f9ac;
  font-weight: 600;
}
.counts-mobView{
  display: none;
}
.message{
  display: block;
}
.messageMain{
  display:block;
}
@media (max-width: 768px) {
  .search-filter {
    display: none;
}
.message{
  display: none;
}
/* .pagination-buttons{
} */
.contact-card{
  width: 200px;
  flex-direction: column;
}
.contact-actions {
  flex-direction: row;
  justify-content:space-around;
  width: 180px;
  padding: 0px;
  padding-left: 10px;
  
  margin-top: 10px;
}
.contact-actions {
  display: flex;
}
.counts-mobView{
  display:block;
  font-size: 12px;
  margin-bottom: 10px;
  text-align: right;
}
.messageMain{
  display: none;
}
}

</style>

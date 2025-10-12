<template>
  <div class="bg-gradient-to-br from-[#e6f0fa] via-[#f4f8fb] to-[#c5def0]">
<NavBar />
  <div>
        <div class="bg-[#3D81B6]">
  <div class="max-w-7xl mx-auto px-4 sm:px-8 lg:px-8 py-4">
    <div class="flex flex-col md:flex-row justify-between items-center md:items-start mb-8 gap-6 mt-4">
      <div>      
      <h1 class=" text-2xl md:text-3xl font-bold text-white">Welcome, {{ user?.username }}!</h1>
      <p class="text-white mt-2">{{  user?.email }}</p>
      </div>
      <div class="flex items-center gap-4 ml-4 ">
        <button @click="scanQR()" class="  hover:bg-[#153958]  text-[#1A4C7A] p-2 rounded-md flex items-center gap-2 bg-white hover:text-white transition">
          <img src="https://res.cloudinary.com/dotzzcayo/image/upload/v1756554037/qr_bt4tlr.png" alt="qr code" class="w-5 h-5 inline-block">
          
          <span  class="hidden md:inline">QR Scanner</span></button>
     
        <router-link :to="{name:'edit-profile'}" class="  bg-white p-2 rounded-md flex items-center gap-2 hover:bg-[#1A4C7A] hover:text-white transition">
          <img src="https://res.cloudinary.com/dotzzcayo/image/upload/v1752843306/edit_wbbo0b.png" alt="edit" class="w-6 h-6 rounded-xl inline-block">
          
          <span  class="hidden md:inline">Edit Profile</span></router-link>

        <router-link :to="{name:'create-event'}" class="  hover:bg-[#153958]  text-white p-2 rounded-md flex items-center gap-2 bg-[#1A4C7A] hover:text-white transition">
          <img src="https://res.cloudinary.com/dotzzcayo/image/upload/v1751300079/add_smvptr.png" alt="edit" class="w-5 h-5 rounded-xl inline-block">
          
          <span  class="hidden md:inline">Create Event</span></router-link>
      </div></div></div>
    </div>
    <div class="flex justify-center gap-6 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Total Registered Users Card -->
      <div class="bg-white border  transform bg-gradient-to-b from-[#F9FBFD] to-[#d5e6f3] border-[#E0E6ED] rounded-2xl shadow-md hover:shadow-xl transition-transform duration-300   hover:-translate-y-1 cursor-pointer w p-6 flex flex-col items-center w-full max-w-md md:max-w-xl ">
        <h2 class="text-xl font-semibold mb-2 text-[#1E6091]">Total Users</h2>
        <div class="text-4xl font-bold text-[#1E6091] mb-1">{{ totalRegisteredUsers }}</div>
      </div>

      <!-- Total Events Card -->
      <div class="bg-white border bg-gradient-to-b from-[#F9FBFD] to-[#d5e6f3] border-[#E0E6ED] rounded-2xl shadow-md hover:shadow-xl transition-transform duration-300  transform hover:-translate-y-1 cursor-pointer w p-6 flex flex-col items-center w-full max-w-md md:max-w-xl">
        <h2 class="text-xl font-semibold mb-2 text-[#1E6091]">Total Events</h2>
        <div class="text-4xl font-bold text-[#1E6091] mb-1">{{ total }}</div>
      </div>
    </div>

        <!--search-->
     <section class="px-4 md:px-16 py-8">
      <!-- Search Bar -->
      <div class="mb-2 max-w-xl mx-auto flex gap-4">
        <input
          v-model="searchQuery"
          @keyup.enter="fetchAllEvents"
          type="text"
          placeholder="Search for event title or description..."
          class="w-full p-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#1E5A8A]"
          id="search"
        />
        <button
          @click="fetchAllEvents"
          class="bg-[#1E5A8A] text-white px-6 py-3 rounded-xl hover:bg-[#16456b]"
        >
          Search
        </button>
      </div>
    </section>

    <!-- Events Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h2 class="text-xl font-semibold mb-6">My Events</h2>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        
        <!-- Event Card -->
        <div v-for="event in events" :key="event.id" class="bg-white border border-gray-200 rounded-xl shadow-md hover:shadow-lg transition transform hover:-translate-y-1 max-h-fit">
          <!-- Event Image -->
          <img
            :src=event.image
            alt="Sample Event"
            class="w-full h-48 object-cover rounded-t-xl"
          />

          <!-- Event Content -->
          <div class="p-6">
            <h2 class="text-lg font-semibold">{{ event.name }}</h2>
            <p class="text-sm text-gray-600 mt-2 h-18">
              {{ event.description}}
            </p>

            <!-- Date & Location -->
            <p class="mt-4 text-sm text-gray-500">📅 {{ event.date }} at {{ event.time }}</p>
            <p class="mt-1 text-sm text-gray-500">📍 {{ event.location }}</p>
 
            <!-- Capacity & Organizer -->
            <div class="flex justify-between mt-3">
              <p class="text-sm text-gray-600">👥 Available Slots: {{  event.capacity }}</p>
              <p class="text-sm text-gray-600">by <span class="capitalize">{{ event.organizer }}</span></p>
            </div>

            <!-- Action Buttons -->
            <div class="flex justify-between items-center mt-4">
              <button  @click="openEdit(event)"
                class=" w-[220px] flex justify-center items-center gap-2 px-3 py-1 rounded-md border border-gray-300 bg-white hover:bg-gray-200 text-[#1A4C7A] transition text-sm ">
                <img src="https://res.cloudinary.com/dotzzcayo/image/upload/e_background_removal/f_png/v1752843306/edit_wbbo0b.png" alt="Edit" class="w-5 h-5 ">
                <span>Edit</span>
            </button>

              <button @click="toggleConfirm(event.id)"
                class="flex justify-center items-center gap-2 px-3 py-1 rounded-md border border-gray-300 bg-white hover:bg-gray-200 text-red-600 transition text-sm w-[100px]">
                <img src="https://res.cloudinary.com/dotzzcayo/image/upload/e_background_removal/f_png/v1755009971/red_delete_mw5ruu.png" alt="Delete" class="w-5 h-5">
                <span>Delete</span>
            </button>

            </div>
              <div v-if="show[event.id]" class="mt-4 p-4 border border-red-300 bg-red-50 rounded-md text-center">
                <p class="text-red-600 text-sm mt-2">Are you sure?</p>
                <div class="flex gap-2 mt-1 items-center justify-center">
                  <button @click="deleteEvent(event.id)" class="px-3 py-1 bg-red-600 text-white rounded-md hover:bg-red-700 text-sm">Yes</button>
                  <button @click="toggleConfirm(event.id)" class="px-3 py-1 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 text-sm">No</button>
                </div>
              
              </div>

            <!-- View Registered Users -->
            <button @click="openRegistration(event)"
              class="mt-4 flex items-center gap-2 px-3 py-2 rounded-md bg-[#1A4C7A] hover:bg-[#2370AC] transition text-white text-sm w-full justify-center">
              <span>View Registered Users</span>
          </button>
          </div>

        </div>
        <EditEvent 
            v-if="showEditModal" 
            :event="selectedEvent" 
            @cancel="showEditModal = false"
            @update="handleUpdate"
          />
        <ViewRegisteration
            v-if="showRegisteredUsers" 
            :eventId="selectedEvent" 
            @cancel="showRegisteredUsers = false"

          /> 
                  <QRCode
            v-if="showQRCOde" 
            @cancel="showQRCOde = false"

          /> 
        
        



      </div>

    </div>

            <div class="mt-8  mb-8 flex justify-center gap-4" v-if="!(events.length === 0)">
      <button
        @click="prevPage"
        :disabled="offset === 0"
        class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 disabled:opacity-50"
      >
        Previous
      </button>
      <button
        @click="nextPage"
        :disabled="events.length < limit"
        class="px-4 py-2 bg-[#1E5A8A] text-white rounded hover:bg-[#16456b] disabled:opacity-50"
      >
        Next
      </button>
    </div>

    <!-- No Results -->
    <div v-if="events.length === 0" class="text-center mt-12 mb-4 text-gray-500">
      No events found.
    </div>
  </div>
  <Footer />
  </div>
</template>

<script >
import NavBar from '../../components/NavBar.vue';
import Footer from '../../components/Footer.vue';
import EditEvent from '../../components/EditEvent.vue';
import { useAuthStore } from '../../stores/auth.js';
import { storeToRefs } from 'pinia';
import api from '../../axios'; 
import ViewRegisteration from '../../components/ViewRegisteration.vue';
import QRCode from '../../components/QRCode.vue';
export default {
  name: 'OrganizerDashboard',
  components: {
    NavBar,
    Footer,
    EditEvent,
    ViewRegisteration,
    QRCode
  },
  data() {
    return {
      searchQuery: '',
      events:[],
      limit: 3,
      offset: 0,
      total: 0,
      user: null,
      show: {},
      showRegisteredUsers: false,
      showEditModal: false,
      selectedEvent: null,
      showQRCOde:false,
      totalRegisteredUsers: 0,
    };
  },

    async mounted()  {
    const authStore = useAuthStore();
    const { isAuthenticated, user } = storeToRefs(authStore);

    if (!isAuthenticated.value) {
      this.$router.push({ name: 'login' });

    }
    else{
      this.user = user.value;
      await this.fetchAllEvents();
    }
  },
  methods: {
    
    async fetchAllEvents() {
      try
      {
          const eventres = await api.get(`${import.meta.env.VITE_API_BASE_URL}/events/organizer-event`, {
          params: {
            search: this.searchQuery,
            limit: this.limit,
            offset: this.offset
          }
        });
        this.events = eventres.data.events.map(event => ({
          ...event,
          image: `${import.meta.env.VITE_API_BASE_URL}/static/images/${event.image}`
        }));
        console.log(this.events)
        this.total = eventres.data.total;
        const response= await api.get(`${import.meta.env.VITE_API_BASE_URL}/registration/view-all-student-registrations`); //fetch total registered users
        this.totalRegisteredUsers = response.data.total;
        console.log( this.totalRegisteredUsers)
      
      } 
      catch (error) {
  
        this.events = [] 
      }

    },
     

    
      openEdit(event) {
    this.selectedEvent = event
    this.showEditModal = true
  },
  openRegistration(event){
    this.selectedEvent =event
    this.showRegisteredUsers =true

  },
    toggleConfirm(eventId) {
      this.show[eventId] = !this.show[eventId];
    },
    scanQR(){
      this.showQRCOde = true;
    },

    async deleteEvent(eventId) {
      try {
        await api.delete(`${import.meta.env.VITE_API_BASE_URL}/events/delete-event/${eventId}`);
        this.events = this.events.filter(event => event.id !== eventId);
        this.total -= 1;
        delete this.show[eventId];
        await this.fetchAllEvents();

      } catch (error) {
        console.error('Error deleting event:', error);
      }
    },

          nextPage(){
    if(this.limit + this.offset < this.total){
      this.offset += this.limit
      this.fetchAllEvents()
    }

  },
  prevPage(){
    if(this.offset > 0){
      this.offset -= this.limit
      this.fetchAllEvents()
    }

  },  
  async handleUpdate(updatedEvent) {

    const index = this.events.findIndex(e => e.id === updatedEvent.id);
    if (index !== -1) {
      this.events[index] = {
        ...updatedEvent,
      image: updatedEvent.image
        ? `${import.meta.env.VITE_API_BASE_URL}/static/images/${updatedEvent.image}`
        : this.events[index].image
      
    };
    this.showEdit[updatedEvent.id] = false;
    
  }
  },
}
 
};

</script>
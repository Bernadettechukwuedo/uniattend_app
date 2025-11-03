<template>
  <div class="bg-linear-to-br from-[#e6f0fa] via-[#f4f8fb] to-[#c5def0]">
<NavBar />
  <div class="overflow-y-hidden">

    <div class="bg-[#3D81B6]">
  <div class="max-w-7xl mx-auto px-4 sm:px-8 lg:px-8 py-4">
    <div class="flex flex-col md:flex-row justify-between items-center md:items-start mb-8 gap-6 mt-4">
      
      <!-- User Info -->
      <div class="text-center md:text-left">
        <h1 class="text-2xl md:text-3xl font-bold text-white">
          Welcome, {{ user?.username }}!
        </h1>
        <p class="text-white mt-1">{{ user?.email }}</p>
      </div>

      <!-- Edit Profile Button -->
      <div class="flex justify-center md:justify-end">
        <router-link
          :to="{ name: 'edit-profile' }"
          class="bg-white px-4 py-2 rounded-md flex items-center gap-2 hover:bg-[#1A4C7A] hover:text-white transition"
        >
          <img
            src="https://res.cloudinary.com/dotzzcayo/image/upload/v1752843306/edit_wbbo0b.png"
            alt="edit"
            class="w-5 h-5 rounded-md"
          />
          <span class="font-medium">Edit Profile</span>
        </router-link>
      </div>
      
    </div>
  </div>
</div>

    <div class="flex flex-col md:flex-row justify-between  max-w-7xl gap-6 mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-white border bg-linear-to-b from-[#F9FBFD] to-[#d5e6f3] border-[#E0E6ED] rounded-2xl shadow-md hover:shadow-xl transition-transform duration-300  transform hover:-translate-y-1 cursor-pointer w-full max-w-md md:max-w-xl text-center p-6">
        <h1 class="text-xl font-semibold mb-2 text-[#1E6091]">Total Registered Events</h1>
        <p  class="text-4xl font-bold text-[#1E6091] mb-1">{{  totalRegisteredEvents }}</p>
      </div>
            <div class="bg-white border bg-linear-to-b from-[#F9FBFD] to-[#d5e6f3] border-[#E0E6ED] rounded-2xl shadow-md hover:shadow-xl transition-transform duration-300  transform hover:-translate-y-1 cursor-pointer w-full max-w-md md:max-w-xl text-center p-6">
        <h1 class="text-xl font-semibold mb-2 text-[#1E6091]">Total Past Registered Events</h1>
        <p  class="text-4xl font-bold text-[#1E6091] mb-1">{{  totalPastEvents }}</p>
      </div>
    </div>
    <!--search-->
     <section class="px-4 md:px-16 py-8">
      <!-- Search Bar -->
      <div class="mb-2 max-w-xl mx-auto flex gap-4">
        <input
          v-model="searchQuery"
          @keyup.enter="fetchEvents"
          type="text"
          placeholder="Search for event title or description..."
          class="w-full p-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#1E5A8A]"
          id="search"
        />
        <button
          @click="fetchEvents"
          class="bg-[#1E5A8A] text-white px-6 py-3 rounded-xl hover:bg-[#16456b]"
        >
          Search
        </button>
      </div>
    </section>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
  
      <h1 class="text-2xl mb-2 font-bold ">Campus Events</h1>
    
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-8 ">
      <div
        v-for="event in filteredEvents"
        :key="event.id"
        class="bg-white border border-gray-200 rounded-xl shadow-md hover:shadow-lg transition transform hover:-translate-y-1 max-h-fit"
      ><div></div>
        <img
          :src="event.image"
          alt="Event Image"
          class="w-full h-48 object-cover rounded-t-xl"
        />
        <div class="p-6">
          <h2 class="text-lg font-semibold ">
            {{event.name }}
          </h2>
          <p class="text-sm text-gray-600 h-18">
            {{ event.description }}
          </p>

          <p class="mt-4 text-sm text-gray-500">📅 {{ event.date }} at {{ event.time }}</p>

          <p class="mt-2 text-sm text-gray-500">📍 {{ event.location }}</p>
          <div class="flex flex-row justify-between mt-2">
                        <p class="text-sm text-gray-600 ">👥 Available Slots:
            {{ event.capacity }} 
          </p>
                    <p class="text-sm text-gray-600  "> by
            <span class="capitalize">{{ event.organizer }}</span>
          </p>

</div>

        <div class="mt-4">
            <button
              v-if="isRegistered(event.id)"
              class="hover:bg-gray-300 text-black border border-gray-400 hover:text-[#1E5A8A] bg-white/80 px-4 py-2 rounded-lg mr-2"
              @click="unregisterEvents(event.id)"
            >
              Unregister
            </button>

            <button
              v-if="isRegistered(event.id)"
              class="bg-[#1E5A8A] text-white px-4 py-2 rounded-lg mt-2"
              @click="viewQrCode(getQrCodePath(event.id))"
            >
              View QR Code
            </button>

            <button
              v-else
              class="bg-[#1E5A8A] text-white px-4 py-2 rounded-lg w-full mt-2"
              @click="registerEvents(event.id)"
            >
              Register
            </button>
          </div>
        </div>
      </div>
    </div> </div>

      <div class="mb-4 flex justify-center gap-4" v-if="!(filteredEvents.length === 0)">
      <button
        @click="prevPage"
        :disabled="offset === 0"
        class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 disabled:opacity-50"
      >
        Previous
      </button>
      <button
        @click="nextPage"
        :disabled="offset + limit >= totalEvents"
        class="px-4 py-2 bg-[#1E5A8A] text-white rounded hover:bg-[#16456b] disabled:opacity-50"
      >
        Next
      </button>
    </div>
        <!-- No Results -->
    <div v-if="filteredEvents.length === 0" class="text-center mb-8 text-gray-500">
      No upcoming events available at the moment.
    </div>

    <!-- QR Code Modal -->
    <div v-if="showQrModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 ">
      <div class="bg-white rounded-xl p-6 max-w-md w-full shadow-lg text-center relative">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">Scan to Check In </h2>
        
        <img
          :src="qrCodePath"
          alt="QR Code"
          class="w-50 h-50 mx-auto mb-4 object-contain"
        />

        <button
          @click="closeQrModal"
          class="mt-4 px-6 py-2 bg-[#1E5A8A] text-white rounded-xl hover:bg-[#16456b] transition"
        >
          Close
        </button>

        <!-- Optional close icon top right -->
        <button
          @click="closeQrModal"
          class="absolute top-3 right-3 text-gray-500 hover:text-gray-700 text-lg "
        >
           ✕
        </button>
      </div>
    </div>


    

    

  </div>
  <Footer />
  </div>
</template>

<script>
import NavBar from '../../components/NavBar.vue';
import Footer from '../../components/Footer.vue';
import { useAuthStore } from '../../stores/auth.js';
import { storeToRefs } from 'pinia';
import api from '../../axios'; 

export default {
  name: 'StudentDashboard',
  components: {
    NavBar,
    Footer,
  },
  data() {
    return {
      searchQuery: '',
      events: [],
      registeredEvents: [],
      totalEvents: 0,
      totalRegisteredEvents: 0,
      limit: 3,
      offset: 0,
      total: 0,
      user: null,
      showQrModal: false,
      qrCodePath: '',
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
    getToken() {
  return useAuthStore().token;
    },
    async fetchAllEvents() {

      try {
        const eventsRes = await api.get('/events/get-events', {
          params: {
            search: this.searchQuery,
            limit: this.limit,
            offset: this.offset
          }
        });

        const registeredRes = await api.get('/registration/get-registrations', {

        });
        

        this.events = eventsRes.data.events.map((event) => ({
          ...event,
          image: event.image
        }));
        

        // If API response is wrapped
        this.registeredEvents = registeredRes.data.registrations ;
        

        this.totalEvents = eventsRes.data.total;
        this.totalRegisteredEvents = registeredRes.data.total ;

      }    catch (error) {
        console.error('Error fetching events:', error)
        this.events = [] 
      
      }
    },

    isRegistered(eventId) {
      return this.registeredEvents.some((e) => e.event_id === eventId );
    },

    getQrCodePath(eventId) {
      const reg = this.registeredEvents.find((e) => e.event_id === eventId);
      return reg ? reg.qr_code_path: '';
      
      
    },

    async registerEvents(eventId) {
      try {
        const response = await api.post('/registration/register-event', {
          event_id: eventId,
          user_id: this.user.id,
        }
      );

        const event = this.events.find((e) => e.id === eventId);
        if (event) this.registeredEvents.push(event);

        if (response.data.success) {
          this.fetchAllEvents();
        } else {
          console.error('Registration failed:', response.data.message);
        }
      } catch (error) {
        console.error('Error registering for event:', error);
      }
    },

    async unregisterEvents(eventId) {
      try {
        const response = await api.delete('/registration/unregister', {
          params: {
            event_id: eventId,
          }
        });

        this.registeredEvents = this.registeredEvents.filter((e) => e.id !== eventId && e.event_id !== eventId);

        if (response.data.success) {
          this.fetchAllEvents();
        } else {
          console.error('Unregistration failed:', response.data.message);
        }
      } catch (error) {
        console.error('Error unregistering from event:', error);
      }
    },

    async fetchEvents() {
      this.offset = 0; // Reset offset on search
      await this.fetchAllEvents();
    },

    nextPage() {
      if (this.offset + this.limit < this.totalEvents) {
        this.offset += this.limit;
        this.fetchAllEvents();
      }
    },

    prevPage() {
      if (this.offset > 0) {
        this.offset -= this.limit;
        this.fetchAllEvents();
      }
    },

    viewQrCode(path) {
      this.qrCodePath = path;
      this.showQrModal = true;
    },

    closeQrModal() {
      this.showQrModal = false;
      this.qrCodePath = '';
    }
  },
   computed: {
    filteredEvents() {
      
     const today = new Date();
     return this.events.filter(event => new Date(event.date) >= today);
   },
     totalPastEvents() {
    const today = new Date();
    return this.registeredEvents.filter(reg => {
      // find event details from the event_id
      const event = this.events.find(e => e.id === reg.event_id);
      return event && new Date(event.date) < today;
    }).length;
  }
}
}
</script>

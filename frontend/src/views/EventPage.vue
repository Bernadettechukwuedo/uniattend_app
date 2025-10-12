<template>
  <div class="min-h-screen bg-white">
    <!-- Navbar -->
    <NavBar />

    <!-- Hero Image -->
    <div class="relative">
      <img
        src="https://res.cloudinary.com/dotzzcayo/image/upload/v1752768472/Roorkee_vjqdfj.jpg"
        alt="University building"
        class="w-full h-[500px] object-cover  shadow-lg"
      />
      <div class="absolute inset-0 bg-gradient-to-br from-[#1E5A8A] via-black/40 to-black"></div>
    </div>

    <!-- Event Overview Header -->
     <section class="px-4 md:px-16 py-8">
      <!-- Search Bar -->
      <div class="mb-8 max-w-xl mx-auto flex gap-4">
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
    <!-- Events Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
      <div
        v-for="event in filteredEvents"
        :key="event.id"
        class="bg-white border border-gray-200 rounded-xl shadow-md hover:shadow-lg transition tranform hover:-translate-y-1 max-h-fit"
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
          <p class="text-sm text-gray-600 h-18 ">
            {{ event.description }}
          </p>

          <p class="mt-4 text-sm text-gray-500">📅 {{ event.date }} at {{ event.time }}</p>

          <p class="text-sm text-gray-600 ">👥 Available Slots:
            {{ event.capacity }} 
          </p>
          <div class="mt-6" >

          <router-link 
            class=" bg-[#1E5A8A] text-white px-4 py-2 rounded-full hover:bg-[#16456b] transition"
          >
            View more
          </router-link></div>
        </div>
      </div>
    </div>
        <div class="mt-8 flex justify-center gap-4" v-if="!(filteredEvents.length === 0)">
      <button
        @click="prevPage"
        :disabled="offset === 0"
        class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 disabled:opacity-50"
      >
        Previous
      </button>
      <button
        @click="nextPage"
        :disabled="filteredEvents.length < limit"
        class="px-4 py-2 bg-[#1E5A8A] text-white rounded hover:bg-[#16456b] disabled:opacity-50"
      >
        Next
      </button>
    </div>

    <!-- No Results -->
    <div v-if="filteredEvents.length === 0" class="text-center mt-12 text-gray-500">
      No events found.
    </div>
  </section>
  
  <Footer/>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import Footer from '../components/Footer.vue';
import api from '../axios'; 

export default {
  name: 'EventPage',
  components: {
    NavBar,
    Footer
  },
  data() {
    return {
      searchQuery: '',
      events: [],
      limit: 3,         // events per page
     offset: 0,        // how many events to skip
      total: 0,  
 
    }
  },
  methods: {
    async fetchEvents() {
      try {
        const response = await api.get(
          `${import.meta.env.VITE_API_BASE_URL}/events/get-events`,
          {
            params: {
              search: this.searchQuery,
              limit: this.limit,
              offset: this.offset
            },
          }
        )
        this.total = response.data.total
        this.events = response.data.events.map((event) => ({
          ...event,
          image: `${import.meta.env.VITE_API_BASE_URL}/static/images/${event.image}`

        }))
      } catch (error) {
        console.error('Error fetching events:', error)
        this.events = [] 
      }
    },
      nextPage(){
    if(this.limit + this.offset < this.total){
      this.offset += this.limit
      this.fetchEvents()
    }

  },
  prevPage(){
    if(this.offset > 0){
      this.offset -= this.limit
      this.fetchEvents()
    }

  },
  },

  mounted() {
    this.fetchEvents() 
  },
  computed: {
    filteredEvents() {
      
      const today = new Date();
     return this.events.filter(event => new Date(event.date) > today);
    }
  }
}
</script>



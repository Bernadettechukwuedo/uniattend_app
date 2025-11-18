<script setup>
import NavBar from '../components/NavBar.vue';
import Footer from '../components/Footer.vue';
import { Icon } from '@iconify/vue';
import { useAuthStore } from '../stores/auth.js';
import { storeToRefs } from 'pinia';
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
const authStore = useAuthStore();
const { isAuthenticated, user } = storeToRefs(authStore);
const router = useRouter();

const isAuth = ref(false);

onMounted(() => {
  CheckAuth();
});
watch(isAuthenticated, () => {
  CheckAuth();
});

function CheckAuth() {
  if (!isAuthenticated.value) {
    isAuth.value = false;
  } else {
    isAuth.value = true;
    const role = user.value.role;
    if (role === 'student') {
      router.push({ name: 'student-dashboard' });
    } else if (role === 'organizer') {
      router.push({ name: 'organizer-dashboard' });
    } else if (role === 'admin') {
      router.push({ name: 'admin-dashboard' });
    }
  }
}

const features1 = [
  {
    icon: 'mdi:account-search',
    title: 'Event Discovery',
    description: 'Easily find events that match your interests, schedule, and location on campus.',
  },
  {
    icon: 'mdi:clipboard-check',
    title: 'Easy Registration',
    description: 'Students can register for events seamlessly using their devices.',
  },
  {
    icon: 'mdi:qrcode-scan',
    title: 'Secure QR Check-in',
    description:
      'Every participant gets a unique QR code, preventing ticket duplication and ensuring only verified attendees enter.',
  },
  {
    icon: 'mdi:earth',
    title: 'Accessible Anywhere',
    description:
      'The web-based system is accessible from any device, ensuring flexibility and ease of use.',
  },
];

const features2 = [
  {
    icon: 'mdi:numeric-1-circle',
    title: 'Discover Events',
    description:
      ' Browse through hundreds of campus events filtered by your interests, date, and location preferences.',
    color: 'text-blue-600',
  },
  {
    icon: 'mdi:numeric-2-circle',
    title: 'Sign Up & Join',
    description: 'Create your profile and register for events that interest you. ',
    color: 'text-green-600',
  },
  {
    icon: 'mdi:numeric-3-circle',
    title: 'Attend & Engage',
    description:
      'Show up to events, meet new people, and engage with your campus community in meaningful ways.',
    color: 'text-yellow-400',
  },
  {
    icon: 'mdi:numeric-4-circle',
    title: 'Scan to Attend',
    description:
      ' Show your QR code at the event entrance for quick and secure check-in, no paperwork, no stress.',
    color: ' text-red-500',
  },
];
</script>

<template>
  <div v-if="!isAuth">
    <NavBar />
    <!--hero section-->
    <div id="home" class="relative h-screen flex items-center justify-center overflow-hidden">
      <div class="absolute inset-0 z-0">
        <img
          src="https://res.cloudinary.com/dotzzcayo/image/upload/v1763491206/hero_section_mbrhnp.jpg"
          alt="Dynamic campus event with excited students collaborating and organizing activities"
          class="w-full h-full object-cover"
        />
        <div
          class="absolute inset-0 bg-linear-to-br from-[#040022]/40 via-[#040022]/60 to-black/40"
        ></div>
      </div>
      <div class="relative z-10 text-center text-white px-4 animate-slide-up max-w-5xl">
        <h1 class="text-5xl md:text-7xl font-bold font-trap mb-6">
          Discover & Create Amazing Campus Event
        </h1>
        <p class="text-xl md:text-3xl mb-8 max-w-4xl mx-auto font-normal font-sans weight-light">
          Connect with your campus community through events that matter. From academic conferences
          to social gatherings, find your next experience here.
        </p>
        <div class="flex flex-row gap-4 justify-center">
          <router-link
            :to="{ name: 'view-events' }"
            class="text-md md:text-lg px-4 md:px-8 py-3 bg-blue-600 hover:bg-[#1a4c7a] shadow-lg rounded-md font-bold"
            >Explore Events</router-link
          >
          <router-link
            :to="{ name: 'signup' }"
            class="text-md md:text-lg px-4 md:px-8 py-3 bg-white/10 border border-white/60 text-white hover:bg-white/20 font-bold backdrop-blur-sm rounded-md"
            >Create Events</router-link
          >
        </div>
      </div>
    </div>

    <!--about-->
    <div class="bg-[#F9F9FA] py-20" id="about">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center text-black mb-16">
          <h2 class="text-4xl md:text-5xl mb-4 font-bold">
            About <span class="text-blue-600">UniAttend</span>
          </h2>
          <p class="text-[18px] md:text-xl max-w-4xl mx-auto text-gray-500 font-semibold">
            We are transforming how students discover, attend, and create events on campus. Our
            platform brings the entire campus community together through meaningful experiences.
          </p>
        </div>
        <!--about card-->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div
            v-for="(feature, index) in features1"
            :key="index"
            class="border border-gray-200 bg-white rounded-xl p-6 text-center shadow-sm hover:shadow-lg hover:rounded-xl transform hover:scale-105 transition-all duration-300"
          >
            <Icon
              :icon="feature.icon"
              width="40"
              height="40"
              class="flex justify-center mb-4 text-4xl mx-auto text-blue-600"
            />
            <h3 class="text-xl font-semibold mb-2">{{ feature.title }}</h3>
            <p class="text-gray-500 text-sm">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </div>
    <!--how it works-->
    <div class="bg-[#FFFFFF] py-20" id="how-it-works">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl mb-4 font-bold text-black">How It Works</h2>
          <p class="text-[18px] md:text-xl max-w-4xl mx-auto text-gray-500 font-semibold">
            Getting started with UniAttend is simple. Follow these four easy steps to transform your
            campus experience.
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-18">
          <div
            v-for="(feature, index) in features2"
            :key="index"
            class="bg-white rounded-xl text-center hover:rounded-xl transform hover:scale-105 hover:shadow-xl transition-transform duration-300 p-4"
          >
            <Icon
              :icon="feature.icon"
              width="60"
              height="60"
              :class="['flex justify-center mb-4 text-4xl mx-auto ', feature.color]"
            />
            <h3 class="text-xl font-semibold mb-2">{{ feature.title }}</h3>
            <p class="text-gray-500 text-sm">{{ feature.description }}</p>
          </div>
        </div>
      </div>

      <div class="bg-[#F4F8FB] rounded-2xl p-8 mx-auto max-w-md md:max-w-2xl">
        <h3 class="text-2xl mb-4 text-center text-black">Ready to Get Started?</h3>
        <p class="opacity-50 text-center text-black mb-6">
          Join thousands of students who are already using UniAttend to discover amazing experiences
          and build connections.
        </p>

        <router-link
          :to="{ name: 'signup' }"
          class="block bg-[#2370AC] px-8 py-3 text-white rounded-lg w-full text-center hover:scale-100 hover:bg-[#344c5e] transition-all duration-300"
        >
          Sign Up Today
        </router-link>
      </div>
    </div>
    <Footer />
  </div>
</template>

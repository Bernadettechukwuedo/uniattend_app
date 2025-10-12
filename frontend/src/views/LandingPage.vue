<script setup>  
import NavBar from '../components/NavBar.vue';
import Footer from '../components/Footer.vue';

</script>


<template >
  <div>
    <NavBar/>

        <!--hero section-->
     <div id="home" class="relative h-screen flex items-center justify-center overflow-hidden ">
      <div class="absolute inset-0 z-0">
        <img
          src="https://images.unsplash.com/photo-1559223607-a43c990c692c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80"
          alt="Dynamic campus event with excited students collaborating and organizing activities"
          class="w-full h-full object-cover "
        />
        <div class="absolute inset-0 bg-gradient-to-br from-[#1E5A8A] via-black/40 to-black"></div>
      </div>
          <div class="relative z-10 text-center text-white px-4 animate-slide-up">
        <h1 class="text-4xl md:text-6xl mb-6 leading-tight">Discover & Create Amazing Campus Events</h1>
        <p class="text-xl md:text-2xl mb-8 text-gray-200 max-w-2xl mx-auto">Connect with your campus community through events that matter. From academic conferences to social gatherings, find your next experience here.</p>
        <div class=" flex flex-row gap-4 justify-center">
          <button class=" text-md md:text-lg px-8 py-3 animate-bounce bg-[#1E5A8A] hover:bg-[#1a4c7a] shadow-lg rounded-full">Explore Events</button>
          <router-link :to="{name:'signup'}" class=" text-md md:text-lg px-8 py-3 bg-white/10 border border-white text-white hover:bg-white/20 backdrop-blur-sm rounded-full">Create Events</router-link>
        </div>
      </div>
      </div>
    
        <!--about-->
      <div class="bg-[#F9F9FA] py-20 " id="about">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center text-black mb-16">
          <h2 class="text-3xl md:text-4xl mb-4 font-bold">
            About <span class="text-[#1E5A8A] ">UniAttend</span>
          </h2>
          <p class="text-xl  max-w-3xl mx-auto">
            We are transforming how students discover, attend, and create events on campus. 
            Our platform brings the entire campus community together through meaningful experiences.
          </p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 justify-items-center px-4 ">
          <!--icon 1-->
           <div class="bg-white border-1 border-gray-300 transform hover:scale-105 transition-transform duration-300 rounded-xl shadow-md w-full max-w-xl text-center">
          <div class="flex justify-center mt-4 mb-4">
            <img
              src="https://res.cloudinary.com/dotzzcayo/image/upload/v1752686213/calender_l71pi8.png"
              alt="Calendar"
              class="w-8 h-8"
            />
          </div>
   

          <!-- Text -->
          
          
            <h1 class="text-xl font-semibold">Event Discovery</h1>
            <p class="text-gray-600 text-sm py-8">
              Easily find events that match your interests, schedule, and location on campus.
            </p>
          
          
          </div>

          
          <!--icon 2-->
           <div class="bg-white border-1 border-gray-300 transform hover:scale-105 transition-transform duration-300 rounded-xl shadow-md  w-full max-w-xl  text-center">
          <div class="flex justify-center mt-4 mb-4">
            <img
              src="https://res.cloudinary.com/dotzzcayo/image/upload/v1751300165/template_hcj6wa.png"
              alt="Registration paper"
              class="w-8 h-8"
            />
          </div>

          <!-- Text -->
          
            <h1 class="text-xl font-semibold">Easy Registration</h1>
            <p class="text-gray-600 text-sm py-8">
              	Students can register for events seamlessly using their devices.
            </p>
          
          
          </div>

          <!--icon 3-->
           <div class="bg-white border-1 border-gray-300 transform hover:scale-105 transition-transform duration-300 rounded-xl shadow-md  w-full max-w-xl text-center">
          <div class="flex justify-center mt-4 mb-4">
            <img
              src="https://res.cloudinary.com/dotzzcayo/image/upload/v1752668806/security_y3eodu.png"
              alt="Security icon"
              class="w-8 h-8"
            />
          </div>

          <!-- Text -->
          
          
            <h1 class="text-xl font-semibold">Secure QR Check-in</h1>
            <p class="text-gray-600 text-sm py-8">
             Every participant gets a unique QR code, preventing ticket duplication and ensuring only verified attendees enter.
            </p>
          
          
          </div>

          <!--icon 4-->
           <div class="bg-white border-1 border-gray-300 transform hover:scale-105 transition-transform duration-300 rounded-xl shadow-md w-full max-w-xl text-center">
          <div class="flex justify-center mt-4 mb-4">
            <img
              src="https://res.cloudinary.com/dotzzcayo/image/upload/v1752668902/world_wide_wnaxgc.png"
              alt="World wide icon"
              class="w-8 h-8"
            />
          </div>

          <!-- Text -->
          
            <h1 class="text-xl font-semibold">Accessible Anywhere</h1>
            <p class="text-gray-600 text-sm py-8">
              	The web-based system is accessible from any device, ensuring flexibility and ease of use.
            </p>
          
          </div>

          
      </div>
        

      </div></div>
                <!--how it works-->
        <div class="bg-[#FFFFFF] py-20" id="how-it-works">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
          <h2 class="text-3xl md:text-4xl mb-4 font-bold text-black">
           How It Works
          </h2>
          <p class="text-xl max-w-3xl mx-auto text-black">
          Getting started with UniAttend is simple. Follow these four easy steps to transform your campus experience.
          </p>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 justify-items-center px-4 pb-12">
          <!--icon 1-->
           <div class="w-full max-w-xl text-center hover:border border-gray-300 hover:rounded-xl transform hover:scale-105  hover:shadow-xl transition-transform duration-300">
          <div class="flex justify-center mt-4 mb-4 ">
            <img
              src="https://res.cloudinary.com/dotzzcayo/image/upload/v1752669868/search_pb2v18.png"
              alt="Search icon"
              class="w-8 h-8  "
            />
          </div>

            <h1 class="text-xl font-semibold">Discover Events</h1>
            <p class="text-gray-600 text-sm py-4">
              Browse through hundreds of campus events filtered by your interests, date, and location preferences.
            </p>
          </div>
                    <!--icon 2-->
           <div class="w-full max-w-xl text-center transform hover:border border-gray-300 hover:rounded-xl hover:shadow-xl hover:scale-105 transition-transform duration-300">
          <div class="flex justify-center mt-4 mb-4 ">
            <img
              src="https://res.cloudinary.com/dotzzcayo/image/upload/v1752685924/contact_jnfo8z.webp"
              alt="Contact icon"
              class="w-8 h-8  "
            />
          </div>

            <h1 class="text-xl font-semibold">Sign Up & Join</h1>
            <p class="text-gray-600 text-sm py-4">
              Create your profile and register for events that interest you. 
            </p>
          
          
          </div>

                              <!--icon 3-->
           <div class="w-full max-w-xl text-center transform hover:border border-gray-300 hover:rounded-xl hover:shadow-xl hover:scale-105 transition-transform duration-300">
          <div class="flex justify-center mt-4 mb-4 ">
            <img
              src="https://res.cloudinary.com/dotzzcayo/image/upload/v1752686213/calender_l71pi8.png"
              alt="Calendar icon"
              class="w-8 h-8  "
            />
          </div>

            <h1 class="text-xl font-semibold">Attend & Engage</h1>
            <p class="text-gray-600 text-sm py-4">
              Show up to events, meet new people, and engage with your campus community in meaningful ways.
            </p>
          
          
          </div>

                              <!--icon 4-->
           <div class="w-full max-w-xl text-center transform hover:border border-gray-300 hover:rounded-xl hover:shadow-xl hover:scale-105 transition-transform duration-300">
          <div class="flex justify-center mt-4 mb-4 ">
            <img
              src="https://res.cloudinary.com/dotzzcayo/image/upload/v1752686745/qr_code_livz5q.png"
              alt="Qr code icon"
              class="w-8 h-8  "
            />
          </div>

            <h1 class="text-xl font-semibold">Scan to Attend</h1>
            <p class="text-gray-600 text-sm py-4">
               Show your QR code at the event entrance for quick and secure check-in, no paperwork, no stress.
            </p>
          
          
          </div>



        
        
        
        </div>

            <div class="bg-[#F4F8FB] rounded-2xl p-8  mx-auto max-w-md md:max-w-2xl">
            <h3 class="text-2xl mb-4 text-center text-black">Ready to Get Started?</h3>
            <p class="opacity-50 text-center text-black mb-6">
              Join thousands of students who are already using UniAttend to discover amazing experiences and build connections.
            </p>
            
            <router-link
              :to="{ name: 'signup' }"
              class="block bg-[#2370AC] px-8 py-3 text-white rounded-lg w-full text-center hover:scale-100 hover:bg-[#344c5e] transition-all duration-300"
            >
              Sign Up Today
            </router-link>


          </div>
          

        </div></div>
  
    <Footer/>

    
    </div>

</template>

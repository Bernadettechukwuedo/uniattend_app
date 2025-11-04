<template>
   <div>
     <div v-if="successmessage" class="text-green-500 text-center mb-4">{{ successmessage }}</div>
    <div >
    <form @submit.prevent = "handleSubmit" class="max-w-md mx-auto mt-10 mb-10 p-6 bg-white rounded-lg shadow-lg" id="form">
       
        <h2 class="text-3xl font-bold text-center mb-6">Sign in to <span class="text-[#1E5A8A]">UniAttend</span></h2>
         <div v-if="errormessage" class="text-red-500 text-center mb-4">{{ errormessage }}</div>
        <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
        <input type="email" id="email" name="email" required v-model="loginForm.email" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">

        <label for="password" class="block text-sm font-medium text-gray-700 mt-4">Password</label>
        <input type="password" v-model="loginForm.password" id="password" name="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">

        
        <label for="password1" class="block text-sm font-medium text-gray-700 mt-4"> Confirm Password</label>
        <input type="password" v-model="password1" id="password1" name="password1" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">


        <button type="submit" class="mt-6 w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-[#1a4c7a] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">Login</button>
        <p class="mt-4 text-sm text-gray-600">Don't have an account? <router-link :to="{name:'signup'}" class="text-blue-600 hover:text-blue-800">Sign Up</router-link></p>
     
    </form></div></div>

  
</template>
<script>

import api from '../../axios'; 
import { useAuthStore } from '../../stores/auth.js';

export default {
    name: 'SignupView',
    components:{
   
       
        api
       
    },
    data() {
        return {
            loginForm:{
                email: '',
                password: '',
     
            },
            password1: '',
            errormessage: "",
            successmessage: "",
            
            
        };
    },
    methods: {
        async handleSubmit() {
            if (this.loginForm.password !== this.password1) {
                this.errormessage="Passwords do not match!";
                return;
            }
            try {
                const response = await api.post('/auth/login', this.loginForm);
                console.log(response.data)
                if (response.status === 201) {
                    this.successmessage=response.data.message;
                    const auth = useAuthStore();
                    auth.login({
                        token: response.data.access_token,
                        refresh_token: response.data.refresh_token,
                        user: response.data.user
                    });
                    
            
                    if(response.data.user.role === 'student') {
                        this.$router.push({ name: 'student-dashboard' });
                        
                    }
                    else if(response.data.user.role === 'organizer') {
                        this.$router.push({ name: 'organizer-dashboard' });

                    }
                    else if(response.data.user.role === 'admin') {
                        this.$router.push({ name: 'admin-dashboard' });

                    }
                    
                    
                } else {
                    this.successmessage="Login failed: " + response.data.message;
                }
            } catch (error) {
                if(error.response){
                    this.errormessage = error.response.data.message;
                } else {
                    this.errormessage = "An error occurred during signup. Please try again";
                }

            }
        }
    },

};


</script>


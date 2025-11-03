<template>
   <div>
    <div v-if="successmessage" class="text-green-500 text-center mb-4">{{ successmessage }}</div>
    <form @submit.prevent="handleSubmit" class="max-w-md mx-auto mt-10 mb-10 p-6 bg-white rounded-lg shadow-md" id="form">
        <div v-if="errormessage" class="text-red-500 text-center mb-4">{{ errormessage }}</div>
        
        <h2 class="text-3xl font-bold text-center mb-6">Welcome to <span class="text-[#1E5A8A]">UniAttend</span></h2>
        <label for="name" class="block text-sm font-medium text-gray-700">Username</label>
        <input type="text" id="name" name="name" required v-model="signupForm.username" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
        <label for="email" class="block text-sm font-medium text-gray-700 mt-4">Email</label>
        <input type="email" v-model="signupForm.email"  id="email" name="email" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
        <label for="password" class="block text-sm font-medium text-gray-700 mt-4">Password</label>
        <input type="password" v-model="signupForm.password" id="password" name="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
        <label for="phone" class="block text-sm font-medium text-gray-700 mt-4">Phone Number</label>
        <input type="tel" v-model="signupForm.phonenumber"  id="phone" name="phone" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
        <label for="role" class="block text-sm font-medium text-gray-700 mt-4">Role</label>
        <select id="role" v-model="signupForm.role" name="role" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
            <option  value="student">Student</option>
            <option value="organizer">Organizer</option>
        </select>   
        <button class="mt-6 w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-[#1a4c7a] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">Register</button>
        <p class="mt-4 text-sm text-gray-600">Already have an account? <router-link :to="{name:'login'}" class="text-blue-600 hover:text-blue-800">Log in</router-link></p>
        
    </form></div>
 
</template>
<script>

import api from '../../axios'; 


export default {
    name: 'SignupView',
    components: {
 
        api
    },
    data() {
        return {
            signupForm:{
                username: '',
                email: '',
                password: '',
                phonenumber: '',
                role: 'student'
            },
            errormessage:"",
            successmessage:"",

        };
    },
    methods: {
        async handleSubmit() {
            try {
                const response = await api.post('/auth/register', this.signupForm);
                if (response.status === 201) {
                    this.successmessagee= response.data.message;
                    this.$router.push({ name: 'login' });
                } else {
                    this.errormessage ="Signup failed: " + response.data.message;
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


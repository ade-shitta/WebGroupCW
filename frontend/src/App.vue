<template>
        <!-- Header -->
        <header class ="main-header">
            <div class="nav-links">
                <router-link class="main-link" :to="{ name: 'Profile Page' }">
                    Profile
                </router-link>
                <router-link class="main-link" :to="{ name: 'Friends Page' }">
                    Friends
                </router-link>
                <router-link class="main-link" :to="{ name: 'Other Users Page' }">
                    Other Users
                </router-link>
            </div>
        </header>
        <RouterView class="flex-shrink-0" />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});

</script>

<style scoped>

.main-header{
    background-color:#88D2FA;
    margin: 0 rem;
    padding: 1.5rem;
}

.nav-links, .main-link{
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    text-decoration: none;               
}

.main-link:hover{
    font-weight: 500;
}

</style>

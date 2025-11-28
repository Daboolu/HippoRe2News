<template>
  <div class="layout">
    <AppSidebar />

    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import AppSidebar from "./components/AppSidebar.vue";
</script>

<style scoped>
.layout {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
.content {
  flex: 1;
  overflow: auto;
  padding: 20px;
}
</style>


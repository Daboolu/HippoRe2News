<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="sidebar">
    <ul>
      <router-link to="/">
        <li>首页</li>
      </router-link>

      <router-link to="/graph">
        <li>图谱可视化</li>
      </router-link>
    </ul>
  </div>
</template>

<style scoped>
.sidebar {
  width: 200px;
  background: #1e1e1e;
  color: white;
  padding-top: 20px;
  position: relative;
  z-index: 10;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  padding: 14px 18px;
  cursor: pointer;
}

.router-link-active li {
  color: #42b983;
  font-weight: bold;
}

.sidebar li:hover {
  background: #333;
}
</style>

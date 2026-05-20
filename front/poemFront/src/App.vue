<script setup lang="ts">
import { RouterView, useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const tabs = [
  { path: '/', name: '诗词鉴赏', icon: '📖' },
  { path: '/chain', name: '诗词接龙', icon: '🔗' },
  { path: '/feihua', name: '飞花令', icon: '🌸' },
]

function isActive(path: string) {
  return route.path === path
}
</script>

<template>
  <div class="app-container">
    <nav class="nav-bar">
      <div
        v-for="tab in tabs"
        :key="tab.path"
        class="nav-item"
        :class="{ active: isActive(tab.path) }"
        @click="router.push(tab.path)"
      >
        <span class="nav-icon">{{ tab.icon }}</span>
        <span class="nav-label">{{ tab.name }}</span>
      </div>
    </nav>
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  max-width: 720px;
  margin: 0 auto;
  padding: 0 16px;
}

.nav-bar {
  display: flex;
  gap: 0;
  padding: 16px 0 0;
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  background: var(--color-background);
  z-index: 10;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 20px;
  cursor: pointer;
  font-size: 14px;
  color: var(--color-text);
  opacity: 0.6;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  margin-bottom: -1px;
  user-select: none;
}

.nav-item:hover {
  opacity: 0.9;
  color: var(--color-heading);
}

.nav-item.active {
  opacity: 1;
  color: #8b5cf6;
  border-bottom-color: #8b5cf6;
}

.nav-icon {
  font-size: 16px;
}

.nav-label {
  font-weight: 500;
}

.main-content {
  flex: 1;
  padding: 20px 0 40px;
}

@media (max-width: 480px) {
  .nav-item {
    padding: 10px 12px;
    font-size: 13px;
  }

  .nav-label {
    font-size: 12px;
  }
}
</style>

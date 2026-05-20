<script setup lang="ts">
import { ref, computed } from 'vue'
import { usePoetryStore } from '@/stores/poetry'

const store = usePoetryStore()

const searchKeyword = ref('')
const selectedPoem = ref(store.currentPoem)
const showSearch = ref(false)

const filteredPoems = computed(() => {
  if (!searchKeyword.value.trim()) return store.poems
  return store.searchPoems(searchKeyword.value)
})

function selectPoem(poem: (typeof store.poems)[0]) {
  selectedPoem.value = poem
  showSearch.value = false
  searchKeyword.value = ''
}

function toggleSearch() {
  showSearch.value = !showSearch.value
  if (!showSearch.value) {
    searchKeyword.value = ''
  }
}
</script>

<template>
  <div class="poetry-view">
    <div class="view-header">
      <h2>诗词鉴赏</h2>
      <button class="btn-icon" @click="toggleSearch" :title="showSearch ? '关闭搜索' : '搜索诗词'">
        {{ showSearch ? '✕' : '🔍' }}
      </button>
    </div>

    <div v-if="showSearch" class="search-panel">
      <input
        v-model="searchKeyword"
        type="text"
        placeholder="搜索诗词标题、作者、诗句..."
        class="search-input"
        autofocus
      />
      <div class="search-results">
        <div
          v-for="poem in filteredPoems"
          :key="poem.id"
          class="search-item"
          @click="selectPoem(poem)"
        >
          <span class="search-item-title">{{ poem.title }}</span>
          <span class="search-item-author">{{ poem.dynasty }}·{{ poem.author }}</span>
        </div>
        <div v-if="filteredPoems.length === 0" class="no-results">
          未找到匹配的诗词
        </div>
      </div>
    </div>

    <div class="poem-card" v-if="selectedPoem">
      <div class="poem-header">
        <h3 class="poem-title">{{ selectedPoem.title }}</h3>
        <p class="poem-author">{{ selectedPoem.dynasty }} · {{ selectedPoem.author }}</p>
      </div>
      <div class="poem-content">
        <p v-for="(line, index) in selectedPoem.content" :key="index" class="poem-line">
          {{ line }}
        </p>
      </div>
      <div class="poem-appreciation">
        <h4 class="appreciation-title">赏析</h4>
        <p class="appreciation-text">{{ selectedPoem.appreciation }}</p>
      </div>
    </div>

    <div class="nav-buttons">
      <button class="btn" @click="store.nextPoem(); selectedPoem = store.currentPoem">
        下一首
      </button>
    </div>
  </div>
</template>

<style scoped>
.poetry-view {
  max-width: 640px;
  margin: 0 auto;
  padding: 16px;
}

.view-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.view-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-heading);
}

.btn-icon {
  background: none;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: var(--color-background-soft);
  border-color: var(--color-border-hover);
}

.search-panel {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 14px;
  background: var(--color-background);
  color: var(--color-text);
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.search-input:focus {
  border-color: #8b5cf6;
}

.search-results {
  margin-top: 8px;
  max-height: 240px;
  overflow-y: auto;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-background);
}

.search-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid var(--color-border);
}

.search-item:last-child {
  border-bottom: none;
}

.search-item:hover {
  background: var(--color-background-soft);
}

.search-item-title {
  font-size: 14px;
  font-weight: 500;
}

.search-item-author {
  font-size: 12px;
  color: var(--color-text);
  opacity: 0.7;
}

.no-results {
  padding: 20px;
  text-align: center;
  color: var(--color-text);
  opacity: 0.6;
  font-size: 14px;
}

.poem-card {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 24px;
  transition: border-color 0.2s;
}

.poem-card:hover {
  border-color: var(--color-border-hover);
}

.poem-header {
  text-align: center;
  margin-bottom: 20px;
}

.poem-title {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 6px;
  color: var(--color-heading);
}

.poem-author {
  font-size: 13px;
  color: var(--color-text);
  opacity: 0.7;
}

.poem-content {
  margin-bottom: 20px;
  padding: 16px 0;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.poem-line {
  text-align: center;
  font-size: 16px;
  line-height: 2.2;
  letter-spacing: 2px;
  color: var(--color-heading);
}

.poem-appreciation {
  padding-top: 4px;
}

.appreciation-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--color-heading);
}

.appreciation-text {
  font-size: 14px;
  line-height: 1.8;
  color: var(--color-text);
  opacity: 0.85;
}

.nav-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.btn {
  padding: 10px 28px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  background: #8b5cf6;
  color: #fff;
  transition: background 0.2s;
}

.btn:hover {
  background: #7c3aed;
}

@media (max-width: 480px) {
  .poem-card {
    padding: 16px;
  }

  .poem-title {
    font-size: 18px;
  }

  .poem-line {
    font-size: 14px;
  }
}
</style>

<script setup lang="ts">
import { ref, computed } from "vue";
import { usePoetryStore } from "@/stores/poetry";

const store = usePoetryStore();
const inputLine = ref("");
const message = ref("");
const gameOver = ref(false);
const chainHistory = ref<{ poem: string; line: string }[]>([]);
const currentPoem = ref(store.getRandomPoem());

const currentLastChar = computed(() => {
  const lines = currentPoem.value.content;
  return store.getLastChar(lines[lines.length - 1] ?? "");
});

chainHistory.value.push({
  poem: `${currentPoem.value.title} · ${currentPoem.value.author}`,
  line: currentPoem.value.content[currentPoem.value.content.length - 1] ?? "",
});

function submitLine() {
  const input = inputLine.value.trim();
  if (!input) return;

  const firstChar = store.getFirstChar(input);
  if (firstChar !== currentLastChar.value) {
    message.value = `请输入以"${currentLastChar.value}"开头的诗句`;
    return;
  }

  const match = store.findLinesContainingChar(firstChar);
  let found = false;
  for (const item of match) {
    for (const line of item.poem.content) {
      if (line === input && !chainHistory.value.some((h) => h.line === line)) {
        found = true;
        chainHistory.value.push({
          poem: `${item.poem.title} · ${item.poem.author}`,
          line: input,
        });
        currentPoem.value = item.poem;
        store.addScore(10);
        message.value = `接龙成功！+10分`;
        inputLine.value = "";
        break;
      }
    }
    if (found) break;
  }

  if (!found) {
    message.value = "未找到匹配的诗句，请重新输入";
  }
}

function skipTurn() {
  let newPoem = store.getRandomPoem();
  while (newPoem.id === currentPoem.value.id) {
    newPoem = store.getRandomPoem();
  }
  currentPoem.value = newPoem;
  const lastLine =
    currentPoem.value.content[currentPoem.value.content.length - 1] ?? "";
  chainHistory.value.push({
    poem: `${currentPoem.value.title} · ${currentPoem.value.author}`,
    line: lastLine,
  });
  message.value = `已切换诗词，请以"${currentLastChar.value}"开头接龙`;
  inputLine.value = "";
}

function resetGame() {
  store.resetScore();
  chainHistory.value = [];
  gameOver.value = false;
  message.value = "";
  inputLine.value = "";
  currentPoem.value = store.getRandomPoem();
  chainHistory.value.push({
    poem: `${currentPoem.value.title} · ${currentPoem.value.author}`,
    line: currentPoem.value.content[currentPoem.value.content.length - 1] ?? "",
  });
}

function endGame() {
  gameOver.value = true;
}
</script>

<template>
  <div class="chain-view">
    <div class="view-header">
      <h2>诗词接龙</h2>
      <div class="score-badge">得分：{{ store.score }}</div>
    </div>

    <div class="game-intro">
      <p>根据上句的最后一个字，接上以此字开头的诗句</p>
    </div>

    <div class="chain-display" v-if="!gameOver">
      <div class="current-prompt">
        <span class="prompt-label">当前尾字：</span>
        <span class="prompt-char">{{ currentLastChar }}</span>
      </div>

      <div class="input-area">
        <input
          v-model="inputLine"
          type="text"
          placeholder="请输入以此字开头的诗句..."
          class="chain-input"
          @keyup.enter="submitLine"
        />
        <div class="input-actions">
          <button class="btn btn-primary" @click="submitLine">提交</button>
          <button class="btn btn-secondary" @click="skipTurn">换一首</button>
          <button class="btn btn-danger" @click="endGame">结束</button>
        </div>
      </div>

      <p
        v-if="message"
        class="message"
        :class="{ error: message.includes('未找到') }"
      >
        {{ message }}
      </p>
    </div>

    <div v-if="gameOver" class="game-over">
      <h3>接龙结束</h3>
      <p>
        最终得分：<strong>{{ store.score }}</strong>
      </p>
      <button class="btn btn-primary" @click="resetGame">再来一次</button>
    </div>

    <div class="chain-history">
      <h4 class="history-title">接龙记录</h4>
      <div class="history-list">
        <div
          v-for="(item, index) in chainHistory"
          :key="index"
          class="history-item"
        >
          <span class="history-index">{{ index + 1 }}</span>
          <div class="history-content">
            <p class="history-line">{{ item.line }}</p>
            <p class="history-source">{{ item.poem }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chain-view {
  max-width: 640px;
  margin: 0 auto;
  padding: 16px;
}

.view-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.view-header h2 {
  font-size: 20px;
  font-weight: 600;
}

.score-badge {
  background: #8b5cf6;
  color: #fff;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.game-intro {
  margin-bottom: 20px;
  font-size: 13px;
  color: var(--color-text);
  opacity: 0.7;
  text-align: center;
}

.current-prompt {
  text-align: center;
  margin-bottom: 16px;
  padding: 16px;
  background: var(--color-background-soft);
  border-radius: 12px;
  border: 1px solid var(--color-border);
}

.prompt-label {
  font-size: 14px;
  color: var(--color-text);
  opacity: 0.7;
}

.prompt-char {
  font-size: 36px;
  font-weight: 700;
  color: #8b5cf6;
  margin-left: 8px;
}

.input-area {
  margin-bottom: 12px;
}

.chain-input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 15px;
  background: var(--color-background);
  color: var(--color-text);
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.chain-input:focus {
  border-color: #8b5cf6;
}

.input-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.btn {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary {
  background: #8b5cf6;
  color: #fff;
}

.btn-primary:hover {
  background: #7c3aed;
}

.btn-secondary {
  background: var(--color-background-soft);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  border-color: var(--color-border-hover);
}

.btn-danger {
  background: transparent;
  color: #ef4444;
  border: 1px solid #ef4444;
}

.btn-danger:hover {
  background: #fef2f2;
}

.message {
  text-align: center;
  font-size: 13px;
  padding: 8px;
  border-radius: 6px;
  margin-bottom: 12px;
  color: #059669;
  background: #ecfdf5;
}

.message.error {
  color: #dc2626;
  background: #fef2f2;
}

.game-over {
  text-align: center;
  padding: 32px 16px;
  background: var(--color-background-soft);
  border-radius: 12px;
  border: 1px solid var(--color-border);
  margin-bottom: 20px;
}

.game-over h3 {
  font-size: 20px;
  margin-bottom: 12px;
}

.game-over p {
  font-size: 16px;
  margin-bottom: 20px;
}

.game-over strong {
  font-size: 24px;
  color: #8b5cf6;
}

.chain-history {
  margin-top: 20px;
}

.history-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 10px;
}

.history-list {
  max-height: 300px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  gap: 12px;
  padding: 10px 12px;
  border-left: 3px solid #8b5cf6;
  background: var(--color-background-soft);
  border-radius: 0 8px 8px 0;
  margin-bottom: 8px;
}

.history-index {
  font-size: 12px;
  font-weight: 600;
  color: #8b5cf6;
  min-width: 20px;
  padding-top: 2px;
}

.history-content {
  flex: 1;
}

.history-line {
  font-size: 14px;
  color: var(--color-heading);
  margin-bottom: 2px;
}

.history-source {
  font-size: 12px;
  color: var(--color-text);
  opacity: 0.6;
}
</style>

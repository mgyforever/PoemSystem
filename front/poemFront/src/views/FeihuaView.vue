<script setup lang="ts">
import { ref, computed } from 'vue'
import { usePoetryStore } from '@/stores/poetry'

const store = usePoetryStore()

const feihuaChars = ['花', '月', '风', '春', '雪', '山', '水', '云', '日', '雨']
const currentChar = ref('')
const gameStarted = ref(false)
const gameOver = ref(false)
const inputLine = ref('')
const message = ref('')
const score = ref(0)
const foundLines = ref<{ poem: string; line: string }[]>([])
const usedLines = ref(new Set<string>())
const timer = ref(0)
const timerInterval = ref<ReturnType<typeof setInterval> | null>(null)
const timeLimit = 120

function startGame(char: string) {
  currentChar.value = char
  gameStarted.value = true
  gameOver.value = false
  score.value = 0
  foundLines.value = []
  usedLines.value = new Set()
  message.value = `请说出含有"${char}"字的诗句`
  inputLine.value = ''
  timer.value = timeLimit
  if (timerInterval.value) clearInterval(timerInterval.value)
  timerInterval.value = setInterval(() => {
    timer.value--
    if (timer.value <= 0) {
      endGame()
    }
  }, 1000)
}

function submitLine() {
  const input = inputLine.value.trim()
  if (!input) return

  if (usedLines.value.has(input)) {
    message.value = '这句已经用过了，换一句吧'
    return
  }

  if (!input.includes(currentChar.value)) {
    message.value = `诗句中必须包含"${currentChar.value}"字`
    return
  }

  const match = store.findLinesContainingChar(currentChar.value)
  let found = false
  for (const item of match) {
    if (item.line === input) {
      found = true
      usedLines.value.add(input)
      foundLines.value.push({
        poem: `${item.poem.title} · ${item.poem.author}`,
        line: input,
      })
      score.value += 10
      message.value = `正确！+10分`
      inputLine.value = ''
      break
    }
  }

  if (!found) {
    message.value = '未在诗库中找到此句，请确认后重试'
  }
}

function giveUp() {
  endGame()
}

function endGame() {
  gameOver.value = true
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
}

function backToSelect() {
  gameStarted.value = false
  gameOver.value = false
  foundLines.value = []
  usedLines.value = new Set()
  score.value = 0
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
}

const formattedTime = computed(() => {
  const min = Math.floor(timer.value / 60)
  const sec = timer.value % 60
  return `${min}:${sec.toString().padStart(2, '0')}`
})

const remainingMatches = computed(() => {
  if (!currentChar.value) return []
  const all = store.findLinesContainingChar(currentChar.value)
  return all.filter(item => !usedLines.value.has(item.line))
})
</script>

<template>
  <div class="feihua-view">
    <div class="view-header">
      <h2>飞花令</h2>
    </div>

    <div v-if="!gameStarted" class="char-select">
      <p class="select-intro">选择一个字，开始飞花令</p>
      <div class="char-grid">
        <button
          v-for="char in feihuaChars"
          :key="char"
          class="char-btn"
          @click="startGame(char)"
        >
          {{ char }}
        </button>
      </div>
      <p class="select-hint">说出含有该字的诗句，尽可能多地接龙</p>
    </div>

    <div v-else class="game-area">
      <div class="game-header">
        <div class="current-char-display">
          <span class="char-label">关键字</span>
          <span class="char-value">{{ currentChar }}</span>
        </div>
        <div class="game-status">
          <div class="timer-display" :class="{ warning: timer <= 30 }">
            {{ formattedTime }}
          </div>
          <div class="score-display">{{ score }} 分</div>
        </div>
      </div>

      <div v-if="!gameOver" class="input-section">
        <input
          v-model="inputLine"
          type="text"
          :placeholder='`请输入含有"${currentChar}"字的诗句...`'
          class="feihua-input"
          @keyup.enter="submitLine"
        />
        <div class="input-actions">
          <button class="btn btn-primary" @click="submitLine">提交</button>
          <button class="btn btn-secondary" @click="giveUp">认输</button>
        </div>
        <p v-if="message" class="message" :class="{ error: message.includes('未') || message.includes('确认') }">
          {{ message }}
        </p>
      </div>

      <div v-if="gameOver" class="game-over">
        <h3>飞花令结束</h3>
        <p>关键字：<strong>"{{ currentChar }}"</strong></p>
        <p>得分：<strong>{{ score }}</strong></p>
        <p>共说出 {{ foundLines.length }} 句含"{{ currentChar }}"的诗句</p>
        <div class="game-over-actions">
          <button class="btn btn-primary" @click="startGame(currentChar)">再来一次</button>
          <button class="btn btn-secondary" @click="backToSelect">选择其他字</button>
        </div>
      </div>

      <div class="found-section">
        <h4 class="found-title">
          已说出的诗句（{{ foundLines.length }}）
          <span v-if="!gameOver" class="remaining">
            还剩 {{ remainingMatches.length }} 句可接
          </span>
        </h4>
        <div class="found-list">
          <div
            v-for="(item, index) in foundLines"
            :key="index"
            class="found-item"
          >
            <span class="found-index">{{ index + 1 }}</span>
            <div class="found-content">
              <p class="found-line">{{ item.line }}</p>
              <p class="found-source">{{ item.poem }}</p>
            </div>
          </div>
          <div v-if="foundLines.length === 0" class="empty-hint">
            还没有说出诗句，开始挑战吧
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.feihua-view {
  max-width: 640px;
  margin: 0 auto;
  padding: 16px;
}

.view-header {
  margin-bottom: 20px;
}

.view-header h2 {
  font-size: 20px;
  font-weight: 600;
}

.select-intro {
  text-align: center;
  font-size: 14px;
  margin-bottom: 20px;
  color: var(--color-text);
  opacity: 0.8;
}

.char-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.char-btn {
  padding: 16px 8px;
  font-size: 24px;
  font-weight: 700;
  border: 2px solid var(--color-border);
  border-radius: 12px;
  background: var(--color-background);
  color: var(--color-heading);
  cursor: pointer;
  transition: all 0.2s;
}

.char-btn:hover {
  border-color: #8b5cf6;
  color: #8b5cf6;
  background: var(--color-background-soft);
  transform: translateY(-2px);
}

.select-hint {
  text-align: center;
  font-size: 12px;
  color: var(--color-text);
  opacity: 0.6;
}

.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: var(--color-background-soft);
  border-radius: 12px;
  border: 1px solid var(--color-border);
}

.current-char-display {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.char-label {
  font-size: 11px;
  color: var(--color-text);
  opacity: 0.6;
  margin-bottom: 4px;
}

.char-value {
  font-size: 36px;
  font-weight: 700;
  color: #8b5cf6;
}

.game-status {
  text-align: right;
}

.timer-display {
  font-size: 24px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  margin-bottom: 4px;
}

.timer-display.warning {
  color: #ef4444;
}

.score-display {
  font-size: 14px;
  color: var(--color-text);
  opacity: 0.7;
}

.input-section {
  margin-bottom: 20px;
}

.feihua-input {
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

.feihua-input:focus {
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

.message {
  text-align: center;
  font-size: 13px;
  padding: 8px;
  border-radius: 6px;
  margin-top: 10px;
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
  font-size: 14px;
  margin-bottom: 6px;
}

.game-over strong {
  font-size: 20px;
  color: #8b5cf6;
}

.game-over-actions {
  display: flex;
  gap: 8px;
  margin-top: 20px;
}

.found-section {
  margin-top: 8px;
}

.found-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.remaining {
  font-size: 12px;
  font-weight: 400;
  opacity: 0.6;
}

.found-list {
  max-height: 280px;
  overflow-y: auto;
}

.found-item {
  display: flex;
  gap: 12px;
  padding: 10px 12px;
  border-left: 3px solid #8b5cf6;
  background: var(--color-background-soft);
  border-radius: 0 8px 8px 0;
  margin-bottom: 8px;
}

.found-index {
  font-size: 12px;
  font-weight: 600;
  color: #8b5cf6;
  min-width: 20px;
  padding-top: 2px;
}

.found-content {
  flex: 1;
}

.found-line {
  font-size: 14px;
  color: var(--color-heading);
  margin-bottom: 2px;
}

.found-source {
  font-size: 12px;
  color: var(--color-text);
  opacity: 0.6;
}

.empty-hint {
  text-align: center;
  padding: 24px;
  color: var(--color-text);
  opacity: 0.5;
  font-size: 14px;
}

@media (max-width: 480px) {
  .char-grid {
    gap: 8px;
  }

  .char-btn {
    padding: 12px 4px;
    font-size: 20px;
  }
}
</style>

import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { poems, getRandomPoem } from "@/data/poems";
import type { Poem } from "@/data/poems";

export const usePoetryStore = defineStore("poetry", () => {
  const currentPoem = ref(getRandomPoem());
  const score = ref(0);

  const lastCharIndex = computed(() => {
    const lines = currentPoem.value.content;
    if (lines.length === 0) return 0;
    return lines.length - 1;
  });

  function getLastChar(line: string): string {
    return line.charAt(line.length - 1);
  }

  function getFirstChar(line: string): string {
    return line.charAt(0);
  }

  function findChainMatch(lastChar: string): Poem | null {
    for (const poem of poems) {
      const firstLine = poem.content[0] ?? "";
      if (
        getFirstChar(firstLine) === lastChar &&
        poem.id !== currentPoem.value.id
      ) {
        return poem;
      }
    }
    return null;
  }

  function findLinesContainingChar(
    char: string,
  ): { poem: Poem; lineIndex: number; line: string }[] {
    const results: { poem: Poem; lineIndex: number; line: string }[] = [];
    const seen = new Set<string>();
    for (const poem of poems) {
      poem.content.forEach((line, index) => {
        if (line.includes(char) && !seen.has(line)) {
          seen.add(line);
          results.push({ poem, lineIndex: index, line });
        }
      });
    }
    return results;
  }

  function nextPoem() {
    currentPoem.value = getRandomPoem();
  }

  function setPoem(poem: Poem) {
    currentPoem.value = poem;
  }

  function addScore(points: number) {
    score.value += points;
  }

  function resetScore() {
    score.value = 0;
  }

  function searchPoems(keyword: string): Poem[] {
    if (!keyword.trim()) return poems;
    const kw = keyword.trim().toLowerCase();
    return poems.filter(
      (p) =>
        p.title.includes(kw) ||
        p.author.includes(kw) ||
        p.content.some((line) => line.includes(kw)) ||
        p.dynasty.includes(kw),
    );
  }

  return {
    currentPoem,
    score,
    lastCharIndex,
    poems,
    getLastChar,
    getFirstChar,
    findChainMatch,
    findLinesContainingChar,
    nextPoem,
    setPoem,
    addScore,
    resetScore,
    searchPoems,
    getRandomPoem,
  };
});

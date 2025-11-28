<script setup>
import { ref } from "vue";
import axios from "axios";

const query = ref("");
const loading = ref(false);
const error = ref("");

const hippoResult = ref(null);
const standardResult = ref(null);

const API_BASE = "http://10.250.17.244:8000";

// 默认示例问题
const exampleQuery = "绿水青山怎么从口号变成现实？";

const search = async () => {
  error.value = "";
  hippoResult.value = null;
  standardResult.value = null;

  if (!query.value.trim()) {
    error.value = "请输入检索内容！";
    return;
  }

  loading.value = true;

  try {
    const hippo = axios.post(`${API_BASE}/retrieve`, { query: query.value });
    const standard = axios.post(`${API_BASE}/standard/retrieve`, { query: query.value });

    const [hippoRes, standardRes] = await Promise.all([hippo, standard]);
    hippoResult.value = hippoRes.data;
    standardResult.value = standardRes.data;

  } catch (e) {
    error.value = "请求后端失败，请检查服务是否启动与 CORS 设置。";
  } finally {
    loading.value = false;
  }
};

// 点击提示示例直接检索
const useExample = async () => {
  query.value = exampleQuery;
  await search();
};
</script>

<template>
  <div class="page">

    <h1>GraphRAG vs StandardRAG 检索对比, 提升检索的语义理解</h1>

    <div class="search">
      <input
        v-model="query"
        autofocus
        placeholder="按 Enter 进行搜索，例如：绿水青山怎么从口号变成现实？"
        @keydown.enter.prevent="search"
      />
      <button :disabled="loading" @click="search">
        {{ loading ? '检索中...' : '搜索' }}
      </button>
    </div>

    <div class="hint">
      示例：<span class="hint-link" @click="useExample">{{ exampleQuery }}</span>
    </div>

    <div v-if="error" class="error">{{ error }}</div>

    <div class="compare">
      <div class="col">
        <h2>HippoRAG</h2>
        <div v-if="hippoResult">
          <div v-for="(p, i) in hippoResult.passages" :key="i" class="card">
            <div class="meta">
              Score: {{ hippoResult.passages_scores[i]?.toFixed(10) }}
            </div>
            <p>{{ p }}</p>
          </div>
        </div>
      </div>

      <div class="col">
        <h2>StandardRAG</h2>
        <div v-if="standardResult">
          <div v-for="(p, i) in standardResult.passages" :key="i" class="card">
            <div class="meta">
              Score: {{ standardResult.passages_scores[i]?.toFixed(4) }}
            </div>
            <p>{{ p }}</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.page { padding: 24px; max-width: 1200px; margin: auto; }
.search { display: flex; gap: 10px; margin-bottom: 10px; }
.search input { flex: 1; padding: 8px; font-size: 16px; }
.hint { font-size: 14px; color: #555; margin-bottom: 20px; }
.hint-link { color: #007bff; cursor: pointer; text-decoration: underline; }
.hint-link:hover { color: #0056b3; }
.compare { display: flex; gap: 24px; }
.col { flex: 1; border: 1px solid #ddd; padding: 12px; border-radius: 8px; }
.card { border-bottom: 1px solid #eee; padding: 8px 0; }
.meta { font-size: 12px; color: gray; margin-bottom: 4px; }
.error { color: red; margin-bottom: 10px; }
</style>

<template>
  <div class="news-kg">

    <!-- 🔍 顶部搜索区域 -->
    <header class="search-header">
      <div class="search-container">
        <div class="search-input-wrapper">
          <div class="search-input-group">
            <input
              v-model="query"
              type="text"
              placeholder="输入关键词搜索素材..."
              class="search-input"
              @keyup.enter="search"
            />
            <button class="search-btn" :class="{ loading: loading }" :disabled="loading" @click="search">
              <svg v-if="!loading" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="11" cy="11" r="8" stroke-width="2" />
                <path d="m21 21-4.35-4.35" stroke-width="2" />
              </svg>
              <div v-else class="loading-spinner"></div>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 🧠 主布局：左侧实体 + 右侧图谱 -->
    <section class="content">
      <aside class="entity-panel">
        <div class="panel-header">
          <div style="display:flex; align-items:center; gap:10px;">
            <button
              style="border:1px solid #e5e7eb;background:#fff;color:#374151;padding:2px 12px;border-radius:6px;font-size:13px;cursor:pointer;"
              @click="toggleSelectAll"
            >全选</button>
            <h4 style="margin:0;">实体列表</h4>
          </div>
          <small>已选 {{ selectedEntityArray.length }}/{{ entitiesRanked.length }}</small>
        </div>

        <div class="entity-list">
          <label v-for="e in entitiesRanked" :key="e.id" class="entity-item">
            <input type="checkbox" :value="e.id" v-model="selectedEntityArray" />
            <span class="name" :class="{ active: isSelected(e.id) }">{{ e.id }}</span>
            <span class="badge">{{ e.count }}</span>
          </label>
        </div>
      </aside>

      <div class="graph-wrap">
        <button class="expand-btn" @click="expand" :disabled="nodes.length === 0">
          扩展一跳
        </button>
        <div ref="chartRef" class="echart"></div>
      </div>
    </section>

    <!-- 📄文章列表展示 -->
    <section style="margin-top:20px;">
      <h2>相关文章 Passages</h2>
      <div v-if="passages.length === 0" style="padding:10px;color:#666;">暂无相关文章</div>

      <div v-else>
        <div v-for="(p,i) in passages" :key="i" class="card">
          <div class="meta">Score: {{ passageScores[i]?.toFixed(10) }}</div>
          <p>{{ p }}</p>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import axios from "axios";
import * as echarts from "echarts";

const API_BASE = "http://10.250.17.244:8000";

// states
const query = ref("");
const loading = ref(false);

const nodes = ref([]);
const edges = ref([]);
const passages = ref([]);
const passageScores = ref([]);

const chartRef = ref(null);
let chartInstance = null;

// entity ranking list
const entitiesRanked = ref([]);
const selectedEntities = ref(new Set());

const selectedEntityArray = computed({
  get() { return Array.from(selectedEntities.value) },
  set(arr) { selectedEntities.value = new Set(arr) }
});

function isSelected(id) { return selectedEntities.value.has(id) }

function toggleSelectAll() {
  const all = entitiesRanked.value.map(e => e.id);
  if (selectedEntities.value.size === all.length) selectedEntities.value.clear();
  else selectedEntities.value = new Set(all);
}

// 🎯 search
async function search() {
  if (!query.value.trim() || loading.value) return;
  loading.value = true;
  try {
    const res = await axios.post(`${API_BASE}/graph/subgraph_all`, { query: query.value });
    fillData(res.data);
    buildGraph(res.data.subgraph_edges);
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

// 🎯 expand
async function expand() {
  const res = await axios.post(`${API_BASE}/graph/subgraph_expand`, {
    current_nodes: nodes.value
  });
  fillData(res.data);
  buildGraph(res.data.subgraph_edges);
}

// 📦 update local UI states
function fillData(data) {
  // passages 排序：根据贡献度 (C)
  const scoreMap = {};
  for (let i = 0; i < data.passages.length; i++) {
    scoreMap[data.passages[i]] = data.passages_scores[i];
  }

  passages.value = [...data.passages].sort((a, b) => scoreMap[b] - scoreMap[a]);
  passageScores.value = passages.value.map(p => scoreMap[p]);

  // 实体排名
  const freq = {};
  data.subgraph_edges.forEach(e => {
    freq[e.source] = (freq[e.source] || 0) + 1;
    freq[e.target] = (freq[e.target] || 0) + 1;
  });

  entitiesRanked.value = Object.keys(freq)
    .map(k => ({ id: k, count: freq[k] }))
    .sort((a, b) => b.count - a.count);

  selectedEntities.value = new Set(entitiesRanked.value.slice(0, 6).map(e => e.id));
}

// 🕸 build graph
function buildGraph(edgeList) {
  const nodeSet = new Set();
  edgeList.forEach(e => {
    nodeSet.add(e.source);
    nodeSet.add(e.target);
  });
  nodes.value = Array.from(nodeSet);

  const graphNodes = nodes.value.map(n => ({
    name: n,
    draggable: true,
    symbolSize: 40 + (entitiesRanked.value.find(x => x.id === n)?.count || 1) * 2
  }));

  edges.value = edgeList.map(e => ({
    source: e.source,
    target: e.target,
    value: e.relation,
    label: { show: true, formatter: e.relation },
    lineStyle: { width: Math.max(1, e.weight) }
  }));

  if (!chartInstance) chartInstance = echarts.init(chartRef.value);

  chartInstance.setOption({
    tooltip: {},
    series: [{
      type: "graph",
      layout: "force",
      roam: true,
      label: { show: true, fontSize: 13 },
      edgeLabel: { show: true, formatter: p => p.data.value },
      data: graphNodes,
      edges: edges.value,
      force: { repulsion: 1600, edgeLength: 200 }
    }]
  });
}
</script>

<style scoped>
.news-kg { display:flex; flex-direction:column; gap:12px; }

/* search header */
.search-header {
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(10px);
    padding: 2rem 0;
    background-size:cover;
}

.search-container { max-width:1200px; margin:0 auto; }
.search-input-group { display:flex; align-items:center;background:#fff;border-radius:50px;overflow:hidden; }

.search-input { flex:1;padding:1rem 1.5rem;font-size:1.3rem;border:none;outline:none; }
.search-btn { border:none;background:#ed2800;color:#fff;padding:1rem;cursor:pointer; }
.search-btn.loading { pointer-events:none; }
.loading-spinner { width:20px;height:20px;border:2px solid rgba(255,255,255,.3);border-top:2px solid white;border-radius:50%;animation:spin 1s linear infinite; }
@keyframes spin { 0%{transform:rotate(0)}100%{transform:rotate(360deg)} }

/* grid layout with sidebar */
.content {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 12px;
}

.entity-panel { background:#fff;border:1px solid #eee;border-radius:16px;padding:10px;display:flex;flex-direction:column; }
.entity-list { overflow:auto;max-height: calc(80vh - 60px); }
.entity-item { display:flex; align-items:center; gap:8px; padding:6px; cursor:pointer; }
.entity-item:hover { background:#f8f9fb; }
.badge { padding:0 6px;background:#ddd;border-radius:8px;font-size:12px; }

/* graph container */
.graph-wrap { background:#fff;border:1px solid #ddd;border-radius:16px;padding:10px; }
.echart { height:70vh; }
.expand-btn { margin-bottom:10px;padding:6px 14px;border-radius:8px;border:1px solid #ccc;background:#fff;cursor:pointer; }

/* passage card */
.card { border-bottom:1px solid #eee;padding:8px 0; }
.meta { font-size:12px;color:gray;margin-bottom:4px; }
</style>

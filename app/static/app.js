const els = {
  healthDot: document.querySelector("#healthDot"),
  healthText: document.querySelector("#healthText"),
  ingestBtn: document.querySelector("#ingestBtn"),
  roleSelect: document.querySelector("#roleSelect"),
  userId: document.querySelector("#userId"),
  sessionId: document.querySelector("#sessionId"),
  chatLog: document.querySelector("#chatLog"),
  chatForm: document.querySelector("#chatForm"),
  queryInput: document.querySelector("#queryInput"),
  sendBtn: document.querySelector("#sendBtn"),
  clearBtn: document.querySelector("#clearBtn"),
  planList: document.querySelector("#planList"),
  citationList: document.querySelector("#citationList"),
  reflectionBox: document.querySelector("#reflectionBox"),
  toolResult: document.querySelector("#toolResult"),
};

const toolForms = {
  weight: document.querySelector("#weightTool"),
  carbon: document.querySelector("#carbonTool"),
  energy: document.querySelector("#energyTool"),
  fault: document.querySelector("#faultTool"),
  production: document.querySelector("#productionTool"),
};

function addMessage(role, text) {
  const node = document.createElement("div");
  node.className = `message ${role}`;
  node.textContent = text;
  els.chatLog.appendChild(node);
  els.chatLog.scrollTop = els.chatLog.scrollHeight;
  return node;
}

function setBusy(isBusy) {
  els.sendBtn.disabled = isBusy;
  els.sendBtn.textContent = isBusy ? "发送中" : "发送";
}

function createProgressMessage() {
  const steps = ["安全检查", "问题分类", "检索知识库", "判断工具调用", "生成回答"];
  const node = addMessage("assistant progress", `处理中...\n- ${steps[0]}`);
  let index = 1;
  const timer = window.setInterval(() => {
    const visibleSteps = steps.slice(0, Math.min(index + 1, steps.length));
    node.textContent = `处理中...\n${visibleSteps.map((step) => `- ${step}`).join("\n")}`;
    els.chatLog.scrollTop = els.chatLog.scrollHeight;
    if (index < steps.length - 1) {
      index += 1;
    }
  }, 650);
  return { node, timer };
}

function finishProgressMessage(progress, plan = []) {
  window.clearInterval(progress.timer);
  if (plan.length) {
    progress.node.textContent = `处理过程：\n${plan.map((step) => `- ${step}`).join("\n")}`;
  } else {
    progress.node.textContent = "处理过程：已完成请求处理";
  }
  els.chatLog.scrollTop = els.chatLog.scrollHeight;
}

function renderPlan(items = []) {
  els.planList.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    els.planList.appendChild(li);
  });
}

function renderCitations(citations = []) {
  els.citationList.innerHTML = "";
  if (!citations.length) {
    els.citationList.className = "citation-list empty";
    els.citationList.textContent = "暂无引用";
    return;
  }
  els.citationList.className = "citation-list";
  citations.forEach((citation) => {
    const item = document.createElement("div");
    item.className = "citation";
    const title = citation.title || citation.doc_id || "知识片段";
    const meta = [
      citation.doc_id ? `文档：${citation.doc_id}` : "",
      citation.security_level ? `权限：${citation.security_level}` : "",
      citation.score !== undefined ? `相似度：${citation.score}` : "",
    ].filter(Boolean).join("  ");
    item.innerHTML = `<strong></strong><span></span>`;
    item.querySelector("strong").textContent = title;
    item.querySelector("span").textContent = meta || "已用于回答生成";
    els.citationList.appendChild(item);
  });
}

function renderReflection(reflection = {}) {
  els.reflectionBox.innerHTML = "";
  if (!Object.keys(reflection).length) {
    els.reflectionBox.className = "reflection-box empty";
    els.reflectionBox.textContent = "暂无检查结果";
    return;
  }
  els.reflectionBox.className = "reflection-box";
  renderResultInto(els.reflectionBox, {
    passed: reflection.passed ? "通过" : "需关注",
    issues: reflection.issues && reflection.issues.length ? reflection.issues.join("；") : "无",
  });
}

function renderResult(data) {
  els.toolResult.className = "tool-result";
  els.toolResult.innerHTML = "";
  renderResultInto(els.toolResult, data);
}

function renderResultInto(container, data) {
  Object.entries(data).forEach(([key, value]) => {
    const row = document.createElement("div");
    row.className = "result-row";
    row.innerHTML = `<b></b><span></span>`;
    row.querySelector("b").textContent = key;
    row.querySelector("span").textContent = Array.isArray(value) || typeof value === "object"
      ? JSON.stringify(value, null, 2)
      : String(value);
    container.appendChild(row);
  });
}

function formPayload(form) {
  return Object.fromEntries([...new FormData(form).entries()].map(([key, value]) => {
    const numberValue = Number(value);
    return [key, value === "" || Number.isNaN(numberValue) ? value : numberValue];
  }));
}

async function postJson(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json();
}

async function loadHealth() {
  try {
    const response = await fetch("/health");
    const data = await response.json();
    els.healthDot.className = "status-dot ok";
    els.healthText.textContent = `${data.project} 在线`;
  } catch (error) {
    els.healthDot.className = "status-dot fail";
    els.healthText.textContent = "服务未连接";
  }
}

async function loadRoles() {
  try {
    const response = await fetch("/roles");
    const roles = await response.json();
    els.roleSelect.innerHTML = "";
    Object.keys(roles).forEach((role) => {
      const option = document.createElement("option");
      option.value = role;
      option.textContent = role;
      if (role === "engineer") option.selected = true;
      els.roleSelect.appendChild(option);
    });
  } catch (error) {
    addMessage("system", `角色列表加载失败：${error.message}`);
  }
}

els.chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = els.queryInput.value.trim();
  if (!query) return;

  addMessage("user", query);
  els.queryInput.value = "";
  setBusy(true);
  const progress = createProgressMessage();

  try {
    const data = await postJson("/chat", {
      session_id: els.sessionId.value.trim() || "default",
      user_id: els.userId.value.trim() || "anonymous",
      role: els.roleSelect.value,
      query,
    });
    finishProgressMessage(progress, data.plan);
    addMessage("assistant", data.answer);
    renderPlan(data.plan);
    renderCitations(data.citations);
    renderReflection(data.reflection);
  } catch (error) {
    window.clearInterval(progress.timer);
    progress.node.textContent = "处理过程：请求失败";
    addMessage("system", `请求失败：${error.message}`);
  } finally {
    setBusy(false);
  }
});

els.clearBtn.addEventListener("click", () => {
  els.chatLog.innerHTML = "";
  renderPlan([]);
  renderCitations([]);
  renderReflection({});
});

els.ingestBtn.addEventListener("click", async () => {
  els.ingestBtn.disabled = true;
  els.ingestBtn.textContent = "索引重建中";
  try {
    const data = await postJson("/ingest", {});
    addMessage("system", `知识库索引已重建：${data.doc_count} 份文档`);
  } catch (error) {
    addMessage("system", `索引重建失败：${error.message}`);
  } finally {
    els.ingestBtn.disabled = false;
    els.ingestBtn.textContent = "重建知识库索引";
  }
});

document.querySelectorAll("[data-question]").forEach((button) => {
  button.addEventListener("click", () => {
    els.queryInput.value = button.dataset.question;
    els.queryInput.focus();
  });
});

document.querySelectorAll("[data-tool]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-tool]").forEach((tab) => tab.classList.remove("active"));
    Object.values(toolForms).forEach((form) => form.classList.remove("active"));
    button.classList.add("active");
    toolForms[button.dataset.tool].classList.add("active");
  });
});

toolForms.weight.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    renderResult(await postJson("/tool/steel-weight", formPayload(toolForms.weight)));
  } catch (error) {
    renderResult({ error: error.message });
  }
});

toolForms.carbon.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    renderResult(await postJson("/tool/carbon-emission", formPayload(toolForms.carbon)));
  } catch (error) {
    renderResult({ error: error.message });
  }
});

toolForms.energy.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    renderResult(await postJson("/tool/energy-cost", formPayload(toolForms.energy)));
  } catch (error) {
    renderResult({ error: error.message });
  }
});

toolForms.fault.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    renderResult(await postJson("/tool/fault-diagnosis", formPayload(toolForms.fault)));
  } catch (error) {
    renderResult({ error: error.message });
  }
});

toolForms.production.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    renderResult(await postJson("/tool/production-indicator", formPayload(toolForms.production)));
  } catch (error) {
    renderResult({ error: error.message });
  }
});

addMessage("assistant", "您好，我是 SteelAgent-RAG。请选择角色后输入问题，或直接使用右侧工具计算。");
loadHealth();
loadRoles();

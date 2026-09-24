/* MetrôBot SP — interface web.
 * Só apresentação: toda a decisão (busca, regras e LLM) acontece no servidor. */
"use strict";

const $ = (sel) => document.querySelector(sel);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

let DADOS = null;

// ---------- comunicação ----------
async function api(rota, corpo) {
  const opcoes = corpo
    ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corpo) }
    : {};
  const resposta = await fetch(rota, opcoes);
  if (!resposta.ok) throw new Error(`${rota}: HTTP ${resposta.status}`);
  return resposta.json();
}

const nomeLinha = (chave) => (DADOS.nomes_linhas[chave] || chave);
const corLinha = (chave) => (DADOS.cores[chave] || "#666");

// ---------- montagem do formulário ----------
function montarFormulario() {
  const origem = $("#origem");
  const destino = $("#destino");

  for (const [local, estacao] of Object.entries(DADOS.locais)) {
    for (const sel of [origem, destino]) {
      const o = document.createElement("option");
      o.value = local;
      o.textContent = `📍 ${local} (${estacao})`;
      sel.appendChild(o);
    }
  }
  for (const est of DADOS.estacoes) {
    for (const sel of [origem, destino]) {
      const o = document.createElement("option");
      o.value = est;
      o.textContent = `🚇 ${est}`;
      sel.appendChild(o);
    }
  }
  origem.value = "Pinacoteca";
  destino.value = "Tatuapé";

  const algs = $("#algoritmos");
  DADOS.algoritmos.forEach((a, i) => {
    const l = document.createElement("label");
    l.innerHTML = `<input type="radio" name="algoritmo" value="${esc(a.codigo)}" ${i === 0 ? "checked" : ""}> ${esc(a.rotulo)}`;
    algs.appendChild(l);
  });

  const bloq = $("#bloqueadas");
  for (const est of DADOS.estacoes) {
    const o = document.createElement("option");
    o.value = est;
    o.textContent = est;
    bloq.appendChild(o);
  }

  const indisp = $("#linhas-indisponiveis");
  for (const chave of Object.keys(DADOS.linhas)) {
    const l = document.createElement("label");
    l.innerHTML = `<input type="checkbox" value="${esc(chave)}">
      <span style="color:${corLinha(chave)};font-weight:600">${esc(nomeLinha(chave))}</span>`;
    indisp.appendChild(l);
  }

  const badge = $("#status-llm");
  if (DADOS.llm_configurado) {
    badge.textContent = "LLM: Groq configurado";
    badge.title = "O LLM interpreta o pedido e narra a rota; a rota vem da busca em grafo.";
  } else {
    badge.textContent = "LLM: sem chave";
    badge.classList.add("off");
    badge.title = "Defina GROQ_API_KEY no arquivo .env para usar a conversa em linguagem natural. O cálculo de rotas funciona normalmente.";
  }
}

function corpoDoFormulario() {
  return {
    origem: $("#origem").value,
    destino: $("#destino").value,
    algoritmo: document.querySelector("input[name=algoritmo]:checked").value,
    bloqueadas: Array.from($("#bloqueadas").selectedOptions).map((o) => o.value),
    linhas_indisponiveis: Array.from(
      document.querySelectorAll("#linhas-indisponiveis input:checked")).map((i) => i.value),
  };
}

// ---------- ações ----------
$("#btn-rota").addEventListener("click", async () => {
  const botao = $("#btn-rota");
  const corpo = corpoDoFormulario();
  botao.disabled = true;
  $("#resultado").innerHTML = '<p class="vazio">Calculando…</p>';
  try {
    const r = await api("/rota", corpo);
    mostrarResultado(r, corpo, null);
  } catch (e) {
    $("#resultado").innerHTML = `<div class="caixa">Erro: ${esc(e.message)}</div>`;
  } finally {
    botao.disabled = false;
  }
});

$("#btn-chat").addEventListener("click", async () => {
  const botao = $("#btn-chat");
  const msg = $("#msg-chat");
  botao.disabled = true;
  msg.className = "msg";
  msg.textContent = "Pensando…";
  try {
    const r = await api("/chat", { mensagem: $("#mensagem").value });
    if (!r.sucesso) {
      msg.className = "msg erro";
      msg.textContent = `❌ ${r.erro}`;
      $("#resultado").innerHTML = `<div class="caixa">${esc(r.erro)}</div>`;
      return;
    }
    msg.textContent = `Interpretado: ${r.interpretacao.origem} → ${r.interpretacao.destino} (${r.interpretacao.algoritmo.toUpperCase()})`;
    // espelha a interpretação nos campos, quando os nomes existem nas listas
    sincronizarCampo($("#origem"), r.interpretacao.origem, r.rota.origem);
    sincronizarCampo($("#destino"), r.interpretacao.destino, r.rota.destino);
    mostrarResultado(r.rota, corpoDoFormulario(), r.resposta);
  } catch (e) {
    msg.className = "msg erro";
    msg.textContent = `Erro: ${e.message}`;
  } finally {
    botao.disabled = false;
  }
});

function sincronizarCampo(select, texto, estacao) {
  for (const valor of [texto, estacao]) {
    if (valor && Array.from(select.options).some((o) => o.value === valor)) {
      select.value = valor;
      return;
    }
  }
}

$("#btn-limpar").addEventListener("click", () => {
  Array.from($("#bloqueadas").options).forEach((o) => (o.selected = false));
  document.querySelectorAll("#linhas-indisponiveis input").forEach((i) => (i.checked = false));
});

// ---------- resultado ----------
function mostrarResultado(r, cenario, narracao) {
  const alvo = $("#resultado");

  if (!r.sucesso) {
    let html = `<h3>Sem rota</h3><div class="caixa">🚫 ${esc(r.erro)}</div>`;
    if (cenario.bloqueadas.length || cenario.linhas_indisponiveis.length) {
      html += `<p class="texto">Cenário aplicado: ` +
        (cenario.bloqueadas.length ? `estações fechadas (${esc(cenario.bloqueadas.join(", "))}) ` : "") +
        (cenario.linhas_indisponiveis.length
          ? `linhas indisponíveis (${esc(cenario.linhas_indisponiveis.map(nomeLinha).join(", "))})` : "") +
        `.</p>`;
    }
    alvo.innerHTML = html;
    desenharMapa({ caminho: [], ordem_visita: [] }, cenario);
    return;
  }

  const paradas = r.caminho.length - 1;
  let html = `<h3>${esc(r.algoritmo.toUpperCase())}: ${esc(r.origem)} → ${esc(r.destino)}</h3>`;
  if (narracao) html += `<div class="narracao">🗣 ${esc(narracao)}</div>`;

  html += `<div class="tiles">
    <div class="tile"><div class="v">${paradas}</div><div class="k">paradas</div></div>
    <div class="tile"><div class="v">${r.total_baldeacoes}</div><div class="k">baldeações</div></div>
    <div class="tile"><div class="v">${r.ordem_visita.length}</div><div class="k">estações visitadas pela busca</div></div>
  </div>`;

  if (r.baldeacoes.length) {
    html += `<div class="bloco"><div class="k">Onde trocar de linha</div><ul>` +
      r.baldeacoes.map((b) => `<li>Em <b>${esc(b.estacao)}</b>: ` +
        `<span class="chip chip-linha" style="background:${corLinha(b.de)}">${esc(nomeLinha(b.de))}</span> → ` +
        `<span class="chip chip-linha" style="background:${corLinha(b.para)}">${esc(nomeLinha(b.para))}</span></li>`).join("") +
      `</ul></div>`;
  } else {
    html += `<div class="bloco"><div class="k">Baldeações</div>Nenhuma: a viagem inteira é na mesma linha.</div>`;
  }

  const setas = r.caminho.flatMap((e, i) => i
    ? [`<span class="chip seta">→</span>`, `<span class="chip">${esc(e)}</span>`]
    : [`<span class="chip">${esc(e)}</span>`]);
  html += `<div class="bloco"><div class="k">Caminho</div><div class="chips">${setas.join("")}</div></div>`;

  html += `<details><summary>Ordem de visita da busca (${r.ordem_visita.length} estações — o "esforço" do algoritmo)</summary>
    <div class="chips">${r.ordem_visita.map((e) => `<span class="chip">${esc(e)}</span>`).join("")}</div></details>`;

  alvo.innerHTML = html;
  desenharMapa(r, cenario);
}

// ---------- mapa das 3 linhas ----------
function desenharMapa(r, cenario) {
  const caminho = new Set(r.caminho || []);
  const visitadas = new Set(r.ordem_visita || []);
  const bloqueadas = new Set(cenario.bloqueadas || []);
  const indisponiveis = new Set(cenario.linhas_indisponiveis || []);
  const integracoes = new Set(DADOS.integracoes);
  let html = "";

  for (const [chave, estacoes] of Object.entries(DADOS.linhas)) {
    const cor = corLinha(chave);
    const off = indisponiveis.has(chave);
    html += `<div class="coluna" style="border-color:${cor};--cor:${cor}">
      <h4 style="color:${cor}" class="${off ? "off" : ""}">${esc(nomeLinha(chave))}${off ? " (indisponível)" : ""}</h4>`;
    for (const est of estacoes) {
      let classe = "";
      let marca = "";
      if (bloqueadas.has(est)) { classe = "bloqueada"; marca = "✖ fechada"; }
      else if ((est === r.origem || est === r.destino) && caminho.has(est)) {
        classe = "ponta"; marca = est === r.origem ? "origem" : "destino";
      } else if (caminho.has(est)) { classe = "rota"; marca = "rota"; }
      else if (visitadas.has(est)) { classe = "visitada"; marca = "visitada pela busca"; }
      html += `<div class="est ${classe}"><span class="pt"></span>
        <span class="nome">${esc(est)}${integracoes.has(est) ? ' <span class="int">⇄</span>' : ""}</span>
        <span class="marca">${marca}</span></div>`;
    }
    html += `</div>`;
  }

  html += `<div class="legenda">Legenda: <b>anel</b> = origem/destino · cor da linha = rota ·
    cinza = visitada pela busca (esforço) · preto ✖ = estação fechada · ⇄ = integração entre linhas</div>`;
  $("#mapa").innerHTML = html;
}

// ---------- inicialização ----------
(async function iniciar() {
  try {
    DADOS = await api("/dados");
    montarFormulario();
  } catch (e) {
    $("#resultado").innerHTML = `<div class="caixa">Não consegui falar com o servidor (${esc(e.message)}).
      Rode <code>uvicorn api:app --reload</code> na raiz do projeto e recarregue a página.</div>`;
  }
})();

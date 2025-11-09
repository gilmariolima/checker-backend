<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>📊 Conferência de Caixa</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
  <style>
    :root{
      --primary: #0a66c2;
      --ok: #1e9b55;
      --warn: #f59f00;
      --err: #ea4335;
      --bg: #f8fafc;
      --card: #fff;
      --muted: #6c757d;
    }

    body{background:var(--bg);font-family:Inter,Segoe UI,system-ui}
    header{background:linear-gradient(90deg,var(--primary),#004182);color:#fff;padding:22px;text-align:center;box-shadow:0 4px 16px rgba(0,0,0,0.1)}
    header h1{font-weight:700;font-size:1.6rem;margin:0}

    .container-lg{max-width:1000px}

    .panel{background:var(--card);border-radius:12px;padding:20px;box-shadow:0 6px 16px rgba(0,0,0,0.05)}
    .form-label{font-weight:600;color:#334155}
    .btn{border-radius:8px}

    .summary{display:flex;flex-wrap:wrap;gap:10px;margin-top:10px}
    .chip{padding:8px 12px;border-radius:999px;font-weight:600;display:inline-flex;align-items:center;gap:6px}
    .ok-chip{background:#dcfce7;color:#166534}
    .warn-chip{background:#fff7ed;color:#b45309}
    .err-chip{background:#fee2e2;color:#b91c1c}

    .agent-card{background:var(--card);border-radius:14px;padding:16px;margin-top:16px;box-shadow:0 4px 14px rgba(0,0,0,0.05);border-left:6px solid #e0ecff;transition:all 0.2s}
    .agent-header{display:flex;align-items:center;justify-content:space-between;cursor:pointer}
    .agent-name{font-weight:700;color:var(--primary)}
    .agent-meta{font-size:0.9rem;color:var(--muted)}
    .agent-content{margin-top:12px;display:none}
    .agent-content.show{display:block;animation:fadeIn 0.3s ease-in}

    @keyframes fadeIn{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:none}}

    .entry{background:#f1f5f9;border-radius:10px;padding:8px 12px;margin-bottom:8px;border-left:4px solid transparent}
    .ok{border-left-color:var(--ok)}
    .warn{border-left-color:var(--warn)}
    .err{border-left-color:var(--err)}

    .circle-wrap{position:relative;width:38px;height:38px;border-radius:50%;background:#e5edff;display:flex;align-items:center;justify-content:center;}
    .circle-inner{position:absolute;width:34px;height:34px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:600;color:var(--primary)}
    .progress-ring{transform:rotate(-90deg)}

    footer{text-align:center;color:#64748b;margin:30px 0;font-size:0.85rem}

    .btn + .btn { margin-left: 5px; }
  </style>
</head>
<body>
  <header style="backdrop-filter: blur(8px); background: rgba(10,102,194,0.8); color:#fff;text-align:center;padding:32px 10px;box-shadow:0 8px 20px rgba(0,0,0,0.15);border-bottom:2px solid rgba(255,255,255,0.2);border-radius:0 0 20px 20px;">
    <h1 style="font-weight:700;font-size:1.9rem;margin:0;"><i class="bi bi-graph-up-arrow"></i> Conferência de Caixa</h1>
  </header>



  <main class="container-lg mt-4">
    <div class="panel">
      <div class="mb-3">
        <label class="form-label">Arquivo PDF (C6 ou BB)</label>
        <input type="file" id="pdfFile" accept=".pdf" class="form-control">
      </div>
      <div class="mb-3">
        <label class="form-label">Planilhas Excel (.xlsx)</label>
        <input type="file" id="excelFile" accept=".xlsx" multiple class="form-control">
      </div>
      <div class="mb-3">
        <label class="form-label">Data da conferência (opcional)</label>
        <input type="date" id="dataFiltro" class="form-control">
      </div>

      <div class="d-flex flex-wrap gap-2 mb-3">
        <button class="btn btn-primary" id="btnConferir"><i class="bi bi-search"></i> Conferir</button>
        <button class="btn btn-outline-secondary" id="btnLimpar"><i class="bi bi-brush"></i> Limpar</button>
        <button class="btn btn-outline-danger" id="btnExport"><i class="bi bi-filetype-pdf"></i> Exportar PDF</button>
      </div>

      <div class="summary">
        <div class="chip ok-chip">✅ Conferidos: <strong id="totalConferidos">0</strong></div>
        <div class="chip warn-chip">⚠️ Falta PDF: <strong id="totalFaltaPdf">0</strong></div>
        <div class="chip err-chip">❌ Falta Excel: <strong id="totalFaltaExcel">0</strong></div>
      </div>

      <div id="progressArea" class="text-center mt-4" style="display:none;">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="text-muted mt-2">Processando arquivos...</p>
      </div>

      <div id="resultado" class="mt-4"></div>
    </div>
  </main>

  <footer>© 2025 Gilmario Lima</footer>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
  <script>
  function toggleAgent(id){document.getElementById(id).classList.toggle('show');}
  function formatCurrency(v){try{return(v||0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}catch{return'R$ 0,00'}}

  let bancoDetectado = '';

  document.getElementById('btnConferir').addEventListener('click',async()=>{
    const pdf=document.getElementById('pdfFile').files[0];
    const excels=document.getElementById('excelFile').files;
    const dataFiltro=document.getElementById('dataFiltro').value;
    if(!pdf||excels.length===0)return alert('Envie o PDF e pelo menos uma planilha Excel!');

    const resEl=document.getElementById('resultado');resEl.innerHTML='';
    document.getElementById('progressArea').style.display='block';

    const fd=new FormData();fd.append('pdf',pdf);for(let i=0;i<excels.length;i++)fd.append('excels',excels[i]);fd.append('data',dataFiltro);

    try{
      const resp=await fetch('http://127.0.0.1:8000/conferir_caixa',{method:'POST',body:fd});
      const dados=await resp.json();
      document.getElementById('progressArea').style.display='none';

      if(dados.erro){resEl.innerHTML=`<div class='alert alert-danger'>${dados.erro}</div>`;return;}

      bancoDetectado = dados.banco?.toUpperCase() || 'DESCONHECIDO';

      const conf=dados.conferidos||[],fPdf=dados.faltando_no_pdf||[],fExcel=dados.faltando_no_excel||[];
      document.getElementById('totalConferidos').textContent=conf.length;
      document.getElementById('totalFaltaPdf').textContent=fPdf.length;
      document.getElementById('totalFaltaExcel').textContent=fExcel.length;

      const agentes={};
      const add=(arr,tipo)=>arr.forEach(x=>{const ag=x.agente||'Sem Agente';if(!agentes[ag])agentes[ag]={conferidos:[],faltando_pdf:[],faltando_excel:[]};agentes[ag][tipo].push(x);});
      add(conf,'conferidos');add(fPdf,'faltando_pdf');add(fExcel,'faltando_excel');

      let html='';
      Object.entries(agentes).forEach(([agente,d])=>{
        const id=agente.replace(/\s+/g,'_');
        const total=d.conferidos.length+d.faltando_pdf.length+d.faltando_excel.length;
        const perc=total?Math.round((d.conferidos.length/total)*100):0;

        const circle=`<div class='circle-wrap'>
          <svg class='progress-ring' width='38' height='38'>
            <circle stroke='#e5e7eb' stroke-width='4' fill='transparent' r='16' cx='19' cy='19'></circle>
            <circle stroke='${perc==100?'#16a34a':'#0a66c2'}' stroke-width='4' fill='transparent' r='16' cx='19' cy='19' stroke-dasharray='${2*Math.PI*16}' stroke-dashoffset='${(1-perc/100)*2*Math.PI*16}'></circle>
          </svg>
          <div class='circle-inner'>${perc}%</div>
        </div>`;

        html+=`<div class='agent-card'>
          <div class='agent-header' onclick='toggleAgent("${id}")'>
            <div><span class='agent-name'><i class='bi bi-person-circle'></i> ${agente}</span><br><span class='agent-meta'>Conferidos: ${d.conferidos.length} • Falta PDF: ${d.faltando_pdf.length} • Falta Excel: ${d.faltando_excel.length}</span></div>
            ${circle}
          </div>
          <div class='agent-content' id='${id}'>
            <div class='mt-3'>

              <!-- ✅ CONFERIDOS -->
              <div class='fw-bold text-success mb-2'>✅ Conferidos (${d.conferidos.length})</div>
              ${d.conferidos.map(x => `
                <div class='entry ok'>
                  <div class="fw-bold text-success mb-1">${x.nome_excel || x.nome}</div>
                  <div class="mt-1 ps-1">
                    <div>
                      <i class="bi bi-file-earmark-excel text-success me-1"></i>
                      <small>
                        <strong>Excel:</strong>
                        <span class="text-dark">${x.nome_excel || '-'}</span> —
                        <span class="valor">${formatCurrency(x.valor_excel)}</span> •
                        ${x.hora_excel || '(sem hora)'}
                      </small>
                    </div>
                    <div>
                      <i class="bi bi-file-earmark-pdf text-danger me-1"></i>
                      <small>
                        <strong>PDF:</strong>
                        <span class="text-dark">${x.nome_pdf || '-'}</span> —
                        <span class="valor">${formatCurrency(x.valor_pdf)}</span> •
                        ${x.hora_pdf || '(sem hora)'}
                      </small>
                    </div>
                  </div>
                </div>
              `).join('')}


              <!-- ⚠️ FALTANDO NO PDF -->
              <div class='fw-bold text-warning mt-3 mb-2'>⚠️ Faltando no PDF (${d.faltando_pdf.length})</div>
              ${d.faltando_pdf.map(x => `
                <div class='entry warn'>
                  <strong>${x.nome}</strong>
                  <div class="mt-1">
                    <div><i class="bi bi-file-earmark-excel text-success"></i>
                      <small><strong>Excel:</strong> ${formatCurrency(x.valor_excel ?? x.valor)} • ${x.hora || '(sem hora)'}</small>
                    </div>
                    <div><i class="bi bi-file-earmark-pdf text-danger"></i>
                      <small><strong>PDF:</strong> <em>não encontrado</em></small>
                    </div>
                  </div>
                  <div class="text-muted mt-1"><small>💬 ${x.motivo || 'Sem motivo registrado.'}</small></div>
                </div>
              `).join('')}

              <!-- ❌ FALTANDO NO EXCEL -->
              <div class='fw-bold text-danger mt-3 mb-2'>❌ Faltando no Excel (${d.faltando_excel.length})</div>
              ${d.faltando_excel.map(x => `
                <div class='entry err'>
                  <strong>${x.nome}</strong>
                  <div class="mt-1">
                    <div><i class="bi bi-file-earmark-excel text-success"></i>
                      <small><strong>Excel:</strong> <em>não encontrado</em></small>
                    </div>
                    <div><i class="bi bi-file-earmark-pdf text-danger"></i>
                      <small><strong>PDF:</strong> ${formatCurrency(x.valor)} • ${x.hora || '(sem hora)'}</small>
                    </div>
                  </div>
                </div>
              `).join('')}

            </div>
          </div>

        </div>`;
      });

      resEl.innerHTML=html;

    }catch(e){
      document.getElementById('progressArea').style.display='none';
      resEl.innerHTML=`<div class='alert alert-danger'>Erro: ${e.message}</div>`;
    }
  });

  document.getElementById('btnLimpar').addEventListener('click',()=>{
    document.getElementById('pdfFile').value='';document.getElementById('excelFile').value='';document.getElementById('dataFiltro').value='';document.getElementById('resultado').innerHTML='';document.getElementById('totalConferidos').textContent='0';document.getElementById('totalFaltaPdf').textContent='0';document.getElementById('totalFaltaExcel').textContent='0';
  });

  document.getElementById('btnExport').addEventListener('click',()=>{
    const resultado=document.getElementById('resultado');
    if(!resultado.innerHTML)return alert('Nada para exportar');

    const totalC=document.getElementById('totalConferidos').textContent;
    const totalP=document.getElementById('totalFaltaPdf').textContent;
    const totalE=document.getElementById('totalFaltaExcel').textContent;
    const hoje=new Date();
    const dataStr=hoje.toLocaleDateString('pt-BR');
    const nomeArquivo=`ConferenciaCaixa_${bancoDetectado||'DESCONHECIDO'}_${hoje.toISOString().split('T')[0]}.pdf`;

    const cabecalho=`<div style='text-align:center;margin-bottom:20px;'>
      <h2 style='color:#0a66c2;margin-bottom:4px;'>📊 Conferência de Caixa</h2>
      <p style='margin:0;font-size:13px;color:#444;'>Banco: <strong>${bancoDetectado}</strong> • Data: <strong>${dataStr}</strong></p>
      <p style='margin:4px 0;font-size:13px;color:#555;'>Conferidos: ${totalC} • Falta PDF: ${totalP} • Falta Excel: ${totalE}</p>
      <hr style='border:none;border-top:1px solid #ccc;margin:10px 0;'>
    </div>`;

    const conteudoPDF=cabecalho+resultado.innerHTML;

    const opt={margin:0.5,filename:nomeArquivo,html2canvas:{scale:2},jsPDF:{unit:'in',format:'a4',orientation:'portrait'}};
    html2pdf().set(opt).from(conteudoPDF).save();
  });
  </script>
</body>
</html>

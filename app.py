import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from datetime import datetime

# =========================================================
# CONFIGURAÇÃO FIXA DA CHAVE API GEMINI
# Cole sua chave dentro das aspas abaixo para não precisar digitar no celular
GEMINI_API_KEY = "SUA_CHAVE_GEMINI_AQUI"
# =========================================================

# FUNÇÃO PARA GERAR RELATÓRIO HTML
def gerar_relatorio_html(df, df_daily, prod_total, perca_total, eficiencia, taxa_perca, tempo_parado):
    """Gera relatório em HTML para impressão"""
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Relatório de Produção</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                margin: 20px;
            }}
            .header {{
                text-align: center;
                border-bottom: 3px solid #0284C7;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            h1 {{
                color: #0284C7;
                margin: 0;
            }}
            .data-relatorio {{
                text-align: center;
                color: #666;
                font-size: 12px;
            }}
            .metricas {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }}
            .metrica-card {{
                border: 1px solid #ddd;
                padding: 15px;
                border-radius: 5px;
                text-align: center;
                background: #f9f9f9;
            }}
            .metrica-titulo {{
                font-size: 12px;
                color: #666;
                text-transform: uppercase;
                margin-bottom: 10px;
            }}
            .metrica-valor {{
                font-size: 24px;
                font-weight: bold;
                color: #0284C7;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }}
            table th {{
                background: #0284C7;
                color: white;
                padding: 10px;
                text-align: left;
                font-size: 12px;
            }}
            table td {{
                border-bottom: 1px solid #ddd;
                padding: 8px;
                font-size: 12px;
            }}
            table tr:nth-child(even) {{
                background: #f9f9f9;
            }}
            .secao-titulo {{
                font-size: 16px;
                font-weight: bold;
                color: #0284C7;
                margin-top: 30px;
                margin-bottom: 15px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 10px;
            }}
            @media print {{
                body {{
                    margin: 0;
                    padding: 10px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>⚡ GESTÃO DE PRODUÇÃO</h1>
            <h2>Relatório de Produção</h2>
            <div class="data-relatorio">Gerado em {agora}</div>
        </div>

        <div class="metricas">
            <div class="metrica-card">
                <div class="metrica-titulo">Produção Total</div>
                <div class="metrica-valor">{prod_total:,.0f} m</div>
            </div>
            <div class="metrica-card">
                <div class="metrica-titulo">Perca Total</div>
                <div class="metrica-valor">{perca_total:,.0f} m</div>
            </div>
            <div class="metrica-card">
                <div class="metrica-titulo">Eficiência Geral</div>
                <div class="metrica-valor" style="color: #10B981;">{eficiencia:.1f}%</div>
            </div>
            <div class="metrica-card">
                <div class="metrica-titulo">Taxa de Perca</div>
                <div class="metrica-valor" style="color: #F59E0B;">{taxa_perca:.1f}%</div>
            </div>
        </div>

        <div class="secao-titulo">📊 Produção Diária</div>
        <table>
            <tr>
                <th>Data</th>
                <th>Produção Total (m)</th>
            </tr>
    """
    
    for _, row in df_daily.iterrows():
        data_fmt = pd.to_datetime(row['Data']).strftime("%d/%m/%Y")
        html_content += f"""
            <tr>
                <td>{data_fmt}</td>
                <td>{row['Total_Producao_Dia']:,.0f}</td>
            </tr>
        """
    
    html_content += """
        </table>

        <div class="secao-titulo">📋 Histórico Completo de Lançamentos</div>
        <table>
            <tr>
                <th>Data</th>
                <th>Turno</th>
                <th>Operador</th>
                <th>Material</th>
                <th>Hora Início</th>
                <th>Hora Término</th>
                <th>Produção (m)</th>
                <th>Perca (m)</th>
                <th>Tempo Parado (min)</th>
                <th>Motivo</th>
            </tr>
    """
    
    for _, row in df.iterrows():
        html_content += f"""
            <tr>
                <td>{row['Data']}</td>
                <td>{row['Turno']}</td>
                <td>{row['Operador']}</td>
                <td>{row['Material']}</td>
                <td>{row['Hora_Inicio']}</td>
                <td>{row['Hora_Final']}</td>
                <td>{row['Producao_m']:,.0f}</td>
                <td>{row['Perca_m']:,.0f}</td>
                <td>{row['Tempo_Parado_min']:.0f}</td>
                <td>{row['Motivo_Parada']}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    return html_content

st.set_page_config(
    page_title="GESTÃO DE PRODUÇÃO - Gestão Industrial Advanced", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização Dark OLED Limpa e Textos Claros
st.markdown("""
    <style>
    .stApp {
        background-color: #0B0F17;
        color: #F8FAFC;
    }
    .header-box {
        background: #111827;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #1E293B;
        margin-bottom: 20px;
    }
    .header-box h1 { color: #38BDF8 !important; font-size: 24px !important; margin: 0 !important; }
    .header-box p { color: #94A3B8 !important; margin: 4px 0 0 0 !important; font-size: 13px !important; }

    /* Estilo dos Rótulos do Formulário */
    label, .stWidgetLabel p {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* Container de Cards de Métricas */
    .metric-card {
        background: #111827;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .metric-title { color: #94A3B8; font-size: 12px; font-weight: 600; text-transform: uppercase; }
    .metric-value { color: #F8FAFC; font-size: 26px; font-weight: 800; margin: 4px 0; }
    
    div[data-testid="stForm"] {
        background: #111827;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 20px;
    }
    .stButton>button, div[data-testid="stForm"] button {
        background: #0284C7 !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# TOPO
st.markdown("""
    <div class="header-box">
        <h1>⚡ GESTÃO DE PRODUÇÃO - PAINEL INDUSTRIAL ADVANCED</h1>
        <p>Acompanhamento de Produção, Perda por Operador e Material, Eficiência e Paradas</p>
    </div>
""", unsafe_allow_html=True)

# Configura a chave do Gemini de forma automática
if GEMINI_API_KEY and GEMINI_API_KEY != "SUA_CHAVE_GEMINI_AQUI":
    genai.configure(api_key=GEMINI_API_KEY)

# BANCO DE DADOS EM MEMÓRIA
if "dados_producao" not in st.session_state:
    st.session_state.dados_producao = pd.DataFrame(columns=[
        "Numero_OP", "Data", "Turno", "Operador", "Material", "Hora_Inicio", "Hora_Final", "Producao_m", "Perca_m", "Tempo_Parado_min", "Motivo_Parada"
    ])

if "ordens_producao" not in st.session_state:
    st.session_state.ordens_producao = pd.DataFrame(columns=[
        "Numero_OP", "Data_Criacao", "Material", "Quantidade_Programada_m", "Status", "Observacoes"
    ])

aba1, aba2, aba3, aba4 = st.tabs(["📝 Registrar Turno", "📊 Dashboard de Produção", "🤖 Copiloto IA", "📋 Ordens de Produção"])

# --- ABA 1: REGISTRAR TURNO ---
with aba1:
    st.subheader("Novo Apontamento de Produção")
    with st.form("form_producao", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            data = st.date_input("🗓️ Data do Turno")
            turno = st.selectbox("⏱️ Turno", ["Manhã", "Tarde", "Noite", "Turno 1", "Turno 2"])
            operador = st.text_input("👤 Nome do Operador", placeholder="Ex: André / Samuel")
        with c2:
            numero_op = st.text_input("📋 Número da Ordem de Produção", placeholder="Ex: OP-2024-001")
            material = st.text_input("📦 Nome / Tipo do Material", placeholder="Ex: Filme PP 50 micras / Lixa 120")
            hora_inicio = st.time_input("🕐 Hora de Início", value=None)
            hora_final = st.time_input("🕑 Hora de Término", value=None)
        with c3:
            producao = st.number_input("📏 Produção Realizada (m)", min_value=0.0, step=10.0)
            perca = st.number_input("⚠️ Perca / Refugo (m)", min_value=0.0, step=1.0)
            tempo_parado = st.number_input("🛑 Tempo Parado (min)", min_value=0.0, step=5.0)
            motivo_parada = st.text_area("📝 Motivo da Parada", placeholder="Ex: Manutenção, troca de bobina...")

        submitted = st.form_submit_button("🚀 Salvar Lançamento do Turno", use_container_width=True)
        
        if submitted:
            if not operador or not material or not numero_op:
                st.error("Por favor, preencha o número da OP, nome do operador e nome do material.")
            elif hora_inicio is None or hora_final is None:
                st.error("Por favor, preencha os horários de início e término.")
            else:
                novo_registro = pd.DataFrame([{
                    "Numero_OP": numero_op.strip().upper(),
                    "Data": str(data),
                    "Turno": turno,
                    "Operador": operador.strip().title(),
                    "Material": material.strip().upper(),
                    "Hora_Inicio": str(hora_inicio),
                    "Hora_Final": str(hora_final),
                    "Producao_m": producao,
                    "Perca_m": perca,
                    "Tempo_Parado_min": tempo_parado,
                    "Motivo_Parada": motivo_parada if motivo_parada else "Sem Paradas"
                }])
                st.session_state.dados_producao = pd.concat([st.session_state.dados_producao, novo_registro], ignore_index=True)
                st.success("✅ Lançamento salvo com sucesso!")

# --- ABA 2: DASHBOARD COMPLETO ---
with aba2:
    df = st.session_state.dados_producao
    
    if df.empty:
        st.info("Nenhum registro encontrado. Faça os lançamentos na aba 'Registrar Turno'.")
    else:
        # TOTAL DA PRODUÇÃO DIÁRIA DA FÁBRICA
        df_daily = df.groupby("Data", as_index=False).agg({"Producao_m": "sum"}).rename(columns={"Producao_m": "Total_Producao_Dia"})
        df_daily["Data"] = pd.to_datetime(df_daily["Data"])
        df_daily = df_daily.sort_values("Data").reset_index(drop=True)

        datas_disponiveis = sorted(df["Data"].unique())
        data_selecionada = st.selectbox("📅 Selecionar data para ver o total diário", options=datas_disponiveis, index=len(datas_disponiveis)-1)
        producao_total_dia = float(df.loc[df["Data"] == data_selecionada, "Producao_m"].sum())

        # MÉTRICAS GERAIS DA FÁBRICA
        prod_total_fabrica = df["Producao_m"].sum()
        perca_total_fabrica = df["Perca_m"].sum()
        tempo_parado_total = df["Tempo_Parado_min"].sum()
        materia_total = prod_total_fabrica + perca_total_fabrica
        
        eficiencia_fabrica = (prod_total_fabrica / materia_total * 100) if materia_total > 0 else 0
        taxa_perca_fabrica = (perca_total_fabrica / materia_total * 100) if materia_total > 0 else 0

        st.markdown("### 🏭 Indicadores Gerais")
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f'<div class="metric-card"><div class="metric-title">Produção Total</div><div class="metric-value">{prod_total_fabrica:,.0f} m</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card"><div class="metric-title">Produção do Dia Selecionado</div><div class="metric-value" style="color:#22C55E">{producao_total_dia:,.0f} m</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card"><div class="metric-title">Eficiência Geral</div><div class="metric-value" style="color:#10B981">{eficiencia_fabrica:.1f}%</div></div>', unsafe_allow_html=True)
        m4.markdown(f'<div class="metric-card"><div class="metric-title">Tempo Total Parado</div><div class="metric-value" style="color:#F59E0B">{tempo_parado_total:.0f} min</div></div>', unsafe_allow_html=True)

        st.caption(f"📌 Total da produção em {data_selecionada}: {producao_total_dia:,.0f} metros")
        st.divider()

        # CONSOLIDAÇÃO POR OPERADOR
        op_df = df.groupby("Operador").agg({
            "Producao_m": "sum",
            "Perca_m": "sum",
            "Tempo_Parado_min": "sum"
        }).reset_index()

        op_df["Materia_Total"] = op_df["Producao_m"] + op_df["Perca_m"]
        op_df["Taxa_Perca_%"] = (op_df["Perca_m"] / op_df["Materia_Total"] * 100).fillna(0)
        op_df["Eficiencia_%"] = (op_df["Producao_m"] / op_df["Materia_Total"] * 100).fillna(0)

        # AVALIAÇÃO E ALERTAS DE OPERADORES
        st.markdown("### 🏆 Avaliação e Alertas de Operadores")
        
        melhor_op = op_df.sort_values(by="Taxa_Perca_%", ascending=True).iloc[0]
        st.success(f"🎉 **PARABÉNS AO OPERADOR DESTAQUE:** **{melhor_op['Operador']}** obteve o menor índice de perca ({melhor_op['Taxa_Perca_%']:.2f}%) com produção de {melhor_op['Producao_m']:,.0f}m!")

        ops_acima_media = op_df[op_df["Taxa_Perca_%"] > taxa_perca_fabrica]
        for _, row in ops_acima_media.iterrows():
            st.error(f"🚨 **ALERTA DE ATENÇÃO:** O operador **{row['Operador']}** está com taxa de perca em **{row['Taxa_Perca_%']:.2f}%** (acima da média geral de {taxa_perca_fabrica:.2f}%).")

        st.divider()

        # CONSOLIDAÇÃO POR MATERIAL
        mat_df = df.groupby("Material").agg({
            "Producao_m": "sum",
            "Perca_m": "sum"
        }).reset_index()
        mat_df["Materia_Total"] = mat_df["Producao_m"] + mat_df["Perca_m"]
        mat_df["Taxa_Perca_%"] = (mat_df["Perca_m"] / mat_df["Materia_Total"] * 100).fillna(0)

        # GRÁFICOS
        g1, g2 = st.columns(2)
        with g1:
            fig_prod_dia = px.line(
                df_daily,
                x="Data",
                y="Total_Producao_Dia",
                markers=True,
                title="<b>Total Diário da Produção da Fábrica (m)</b>",
                template="plotly_dark"
            )
            fig_prod_dia.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_prod_dia, use_container_width=True)

        with g2:
            fig_op_prod = px.bar(
                df, x="Operador", y="Producao_m", color="Material",
                title="<b>Produção por Operador e Material (m)</b>",
                template="plotly_dark",
                barmode="stack"
            )
            fig_op_prod.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_op_prod, use_container_width=True)

        st.markdown("### 📈 Produção Diário por Data")
        st.dataframe(df_daily.assign(Data=df_daily["Data"].dt.strftime("%d/%m/%Y")).rename(columns={"Total_Producao_Dia": "Produção Total (m)"}), use_container_width=True)

        mat_g1, mat_g2 = st.columns(2)
        with mat_g1:
            fig_mat_perca = px.bar(
                mat_df, x="Material", y="Taxa_Perca_%",
                title="<b>Taxa de Perca (%) por Tipo de Material</b>",
                template="plotly_dark",
                color="Taxa_Perca_%",
                color_continuous_scale="Reds"
            )
            fig_mat_perca.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_mat_perca, use_container_width=True)

        with mat_g2:
            fig_total_prod = px.bar(
                df_daily,
                x="Data",
                y="Total_Producao_Dia",
                title="<b>Produção Total por Dia</b>",
                template="plotly_dark",
                color="Total_Producao_Dia",
                color_continuous_scale="Viridis"
            )
            fig_total_prod.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_total_prod, use_container_width=True)

        # TABELA DETALHADA COM MATERIAIS
        st.markdown("### 📋 Histórico Completo de Lançamentos")
        st.dataframe(
            df[["Data", "Turno", "Operador", "Material", "Hora_Inicio", "Hora_Final", "Producao_m", "Perca_m", "Tempo_Parado_min", "Motivo_Parada"]].style.format({
                "Producao_m": "{:,.0f} m",
                "Perca_m": "{:,.0f} m",
                "Tempo_Parado_min": "{:.0f} min"
            }), 
            use_container_width=True
        )

        # SEÇÃO DE IMPRESSÃO DE RELATÓRIO
        st.divider()
        st.markdown("### 🖨️ Exportar e Imprimir Relatório")
        
        col_print1, col_print2 = st.columns(2)
        
        with col_print1:
            if st.button("🖨️ Imprimir Relatório", use_container_width=True):
                html_relatorio = gerar_relatorio_html(df, df_daily, prod_total_fabrica, perca_total_fabrica, eficiencia_fabrica, taxa_perca_fabrica, tempo_parado_total)
                st.markdown(html_relatorio, unsafe_allow_html=True)
                st.info("✅ Clique em CTRL+P ou ⌘+P para imprimir o relatório acima.")
        
        with col_print2:
            # EXPORTAR COMO CSV
            csv_data = df[["Data", "Turno", "Operador", "Material", "Hora_Inicio", "Hora_Final", "Producao_m", "Perca_m", "Tempo_Parado_min", "Motivo_Parada"]].to_csv(index=False)
            st.download_button(
                label="📥 Baixar Dados (CSV)",
                data=csv_data,
                file_name=f"relatorio_producao_{datetime.now().strftime('%d_%m_%Y_%H_%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# --- ABA 3: COPILOTO IA ---
with aba3:
    st.subheader("🤖 Consultar Copiloto de Inteligência Industrial")
    pergunta_usuario = st.text_input("Faça uma pergunta sobre materiais, operadores ou gargalos:", placeholder="Ex: Qual material deu mais perca com o operador Samuel?")
    
    if st.button("🔍 Analisar com IA", use_container_width=True):
        if not GEMINI_API_KEY or GEMINI_API_KEY == "SUA_CHAVE_GEMINI_AQUI":
            st.warning("⚠️ Substitua 'SUA_CHAVE_GEMINI_AQUI' na linha 14 do código no computador antes de consultar.")
        elif st.session_state.dados_producao.empty:
            st.warning("Cadastre ao menos um registro antes de consultar a IA.")
        else:
            with st.spinner("O Copiloto está analisando a relação entre Operadores e Materiais..."):
                try:
                    historico_texto = st.session_state.dados_producao.to_csv(index=False)
                    prompt_sistema = f"""
                    Você é um Gerente de Operações Industriais especialista em otimização de linhas de produção.
                    Analise os dados cadastrados:
                    {historico_texto}
                    
                    Pergunta do Usuário: {pergunta_usuario}
                    
                    Forneça um parecer sucinto e prático com:
                    1. Relação entre Operadores e Materiais rodados.
                    2. Identificação de materiais com alta taxa de perca.
                    3. Recomendações operacionais imediatas.
                    """
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    response = model.generate_content(prompt_sistema)
                    
                    st.markdown("### 💡 Parecer da IA:")
                    st.info(response.text)
                except Exception as e:
                    st.error(f"Erro ao consultar a IA: {e}")  
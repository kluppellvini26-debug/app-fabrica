# GESTÃO DE PRODUÇÃO - AI Agent Guidelines

## Project Overview

**GESTÃO DE PRODUÇÃO** is an industrial production management system built with Streamlit. It tracks manufacturing metrics including production output, material waste, operator efficiency, and machine downtime.

- **Language**: Portuguese (Brazilian Portuguese throughout UI and comments)
- **Type**: Web application (Streamlit)
- **Purpose**: Real-time factory floor monitoring and AI-assisted analytics

## Tech Stack

- **Framework**: Streamlit (web UI)
- **Data**: Pandas (DataFrames)
- **Visualization**: Plotly Express (interactive charts)
- **AI**: Google Generative AI (Gemini API)
- **Design**: Custom Streamlit CSS for dark OLED theme

## Running the Application

```bash
# Prerequisites: Install dependencies
pip install streamlit pandas plotly google-generativeai

# Run the app
streamlit run app.py
```

The app defaults to port `8501` and opens in your browser at `http://localhost:8501`.

## Project Structure

- `app.py` - Main application file (currently monolithic)
- `README.md` - Basic project documentation

## Architecture & Key Conventions

### Application Structure (Three Tabs)

1. **Aba 1 - "📝 Registrar Turno" (Register Shift)**
   - Form for recording production data
   - Fields: Date, Shift, Operator, Material, Production (m), Waste (m), Downtime (min), Downtime Reason
   - Stores data in `st.session_state.dados_producao`

2. **Aba 2 - "📊 Dashboard da Fábrica" (Factory Dashboard)**
   - Analytics and visualizations
   - Displays KPIs and charts using Plotly
   - Connects to production data from session state

3. **Aba 3 - "🤖 Copiloto IA" (AI Copilot)**
   - Gemini AI integration for insights and analysis
   - Uses `genai.configure(api_key=GEMINI_API_KEY)`

### Data Model

Production data is stored as a Pandas DataFrame in `st.session_state.dados_producao`:
- `Data` - Date of production
- `Turno` - Shift (Manhã/Tarde/Noite or Turno 1/2)
- `Operador` - Operator name
- `Material` - Material type/description
- `Producao_m` - Production in meters
- `Perca_m` - Waste/loss in meters
- `Tempo_Parado_min` - Downtime in minutes
- `Motivo_Parada` - Reason for downtime

### Styling

- **Theme**: Dark OLED (`#0B0F17` background, light gray text)
- **Colors**: Cyan accents (`#38BDF8` for headers, `#0284C7` for buttons)
- **Layout**: Wide mode with collapsed sidebar
- **Responsiveness**: Uses Streamlit columns for responsive grids

### Configuration

- **Gemini API Key**: Set in `GEMINI_API_KEY` variable at the top of `app.py`
  - Current: Placeholder `"SUA_CHAVE_GEMINI_AQUI"`
  - Should be populated with actual key for AI features to work

## Common Development Tasks

### Adding a New Field to Production Data
1. Add column name to the DataFrame initialization in `if "dados_producao" not in st.session_state`
2. Add corresponding input widget in the form on Aba 1
3. Update dashboard visualizations to use new field if relevant

### Extending the AI Copilot
1. Prepare data summary from `st.session_state.dados_producao`
2. Use `genai.GenerativeModel()` to create prompts
3. Display responses in Aba 3 using Streamlit widgets

### Styling Changes
1. Modify CSS in the `st.markdown()` call near the top
2. Use Streamlit's `st_emotion` classes or custom HTML/CSS
3. Test in browser with `streamlit run app.py`

## Known Constraints

- **Session State**: Data is stored in memory only (lost on app reload)
  - For persistence, add database integration (SQLite, PostgreSQL, etc.)
- **API Key Management**: Currently hardcoded in app
  - Should use `st.secrets` or environment variables for production
- **Monolithic Structure**: All code in single file
  - Consider splitting into modules as complexity grows

## Debugging Tips

- Use `st.write(st.session_state)` to inspect session state
- Check Gemini API connectivity: `genai.configure()` requires valid key
- Browser console (F12) shows Streamlit client errors
- Terminal shows Streamlit server logs and Python errors
- Clear cache with `streamlit cache clear` if seeing stale data

## Useful Streamlit Commands

```bash
# Run with specific config
streamlit run app.py --logger.level=debug

# Check installed version
streamlit --version

# View Streamlit docs
streamlit help
```

## Next Steps for Enhancement

- [ ] Add persistent database backend
- [ ] Implement user authentication
- [ ] Extract components into separate modules
- [ ] Add data export functionality (CSV/PDF)
- [ ] Enhance AI Copilot with multi-turn conversations
- [ ] Add performance metrics/alerts

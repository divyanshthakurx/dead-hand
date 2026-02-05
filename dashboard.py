import streamlit as st
import json
import os
from PIL import Image

st.set_page_config(layout="wide", page_title="Dead Hand: DPDP Enforcer")
st.title("⚖️ Dead Hand: DPDP Enforcer Console")

runs_dir = os.path.join("data", "runs")

if os.path.exists(runs_dir):
    run_folders = sorted(os.listdir(runs_dir), reverse=True)
    selected_run = st.sidebar.selectbox("Select Mission", run_folders)
else:
    st.error("No runs found.")
    selected_run = None

if selected_run:
    run_path = os.path.join(runs_dir, selected_run)
    report_path = os.path.join(run_path, "report.json")
    
    if os.path.exists(report_path):
        # Refresh Data
        if st.sidebar.button("Refresh Data"):
            st.rerun()
            
        with open(report_path, "r") as f:
            data = json.load(f)
            
        st.header(f"Mission: {data.get('prompt', 'Unknown')}")
        st.caption(f"ID: {data.get('id')} | Started: {data.get('start_time')}")
        
        # --- FIX 1: Handle missing keys safely ---
        steps = data.get('steps', [])
        
        # Calculate DPDP Metrics
        total_checks = len(steps)
        violations = [s for s in steps if s.get('analysis', {}).get('verdict') == "Violation"]
        violation_count = len(violations)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🔍 Screen Checks", total_checks)
        col2.metric("🛡️ Interventions Triggered", violation_count)
        col3.metric("⚖️ DPDP Compliance Rate", f"{((total_checks - violation_count)/total_checks * 100):.1f}%" if total_checks > 0 else "100%")

        st.divider()

        for step in steps:
            with st.container():
                st.subheader(f"Step {step.get('step')}")
                
                c1, c2 = st.columns([1, 2])
                
                with c1:
                    img_path = step.get('screenshot')
                    if img_path and os.path.exists(img_path):
                        image = Image.open(img_path)
                        st.image(image, caption="Screen Capture", use_container_width=True)
                    else:
                        st.warning("Screenshot not found")
                
                with c2:
                    analysis = step.get('analysis', {})
                    
                    verdict = analysis.get('verdict', 'Unknown')
                    section6 = analysis.get('section_6_status', 'N/A')
                    
                    if verdict == "Violation":
                         st.error(f"### 🛑 BLOCKED: {analysis.get('actor', 'Unknown App')}")
                    elif verdict == "Safe":
                         st.success(f"### ✅ ALLOWED: {analysis.get('actor', 'Unknown App')}")
                    else:
                         st.info(f"### ℹ️ Status: {verdict}")

                    st.markdown(f"**Request:** `{analysis.get('request', 'None')}`")
                    st.markdown(f"**Section 6 Status:** {section6}")
                    
                    st.markdown("---")
                    st.markdown(f"**🧠 Legal Logic:**")
                    st.caption(analysis.get('necessity_check', 'No reasoning provided.'))

    else:
        st.info("Waiting for data... (Run the watcher!)")
import streamlit as st
import json
import os
from PIL import Image

st.set_page_config(layout="wide", page_title="Dead Hand Dashboard")
st.title("💀 Dead Hand: Dark Pattern Detective")

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
        scores = []
        for s in steps:
            # Check for both keys just in case
            analysis = s.get('analysis', {})
            val = analysis.get('score', analysis.get('darkness_score', 0))
            scores.append(val)
            
        avg_score = sum(scores) / len(scores) if scores else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Steps", len(steps))
        col2.metric("Avg Darkness Score", f"{avg_score:.1f}/10")
        col3.metric("High Risk Screens", sum(1 for s in scores if s > 7))

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
                    
                    score = analysis.get('score', 0)
                    
                    color = "green" if score < 4 else "orange" if score < 7 else "red"
                    st.markdown(f"### Darkness Score: :{color}[{score}/10]")
                    st.markdown(f"**Verdict:** {analysis.get('verdict', 'N/A')}")
                    
                    st.markdown("**Findings:**")
                    
                    findings = analysis.get('findings', [])
                    if isinstance(findings, list):
                        for pat in findings:
                            st.markdown(f"- {pat}")
                    else:
                        st.markdown(str(findings))

    else:
        st.info("Waiting for data... (Run the watcher!)")
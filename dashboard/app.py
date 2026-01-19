# dashboard/app.py
import streamlit as st
import json
import os
from PIL import Image

st.set_page_config(page_title="Dead Hand Dashboard", layout="wide")

st.title("💀 Dead Hand: Dark Pattern Hunter")

# Sidebar: Select Run
traj_dir = "trajectories"
if not os.path.exists(traj_dir):
    os.makedirs(traj_dir)
    
runs = sorted(os.listdir(traj_dir), reverse=True)
selected_run = st.sidebar.selectbox("Select Mission Log", runs)

if selected_run:
    run_path = os.path.join(traj_dir, selected_run)
    
    # Load Audit Data
    try:
        with open(os.path.join(run_path, "audit_report.json"), "r") as f:
            audit_data = json.load(f)
            
        # Metrics
        scores = [step.get('darkness_score', 0) for step in audit_data]
        avg_score = sum(scores) / len(scores) if scores else 0
        max_score = max(scores) if scores else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Max Darkness Detected", f"{max_score}/10", delta_color="inverse")
        col2.metric("Steps Taken", len(audit_data))
        col3.metric("Status", "Audit Complete")
        
        st.divider()
        
        # Replay Slider
        step_idx = st.slider("Replay Step", 0, len(audit_data)-1, 0)
        
        current_step = audit_data[step_idx]
        
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader("Agent View")
            # Dynamic Image Loading
            img_path = os.path.join(run_path, f"step_{step_idx}.png")
            if os.path.exists(img_path):
                st.image(Image.open(img_path), caption=f"Step {step_idx}")
            else:
                st.info("Screenshot not found for this step.")
                
        with c2:
            st.subheader("🔍 Pattern Analysis")
            score = current_step.get('darkness_score', 0)
            
            if score > 7:
                st.error(f"High Darkness Score: {score}/10")
            elif score > 3:
                st.warning(f"Medium Darkness Score: {score}/10")
            else:
                st.success(f"Low Darkness Score: {score}/10")
                
            st.write(f"**Analysis:** {current_step.get('analysis', 'No data')}")
            
            patterns = current_step.get('patterns_detected', [])
            if patterns:
                st.write("**Detected Patterns:**")
                for p in patterns:
                    st.markdown(f"- 🔴 {p}")
                    
    except FileNotFoundError:
        st.error("No audit report found for this run yet.")
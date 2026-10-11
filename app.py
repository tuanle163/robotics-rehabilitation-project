"""Robotic Hand Rehabilitation (HEXORA) - portfolio of Tuan Le, Control Development lead.
Run:  streamlit run app.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

A = Path(__file__).parent / "assets"
st.set_page_config(page_title="HEXORA | Robotic Hand Rehabilitation", page_icon="🦾", layout="wide")

TEAL, ORANGE, NAVY = "#14b8a6", "#f97316", "#0f172a"

st.markdown(
    f"""
<style>
.block-container {{padding-top: 1.2rem; max-width: 1150px;}}
.hero {{background: linear-gradient(135deg,{NAVY} 0%,#134e4a 100%); color:#fff; padding:2.6rem 2.2rem;
        border-radius:18px; margin-bottom:1.2rem;}}
.hero h1 {{font-size:2.6rem; margin:0 0 .3rem 0; color:#fff;}}
.hero p {{font-size:1.1rem; color:#cbd5e1; margin:.2rem 0;}}
.chip {{display:inline-block; background:rgba(20,184,166,.18); color:#5eead4; border:1px solid #14b8a6;
        padding:.15rem .7rem; border-radius:999px; margin:.2rem .25rem .2rem 0; font-size:.85rem;}}
.card {{background:#f8fafc; border:1px solid #e2e8f0; border-left:5px solid {TEAL}; border-radius:12px;
        padding:1rem 1.2rem; height:100%; color:#0f172a;}}
.card h4 {{margin:0 0 .4rem 0; color:#0f172a;}}
.card.warn {{border-left-color:{ORANGE};}}
.kpi {{text-align:center; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:.9rem .4rem;}}
.kpi b {{font-size:1.7rem; color:{TEAL}; display:block;}}
.kpi span {{font-size:.8rem; color:#475569;}}
</style>
""",
    unsafe_allow_html=True,
)


def card(title, body, warn=False):
    st.markdown(f'<div class="card {"warn" if warn else ""}"><h4>{title}</h4>{body}</div>', unsafe_allow_html=True)


def kpis(items):
    for col, (v, l) in zip(st.columns(len(items)), items):
        col.markdown(f'<div class="kpi"><b>{v}</b><span>{l}</span></div>', unsafe_allow_html=True)


def img(name, caption):
    st.image(str(A / name), caption=caption, use_container_width=True)


# ------------------------------------------------------------------ HERO
st.markdown(
    """
<div class="hero">
<span class="chip">MEng Mechatronics</span><span class="chip">University of Leeds · MECH 5030M Team Project</span>
<h1>HEXORA - Robotic Hand Rehabilitation After Stroke</h1>
<p>A portable, wearable hand exoskeleton delivering passive-assist therapy for flaccid post-stroke hands.</p>
<p><b>Huynh Minh Tuan Le</b> - Control Development: embedded control, electronics, GUI and sensing validation</p>
</div>
""",
    unsafe_allow_html=True,
)

tabs = st.tabs(["🏠 Overview", "🧩 System Design", "🎛️ Control & Electronics",
                "🔁 Closed → Open Loop", "🧪 Testing & Results", "🧠 Skills & Role"])

# ------------------------------------------------------------------ OVERVIEW
with tabs[0]:
    kpis([("150,000", "UK strokes / year"), ("77-85%", "hemiparesis of upper limb"),
          ("5", "engineers, 3 disciplines"), ("3.7%", "motion-capture validation error")])
    st.write("")
    c1, c2 = st.columns([1.1, 1])
    with c1:
        st.subheader("The problem")
        st.write(
            "Stroke is a leading cause of disability. Most survivors suffer hemiparesis, and **flaccidity** "
            "(weakness and loss of dexterity) is more common than spasticity. Conventional physiotherapy is expensive, "
            "so patients receive too little of it. Robotic devices can deliver repeatable, affordable therapy, "
            "but many are bulky and clinic-bound."
        )
        st.subheader("The aim")
        st.info("Design, build and test a **portable** hand rehabilitation prototype giving **active-assistive movement "
                "therapy** with a **graphical user interface** to post-stroke patients with hand flaccidity.")
        st.subheader("Objectives")
        st.markdown(
            "1. Hand motion and torque analysis → design specification\n"
            "2. Follow a design process to develop the exoskeleton\n"
            "3. **Develop a controller to provide hand rehabilitation motion** *(my focus)*\n"
            "4. Test the device against the requirements"
        )
    with c2:
        img("exo3.png", "Index-finger exoskeleton CAD: motors, potentiometers, tension cables, radial index module")
    st.subheader("Project timeline")
    st.markdown(
        "| Stage | Output |\n|---|---|\n"
        "| Presentation 1 (Oct 2016) | Literature review, aim, objectives, deliverables |\n"
        "| Data acquisition | Optotrak motion capture & force-gauge experiments, validated |\n"
        "| Presentation 2 (Mar 2017) | Design development, FEA/fatigue, electronics, first GUI |\n"
        "| Final | Prototype build, ROM / sensing / functional tests, report & poster |"
    )

# ------------------------------------------------------------------ SYSTEM DESIGN
with tabs[1]:
    st.subheader("System architecture")
    st.graphviz_chart(
        """
digraph G { rankdir=LR; node [shape=box, style="rounded,filled", fontname=Helvetica, fillcolor="#f1f5f9", color="#0f172a"];
 GUI [label="Desktop GUI (LabVIEW)\\nangle sliders · live plots · E-stop", fillcolor="#99f6e4"];
 CRIO [label="NI cRIO 9024 (real-time + FPGA)\\ntrajectory interpolation\\nangle → PWM duty", fillcolor="#fed7aa"];
 DO [label="NI 9401\\nPWM out"]; AI [label="NI 9215\\nanalog in"];
 SERVO [label="Servo motors\\n(internal closed loop)\\nMCP · PIP"];
 GEAR [label="2:1 spur gears + cable\\ntransmission"];
 FINGER [label="Index finger\\nMCP + PIP", fillcolor="#bae6fd"];
 POT [label="Potentiometers\\n(position monitoring)"];
 GUI -> CRIO [label="Ethernet"]; CRIO -> DO -> SERVO -> GEAR -> FINGER;
 GEAR -> POT -> AI -> CRIO; CRIO -> GUI [label="actual angle", style=dashed];
}"""
    )
    st.subheader("Mechanical design")
    c1, c2 = st.columns(2)
    with c1:
        img("p2_s11_3.png", "CAD of index module on a hand model (SolidWorks)")
    with c2:
        img("exo4.png", "Exoskeleton concept")
    c1, c2, c3 = st.columns(3)
    with c1:
        card("Index finger module", "MCP and PIP independently actuated by servos and cable transmission. "
             "ROM 80° (MCP) / 90° (PIP); mechanical stops prevent hyper-flexion/extension; adjustable to hand sizes.")
    with c2:
        card("Fingers 3-5 module", "One actuator drives three pulley loops: the three fingers move almost identically "
             "in grasp/release and tip pinch, so one actuator is sufficient.")
    with c3:
        card("Materials", "Aluminium alloy for finger parts (safety factor 12.97, ~10⁸ cycles); PLA base for the prototype "
             "(~1.08×10⁶ cycles under extreme stress). Chosen on biocompatibility, function and cost.")
    st.subheader("Design requirements derived from experiments")
    st.dataframe(pd.DataFrame({
        "Requirement": ["Torque (max)", "Angular speed", "Range of motion", "Controller"],
        "Specification": ["MCP 1.96 Nm · PIP 0.61 Nm", "3.00-3.79 rad/s", "MCP 0-80° · PIP 0-90°",
                          "Originally: closed-loop PID"]}), hide_index=True, use_container_width=True)

# ------------------------------------------------------------------ CONTROL
with tabs[2]:
    st.subheader("My contribution: embedded control, electronics & GUI")
    c1, c2 = st.columns(2)
    with c1:
        card("Hardware", "<ul><li><b>NI CompactRIO 9024</b>: real-time controller + FPGA</li>"
             "<li><b>NI 9401</b> digital I/O → PWM to servos (250 Hz)</li><li><b>NI 9215</b> analog in ← potentiometers</li>"
             "<li>Power HD 3688HB &amp; Corona DS-929MG servos</li><li>Vishay P11P potentiometers, Interlink FSRs</li></ul>")
    with c2:
        card("Software (LabVIEW)", "<ul><li>Interpolation filter for smooth trajectory planning</li>"
             "<li>Desired angle → PWM duty-cycle mapping from benchmark calibration</li>"
             "<li>GUI: MCP/PIP angle sliders, live desired-vs-actual plots, emergency stop</li>"
             "<li>Passive-assist mode: full assistance for flexion/extension</li></ul>")
    st.subheader("Servo calibration benchmark")
    st.caption("PWM duty cycle swept; angle measured via potentiometers.")
    st.dataframe(pd.DataFrame({"Motor": ["MCP", "PIP"], "Duty min (%)": [22.5, 16], "Duty max (%)": [52.5, 60],
                               "ROM min (°)": [0, 0], "ROM max (°)": [120.49, 150]}),
                 hide_index=True, use_container_width=True)
    st.subheader("Safety by design")
    st.markdown("FMEA identified four hazards: **hyperextension, joint breakage, electric shock, mechanical failure.** "
                "Mitigations: mechanical stops, software-limited duty cycles within safe ROM, emergency stop in the GUI.")

# ------------------------------------------------------------------ CLOSED -> OPEN
with tabs[3]:
    st.subheader("Why I moved from closed-loop to open-loop control")
    kpis([("~4°", "sensor drift per grasp-release cycle"), ("2:1", "spur gear to potentiometer"),
          ("Backlash", "root cause"), ("Open loop", "chosen strategy")])
    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        card("1 · Plan", "Requirement: closed-loop PID on joint angle, with the potentiometer as feedback.")
    with c2:
        card("2 · Evidence", "Optotrak vs potentiometer showed the reading <b>freezes at zero velocity / direction "
             "changes</b> and drifts ~4° per cycle: gear backlash. Error compounds over cycles.", warn=True)
    with c3:
        card("3 · Decision", "Feedback unreliable → closed loop would chase a wrong signal. Use <b>open loop</b>: "
             "servos' internal loop holds position from PWM; potentiometer is for <b>display/monitoring only</b>.")
    st.markdown("**Trade-off.** Open loop gives up active error correction, but keeps motion stable and smooth and "
                "bounded by the calibrated PWM map and mechanical stops. Proposed fix: smaller-module gears, or a "
                "backlash-free sensor (e.g. encoder at the joint).")

    st.subheader("🔬 Interactive illustration")
    st.caption("Illustrative model, not measured data. Sensor drift is parameterised from the ~4° observed per cycle.")
    cc1, cc2, cc3 = st.columns(3)
    drift = cc1.slider("Sensor drift per cycle (°)", 0.0, 8.0, 4.0, 0.5)
    cycles = cc2.slider("Grasp-release cycles", 1, 8, 5)
    target_amp = cc3.slider("Target amplitude (°)", 30, 90, 70)
    t = np.linspace(0, cycles, 80 * cycles)
    target = target_amp / 2 * (1 - np.cos(2 * np.pi * t))
    sensor_bias = drift * t                       # drift accumulates in measurement
    # closed loop: controller servoes the *measured* value to the target -> true angle absorbs the bias
    closed_true = target - sensor_bias * np.clip(target / max(target_amp, 1), 0, 1)
    # open loop: PWM map + servo internal loop; small fixed gain error, no accumulation
    open_true = target * 0.92 + 0
    fig = go.Figure()
    fig.add_scatter(x=t, y=target, name="Target", line=dict(color="#94a3b8", dash="dot"))
    fig.add_scatter(x=t, y=open_true, name="Open loop (actual)", line=dict(color=TEAL, width=3))
    fig.add_scatter(x=t, y=closed_true, name="Closed loop on drifting sensor (actual)", line=dict(color=ORANGE, width=3))
    fig.update_layout(height=380, xaxis_title="Cycle", yaxis_title="Joint angle (°)", margin=dict(t=20),
                      legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("With drift, the closed-loop actual angle wanders further from the target each cycle; "
               "the open-loop error stays bounded (measured open-loop error was ~9-15 % for MCP).")

# ------------------------------------------------------------------ TESTING
with tabs[4]:
    st.subheader("Verification & validation")
    kpis([("±2.70°", "Optotrak jig uncertainty"), ("±0.91 N", "force gauge accuracy"),
          ("12%", "force validation error"), ("63.5°", "MCP actual @ 70° demand")])
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### MCP functional test (open loop)")
        mcp = pd.DataFrame({"Desired (°)": [30, 50, 70], "Error (°)": [4.4, 5.57, 6.47], "Error (%)": [-14.67, -11.14, -9.24]})
        st.dataframe(mcp, hide_index=True, use_container_width=True)
        f = go.Figure(go.Bar(x=mcp["Desired (°)"], y=mcp["Error (°)"], marker_color=TEAL))
        f.update_layout(height=260, margin=dict(t=10), xaxis_title="Desired (°)", yaxis_title="Error (°)")
        st.plotly_chart(f, use_container_width=True)
        st.caption("Max 70° demand → 63.53° actual; below safety limit of 89.91°. Smooth 0-70° transient.")
    with c2:
        st.markdown("##### PIP functional test (open loop)")
        pip = pd.DataFrame({"Desired (°)": [50, 70], "Error (°)": [-8.25, -27.15], "Error (%)": [16.50, 38.79]})
        st.dataframe(pip, hide_index=True, use_container_width=True)
        f = go.Figure(go.Bar(x=pip["Desired (°)"], y=pip["Error (°)"], marker_color=ORANGE))
        f.update_layout(height=260, margin=dict(t=10), xaxis_title="Desired (°)", yaxis_title="Error (°)")
        st.plotly_chart(f, use_container_width=True)
        st.caption("Max 90° demand → 106° actual; below safety limit of 114.10°. Larger PIP error is an honest limitation of open loop.")
    st.subheader("Outcome")
    st.success("The prototype actuated the index finger in passive-assist mode within the safe ROM (110° PIP, 90° MCP), "
               "achieved cylindrical grasp, and was unable to achieve tip pinch.")
    st.warning("Limitations: only the index finger was actuated; open-loop accuracy limited by backlash. "
               "Future work: low-module/backlash-free sensing, then reinstate closed-loop control.")

# ------------------------------------------------------------------ SKILLS
with tabs[5]:
    st.subheader("My role")
    st.write("**Control Development** within a 5-person multidisciplinary team (Mechatronics, Mechanical, Medical Engineering), "
             "supervised by Dr Andrew Jackson.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Research skills")
        st.markdown(
            "- Literature review: stroke impairment, therapy types, hand kinematics, actuation and controller design\n"
            "- Designed and validated experiments (Optotrak motion capture, force gauge) before trusting data\n"
            "- Quantified uncertainty (±2.70°, ±0.91 N) and error\n"
            "- Used evidence (Optotrak vs potentiometer) to overturn an initial design requirement\n"
            "- Compared admittance and PID control strategies")
        st.markdown("#### Engineering skills")
        st.markdown("`LabVIEW` `NI cRIO / FPGA` `PWM` `PID` `MATLAB` `SolidWorks` `Optotrak` `FEA` `FMEA`")
    with c2:
        st.markdown("#### Project skills")
        st.markdown(
            "- Requirements → design specification traceability\n"
            "- Risk assessment (FMEA) and safety-led design\n"
            "- Contract Performance Plan, weekly meeting minutes, three presentations, poster and report\n"
            "- Clear technical communication to clinical and engineering audiences\n"
            "- Honest reporting of trade-offs and limitations")
        st.markdown("#### Key takeaway")
        st.info("Good engineering is following the data: when feedback was unreliable, I removed it from the control path.")
    st.subheader("Gallery")
    cols = st.columns(3)
    for col, (n, cap) in zip(cols, [("exo1.png", "Concept 1"), ("exo2.png", "Concept 2"), ("exo4.png", "Concept 3")]):
        with col:
            img(n, cap)

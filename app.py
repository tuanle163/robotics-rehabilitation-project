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
                "🔁 Closed → Open Loop", "🧪 Testing & Results", "🎥 Demo Video", "🧠 Skills & Role"])

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
        "| Final | Prototype build, range of motion (ROM), sensing and functional tests, report & poster |"
    )

# ------------------------------------------------------------------ SYSTEM DESIGN
with tabs[1]:
    st.subheader("System architecture")
    st.markdown("The cRIO sends **PWM** signals through the NI 9401 to the MCP and PIP servos (6 V supply), and reads "
                "potentiometer voltages (5 V supply) through the NI 9215.")
    with st.expander("End-to-end data flow (GUI → finger → GUI)", expanded=True):
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
             "Range of motion (ROM) 80° (MCP) / 90° (PIP); mechanical stops prevent hyper-flexion/extension; adjustable to hand sizes.")
    with c2:
        card("Fingers 3-5 module", "One actuator drives three pulley loops: the three fingers move almost identically "
             "in grasp/release and tip pinch, so one actuator is sufficient.")
    with c3:
        card("Materials", "Aluminium alloy for finger parts (safety factor 12.97, ~10⁸ cycles); PLA base for the prototype "
             "(~1.08×10⁶ cycles under extreme stress). Chosen on biocompatibility, function and cost.")
    st.info("**ROM = Range of Motion**: the angle a joint can safely move through, from fully extended (0°) to fully flexed. "
            "For this device it is **MCP 0-80°** (knuckle joint at the base of the finger) and **PIP 0-90°** "
            "(middle finger joint). Mechanical stops and software limits keep the finger inside its ROM so it cannot hyper-flex or hyper-extend.")
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
    from plotly.subplots import make_subplots
    st.subheader("Why I moved from closed-loop to open-loop control")
    kpis([("~4°", "sensor drift per cycle"), ("Backlash", "root cause (2:1 spur gear)"),
          ("Open loop", "chosen strategy"), ("Interpolated", "smooth trajectory planning")])
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### ❌ Closed loop: backlash makes the sensor drift")
        t = np.linspace(0, 3, 600)
        motor = 35 * (1 - np.cos(2 * np.pi * t))                 # true joint angle (illustrative)
        play = 2.0                                               # gear slack (deg)
        pot = np.zeros_like(motor)
        for i in range(1, len(t)):                               # slack must be taken up before the pot moves
            d = motor[i] - pot[i - 1]
            pot[i] = pot[i - 1] + (d - play / 2 if d > play / 2 else d + play / 2 if d < -play / 2 else 0)
        pot = pot - 2 * play * t                                 # error accumulates ~4° per cycle
        f1 = go.Figure()
        f1.add_scatter(x=t, y=motor, name="True angle", line=dict(color="#64748b", width=3))
        f1.add_scatter(x=t, y=pot, name="Potentiometer", line=dict(color=ORANGE, width=3),
                       fill="tonexty", fillcolor="rgba(220,38,38,.18)")
        f1.update_layout(height=300, margin=dict(t=10, b=10), xaxis_title="Cycle", yaxis_title="Angle (°)",
                         legend=dict(orientation="h", y=1.12))
        st.plotly_chart(f1, use_container_width=True)
        st.caption("Reading goes flat at every reversal (gear slack); the red gap grows each cycle, "
                   "so a feedback loop would chase a wrong value. Illustrative model of the ~4°/cycle measured.")
    with c2:
        st.markdown("##### ✅ Open loop + interpolated trajectory")
        tt = np.linspace(0, 4, 500)
        x = np.clip(tt - 0.5, 0, 2.5) / 2.5
        step = np.where(tt >= 0.5, 70.0, 0.0)
        smooth = 70 * (10 * x**3 - 15 * x**4 + 6 * x**5)
        f2 = make_subplots(specs=[[{"secondary_y": True}]])
        f2.add_scatter(x=tt, y=step, name="Raw command (step)", line=dict(color="#94a3b8", dash="dot"))
        f2.add_scatter(x=tt, y=smooth, name="Interpolated angle", line=dict(color=TEAL, width=4))
        f2.add_scatter(x=tt, y=np.gradient(smooth, tt), name="Speed (°/s)", line=dict(color=ORANGE, width=2),
                       fill="tozeroy", fillcolor="rgba(249,115,22,.15)", secondary_y=True)
        f2.update_layout(height=300, margin=dict(t=10, b=10), xaxis_title="Time (s)",
                         legend=dict(orientation="h", y=1.12))
        f2.update_yaxes(title_text="Angle (°)", secondary_y=False)
        f2.update_yaxes(title_text="Speed (°/s)", secondary_y=True, showgrid=False)
        st.plotly_chart(f2, use_container_width=True)
        st.caption("The interpolation filter turns the GUI's desired angle into a smooth trajectory: speed starts "
                   "and ends at zero, so the servo moves gently.")
    st.success("**Pipeline:** desired angle → **interpolation (trajectory planning)** → angle-to-PWM duty map → servo's "
               "internal loop → finger.  The potentiometer is kept for **GUI display only**.")
    st.markdown("**Trade-off.** Open loop gives up active error correction, but motion stays stable, smooth and "
                "bounded by the calibrated PWM map and mechanical stops. Future fix: smaller-module gears or a "
                "backlash-free joint encoder, then reinstate closed loop.")

    st.subheader("🔬 See it yourself: why a drifting sensor is dangerous in closed loop")
    st.markdown(
        "**How to read this:** the finger is asked to bend to the *target*. In **closed loop** the controller keeps "
        "pushing until its **sensor** says the target is reached. But the backlash makes the sensor read *too low* a "
        "little more every cycle, so the controller pushes the real finger **further and further**. "
        "In **open loop** the servo simply goes to the calibrated position, so the finger does not creep."
    )
    st.caption("Simplified illustration, not measured data. Drift is based on the ~4° per cycle observed in testing; "
               "open-loop result matches the measured 63.5° at a 70° demand.")
    cc1, cc2 = st.columns(2)
    cycle = cc1.slider("Move the slider: number of grasp-release cycles completed", 0, 8, 0)
    drift = cc2.slider("Sensor drift per cycle (°)", 1.0, 6.0, 4.0, 0.5)
    target_v, limit = 70.0, 89.91   # MCP demand and MCP safety limit from the report
    closed_actual = target_v + drift * cycle
    open_actual = target_v * 0.908
    # ---- horizontal bar chart
    names = ["Closed loop (actual finger)", "Open loop (actual finger)", "Target"]
    vals = [closed_actual, open_actual, target_v]
    cols_ = [ORANGE if closed_actual <= limit else "#dc2626", TEAL, "#94a3b8"]
    fig = go.Figure(go.Bar(y=names, x=vals, orientation="h", marker_color=cols_,
                           text=[f"{v:.1f}°" for v in vals], textposition="outside"))
    fig.add_vline(x=limit, line_dash="dash", line_color="#dc2626",
                  annotation_text="Safety limit 89.9°", annotation_position="top")
    fig.update_layout(height=260, xaxis=dict(title="MCP joint angle (°)", range=[0, 130]), margin=dict(t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)

    # ---- finger drawing: the line (phalanx) rotates about the MCP / PIP joints
    def finger(mcp_deg, pip_ratio=1.0):
        """Side view. Flexion rotates the finger downward. Returns joint coordinates."""
        a1 = np.radians(mcp_deg)
        a2 = np.radians(mcp_deg * pip_ratio)
        palm = (-3.0, 0.0)
        mcp = (0.0, 0.0)
        pip = (mcp[0] + 4.5 * np.cos(a1), mcp[1] - 4.5 * np.sin(a1))
        tip = (pip[0] + 3.5 * np.cos(a1 + a2), pip[1] - 3.5 * np.sin(a1 + a2))
        return palm, mcp, pip, tip

    from plotly.subplots import make_subplots
    fig2 = make_subplots(rows=1, cols=2, subplot_titles=("Open loop", "Closed loop"), horizontal_spacing=0.06)
    for col, (ang, color) in enumerate([(open_actual, TEAL),
                                        (closed_actual, ORANGE if closed_actual <= limit else "#dc2626")], start=1):
        for a_deg, c, w, dash, nm in [(limit, "#dc2626", 2, "dash", "Safety limit"),
                                      (target_v, "#94a3b8", 5, "dot", "Target"),
                                      (ang, color, 9, "solid", "Actual finger")]:
            p, m, pp, t_ = finger(a_deg)
            fig2.add_trace(go.Scatter(x=[p[0], m[0], pp[0], t_[0]] if nm != "Safety limit" else [m[0], pp[0]],
                                      y=[p[1], m[1], pp[1], t_[1]] if nm != "Safety limit" else [m[1], pp[1]],
                                      mode="lines", line=dict(color=c, width=w, dash=dash),
                                      name=nm, showlegend=(col == 1)), row=1, col=col)
        p, m, pp, t_ = finger(ang)
        fig2.add_trace(go.Scatter(x=[m[0], pp[0]], y=[m[1], pp[1]], mode="markers+text",
                                  marker=dict(size=16, color="white", line=dict(color="#0f172a", width=3)),
                                  text=["MCP", "PIP"], textposition="top center", showlegend=False), row=1, col=col)
        fig2.add_annotation(x=1.2, y=-0.9, text=f"{ang:.0f}°", showarrow=False, font=dict(size=18, color=color),
                            row=1, col=col)
    fig2.update_xaxes(visible=False, range=[-4, 9], scaleanchor="y", scaleratio=1)
    fig2.update_yaxes(visible=False, range=[-9, 3])
    fig2.update_layout(height=380, margin=dict(t=40, b=0), legend=dict(orientation="h", y=-0.02))
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Side view of the index finger. The line rotates about the MCP joint (palm side) and PIP joint. "
               "Grey dotted = target, red dashed = safety limit. PIP is drawn following the MCP angle for illustration.")
    if closed_actual > limit:
        st.error(f"After {cycle} cycles the closed-loop finger reaches {closed_actual:.1f}°, past the safety limit. "
                 "Open loop stays steady.")
    elif cycle == 0:
        st.info("At the start both work. Now drag the cycle slider to the right.")
    else:
        st.warning(f"Closed loop has crept {closed_actual - target_v:.1f}° beyond target and keeps growing; open loop is unchanged.")


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
    st.subheader("Prototype demo")
    st.video("https://youtu.be/o3KeEM2h4Hs")
    vids = sorted(p for p in A.glob("*") if p.suffix.lower() in (".mov", ".mp4", ".webm"))
    if vids:
      with st.expander("Local copy of the demo (if YouTube is blocked)"):
        st.video(str(vids[0]))

with tabs[6]:
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
    for col, (n, cap) in zip(cols, [("exo1.png", "View 1"), ("exo2.png", "View 2"), ("exo4.png", "View 3")]):
        with col:
            img(n, cap)

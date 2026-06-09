import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utils.parser import extract_text
from utils.analyzer import load_skills, extract_skills, get_required_skills
from utils.scorer import calculate_score, missing_skills
from utils.suggestions import generate_suggestions
from utils.resume_quality import project_score, experience_score, structure_score, skill_density_score
from utils.impact_analyzer import detect_achievements
from utils.bullet_analyzer import analyze_bullets
from utils.section_classifier import classify_sections
from utils.skill_gap import analyze_skill_gap
from utils.job_recommender import recommend_jobs

def run():

    st.set_page_config(
        page_title="AI Resume Analyzer",
        layout="centered",
        page_icon="📄"
    )

    st.markdown("""
<style>

/* Galaxy Background */

.stApp{
background:
radial-gradient(circle at 20% 20%, #5b0f4a 0%, transparent 40%),
radial-gradient(circle at 80% 30%, #3c096c 0%, transparent 40%),
radial-gradient(circle at 50% 80%, #240046 0%, transparent 40%),
linear-gradient(180deg,#0d001a,#020006);
color:white;
}

/* Button */

.stButton>button{
background:linear-gradient(90deg,#800f2f,#7b2cbf);
border-radius:30px;
color:white;
}

/* Skill Chips */


                .skill-chip{
display:inline-block;
padding:8px 14px;
margin:6px;
background:linear-gradient(90deg,#7b2cbf,#9d4edd);
border-radius:30px;
font-size:14px;
transition:all 0.25s ease;
box-shadow:0 0 8px rgba(157,78,221,0.6);
}

.skill-chip:hover{
transform: translateY(-6px) scale(1.08);
box-shadow:0 0 20px rgba(200,120,255,1);
}


/* futuristic analysis box */

.analysis-box{
border:1px solid rgba(255,255,255,0.15);
border-radius:14px;
padding:20px;
margin-top:20px;
background:rgba(0,0,0,0.35);
backdrop-filter: blur(10px);
box-shadow:0 0 25px rgba(140,80,255,0.3);
}

/* metallic header */

.analysis-header{
font-size:20px;
font-weight:600;
padding:10px 15px;
margin-bottom:15px;
border-radius:8px;

background:linear-gradient(
90deg,
#d4d4d4,
#f5f5f5,
#bcbcbc,
#ffffff,
#d4d4d4
);

color:black;
letter-spacing:1px;
}

/* table styling */

.analysis-table{
width:100%;
border-collapse:collapse;
}

.analysis-table td{
border:1px solid rgba(255,255,255,0.2);
padding:8px;
}

/* tech bullet */

.tech-bullet{
color:#c77dff;
font-weight:600;
margin-right:8px;
}
                
                .section-card{
border:1px solid rgba(255,255,255,0.15);
border-radius:14px;
padding:18px;
background:rgba(0,0,0,0.35);
box-shadow:0 0 20px rgba(140,80,255,0.25);
margin-top:15px;
height:100%;
display:flex;
flex-direction:column;
}

.section-header{
font-size:18px;
font-weight:600;
padding:8px 12px;
margin-bottom:12px;
border-radius:6px;

background:linear-gradient(
90deg,
#cfcfcf,
#f2f2f2,
#cfcfcf
);

color:black;
}

.stat-ball{
display:inline-block;
width:80px;
height:80px;
border-radius:50%;
background:linear-gradient(145deg,#7b2cbf,#9d4edd);
color:white;
font-size:22px;
font-weight:bold;
text-align:center;
line-height:80px;
margin:10px;
box-shadow:0 0 18px rgba(157,78,221,0.7);
}

.stat-label{
text-align:center;
font-size:12px;
margin-top:4px;
color:#e0e0e0;
}
                /* Galaxy title box */

.hero-box{
position:relative;
padding:30px 20px;
border-radius:18px;
margin-bottom:25px;
text-align:center;

/* galaxy background */
background:
radial-gradient(circle at 20% 30%, rgba(255,255,255,0.15) 2px, transparent 3px),
radial-gradient(circle at 70% 20%, rgba(255,255,255,0.2) 1px, transparent 3px),
radial-gradient(circle at 40% 80%, rgba(255,255,255,0.15) 2px, transparent 4px),
linear-gradient(135deg,#240046,#5a189a,#3c096c);

box-shadow:
0 0 30px rgba(157,78,221,0.6),
inset 0 0 20px rgba(255,255,255,0.08);

border:2px solid rgba(255,255,255,0.25);
}

/* shiny metallic title */

.hero-title{
font-size:42px;
font-weight:800;

background:linear-gradient(
90deg,
#dcdcdc,
#ffffff,
#bfbfbf,
#ffffff,
#dcdcdc
);

-webkit-background-clip:text;
-webkit-text-fill-color:transparent;

letter-spacing:1px;
}

/* subtitle */

.hero-subtitle{
color:#d0cde1;
font-size:16px;
margin-top:8px;
}

/* shine animation */

.hero-box:before{
content:"";
position:absolute;
top:0;
left:-75%;
width:50%;
height:100%;
background:linear-gradient(
120deg,
transparent,
rgba(255,255,255,0.3),
transparent
);
transform:skewX(-20deg);
animation:shine 6s infinite;
}

@keyframes shine{
0%{left:-75%;}
100%{left:130%;}
}
.job-card{
background:rgba(123,44,191,0.15);
border:1px solid rgba(255,255,255,0.15);
border-radius:14px;
padding:18px;
text-align:center;
margin:8px 0;
font-size:16px;
font-weight:600;
box-shadow:0 0 15px rgba(157,78,221,0.25);
transition:0.3s;
}

.job-card:hover{
transform:translateY(-5px);
box-shadow:0 0 25px rgba(157,78,221,0.6);
}

.job-icon{
font-size:28px;
display:block;
margin-bottom:8px;
}
</style>
""", unsafe_allow_html=True)

    st.markdown(
"""
<div class="hero-box">

<div class="hero-title">
AI Resume Analyzer
</div>

<div class="hero-subtitle">
Upload your resume and get AI powered ATS analysis, skill gap insights,
and career recommendations.
</div>

</div>
""",
unsafe_allow_html=True
)

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_role = st.text_input("Enter Target Job Role")

    analyze = st.button("Analyze Resume")

    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    skills_path = os.path.join(BASE_DIR, "data", "skills.json")

    skills = load_skills(skills_path)

    if analyze and uploaded_file and job_role:

        text = extract_text(uploaded_file)
        found_skills = extract_skills(text, skills)
        required_skills = get_required_skills(job_role)

        skill_score = calculate_score(found_skills, required_skills)

        proj_score = project_score(text)
        exp_score = experience_score(text)
        struct_score = structure_score(text)
        density_score = skill_density_score(text, found_skills)

        impact_score, achievement_count = detect_achievements(text)
        bullet_score, bullet_count = analyze_bullets(text)
        sections_detected = classify_sections(text)

        score = (
            0.35 * skill_score +
            0.15 * proj_score +
            0.15 * exp_score +
            0.10 * struct_score +
            0.10 * density_score +
            0.10 * impact_score +
            0.05 * bullet_score
        )

        missing = missing_skills(found_skills, required_skills)
        matched_skills, gap_skills, match_count, total_required = analyze_skill_gap(found_skills, required_skills)
        recommended_jobs = recommend_jobs(found_skills)
        suggestions = generate_suggestions(found_skills, missing, text)

        st.markdown("## ATS Score")
        st.progress(int(max(min(score, 100), 0)))
        st.markdown(f"### {round(score,2)} %")

        st.subheader("Resume vs Industry Benchmark")

        labels = [
            "Skill Match",
            "Projects",
            "Experience",
            "Structure",
            "Density",
            "Impact",
            "Bullets"
        ]

        user_scores = [
            skill_score,
            proj_score,
            exp_score,
            struct_score,
            density_score,
            impact_score,
            bullet_score
        ]

        industry_scores = [
            65,
            60,
            55,
            70,
            60,
            50,
            55
        ]

        x = np.arange(len(labels))
        width = 0.38

        fig, ax = plt.subplots(figsize=(8,4))

        user_color = "#7dd3fc"
        industry_color = "#0284c7"

        bars1 = ax.bar(
            x - width/2,
            user_scores,
            width,
            label="Your Resume",
            color=user_color
        )

        bars2 = ax.bar(
            x + width/2,
            industry_scores,
            width,
            label="Industry Average",
            color=industry_color
        )

        ax.set_ylabel("Score")
        ax.set_ylim(0,100)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=20)
        ax.legend()

        for bar in bars1:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2,
                height + 1,
                f"{height:.0f}",
                ha="center",
                va="bottom",
                fontsize=9
            )

        for bar in bars2:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2,
                height + 1,
                f"{height:.0f}",
                ha="center",
                va="bottom",
                fontsize=9
            )

        plt.tight_layout()
        st.pyplot(fig)

        coverage = min(len(found_skills) / max(len(required_skills), 1), 1)

        st.subheader("Skill Coverage")
        st.progress(int(coverage * 100))
        st.write(str(round(coverage * 100, 2)) + " % role skill coverage")

        skill_html = ""
        for s in sorted(found_skills):
            skill_html += f'<span class="skill-chip">{s}</span>'

        st.markdown(skill_html, unsafe_allow_html=True)
        st.subheader("Missing Skills")

        missing_html = ""
        for s in missing:
            missing_html += f'<span class="skill-chip">{s}</span>'

        st.markdown(missing_html, unsafe_allow_html=True)

        gap_html = f"""
        <div class="analysis-box">

        <div class="analysis-header">
        AI Skill Gap Analysis
        </div>

        <table class="analysis-table">
        <tr>
        <td>Matched Skills</td>
        <td>{match_count} / {total_required}</td>
        </tr>
        </table>
        """

        if len(gap_skills) > 0:
            gap_html += "<br><b>Recommended Skills To Learn</b><br>"

            for s in gap_skills:
                gap_html += f'<div><span class="tech-bullet">⚙</span>{s}</div>'

        else:
            gap_html += "<br>Your resume already covers the required skill set."

        gap_html += "</div>"

        st.markdown(gap_html, unsafe_allow_html=True)
        st.markdown("""
        <div class="analysis-box">
        <div class="analysis-header">
        AI Career Recommendations
        </div>
        </div>
        """, unsafe_allow_html=True)

        if recommended_jobs:

            cols = st.columns(3)

            for idx, job in enumerate(recommended_jobs):

                with cols[idx % 3]:

                    st.markdown(
                        f"""
                        <div class="job-card">
                            <span class="job-icon">🚀</span>
                            {job}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        else:

            st.warning(
                "Not enough skill signals detected to recommend roles."
            )


            st.subheader("Analysis Visualizations")

        colA, colB = st.columns(2)

        with colA:
            labels = ["Matched Skills", "Missing Skills"]
            matched = len(matched_skills)
            values = [matched, len(missing)]
            fig, ax = plt.subplots()
            ax.bar(labels, values)
            st.pyplot(fig)

        with colB:
            labels = ["Skill", "Projects", "Experience", "Structure", "Density", "Impact", "Bullets"]
            values = [
                skill_score,
                proj_score,
                exp_score,
                struct_score,
                density_score,
                impact_score,
                bullet_score
            ]
            values.append(values[0])
            angles = np.linspace(0, 2 * np.pi, len(values), endpoint=False).tolist()
            fig = plt.figure(figsize=(3,3))
            ax = plt.subplot(111, polar=True)
            ax.plot(angles, values)
            ax.fill(angles, values, alpha=0.25)
            ax.set_ylim(0,100)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)
            st.pyplot(fig)

        st.markdown("---")

        # Detection and Statistics side by side
        col1, col2 = st.columns(2)

        # -------- Resume Section Detection -------- #
        with col1:

            detect_html = """
            <div class="section-card" style="height:100%">
            <div class="section-header">
            Resume Section Detection
            </div>
            """

            for sec in sections_detected:

                if sections_detected[sec]:
                    detect_html += f"✓ {sec.capitalize()}<br>"
                else:
                    detect_html += f"✗ {sec.capitalize()}<br>"

            detect_html += "</div>"

            st.markdown(detect_html, unsafe_allow_html=True)


        # -------- Resume Statistics -------- #
        with col2:

            stats_html = f"""
            <div class="section-card" style="height:100%">

            <div class="section-header">
            Resume Statistics
            </div>

            <div style="
                display:grid;
                grid-template-columns:1fr 1fr;
                gap:10px;
                justify-items:center;
                align-items:center;
            ">

            <div>
            <div class="stat-ball">{achievement_count}</div>
            <div class="stat-label">Achievements</div>
            </div>

            <div>
            <div class="stat-ball">{bullet_count}</div>
            <div class="stat-label">Bullets</div>
            </div>

            <div>
            <div class="stat-ball">{len(found_skills)}</div>
            <div class="stat-label">Skills</div>
            </div>

            <div>
            <div class="stat-ball">{len(missing)}</div>
            <div class="stat-label">Missing</div>
            </div>

            </div>
            </div>
            """

            st.markdown(stats_html, unsafe_allow_html=True)
        # -------- Resume Suggestions (Below) -------- #

        suggest_html = """
        <div class="section-card">

        <div class="section-header">
        Resume Suggestions
        </div>
        """

        if len(suggestions) > 0:

            for s in suggestions:
                suggest_html += f"🧠 {s}<br><br>"

        else:
            suggest_html += "No suggestions detected."

        suggest_html += "</div>"

        st.markdown(suggest_html, unsafe_allow_html=True)
        
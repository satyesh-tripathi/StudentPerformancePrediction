# Student Performance Prediction System 🎓

**AIML Summer Internship 2026 Capstone Project**  
**Institution:** IIHMF, MNNIT Allahabad, Prayagraj

## 🌐 Live Demonstration
**[Access the Live Web Application](https://studentperformanceprediction-kbnar9atvbm9bfjbzrzrsa.streamlit.app/)**

## 📌 Project Overview
This system is an end-to-end Machine Learning pipeline developed to predict student final exam grades (G3) using behavioral and demographic indicators. By deliberately excluding prior-period grades (G1/G2), this system acts as an early-intervention tool to help educators identify at-risk students before final exams occur.

📂 Project Structure
As mandated by the capstone submission guidelines, the project is structured as follows:

Dataset/: Contains student-mat.csv and processed modeling data.

Model/: Stores the persisted student_performance_best_model.pkl pipeline.

src/: Contains modular scripts for data cleaning, engineering, and tuning.

Streamlit_App/: Contains the live web interface code.

Documentation/: Contains project management logs, the formal Project Report (PDF), and the Presentation Deck (PPT).

📑 Project Deliverables
Formal Report: Located in Documentation/Project_Report.pdf.

Defense Presentation: Located in Documentation/Presentation_Deck.pdf.

Engineering Logs: Please refer to the Documentation/ folder for decision.md (Engineering Log) and task.md (Project Tracker).

## 🚀 How to Run
1. Install requirements: pip install -r Streamlit_App/requirements.txt
2. Launch the app: streamlit run Streamlit_App/app.py
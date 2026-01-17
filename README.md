# TOPSIS Decision Support System

This project implements the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method as a complete decision-support system.

## Methodology
┌───────────────┐   ┌──────────────────┐   ┌──────────────────────┐   ┌───────────────────────┐   ┌────────────────────┐   ┌───────────────────────┐
│  Data Input   │ → │ Data Validation  │ → │ Normalization &      │ → │ Ideal Solution        │ → │ Distance & TOPSIS  │ → │ Ranking & Result      │
│  (CSV File)   │   │ (Numeric, Weights│   │ Weight Application   │   │ Determination         │   │ Score Calculation  │   │ Generation            │
│               │   │ & Impacts Check) │   │                      │   │ (Best & Worst)        │   │                    │   │ (Table & Graph)       │
└───────────────┘   └──────────────────┘   └──────────────────────┘   └───────────────────────┘   └────────────────────┘   └───────────────────────┘


The project is divided into three parts:

## 1. Command Line Application
- Accepts CSV input file
- Takes weights and impacts as command-line arguments
- Generates TOPSIS score and rank in CSV format

## 2. Python Package
- TOPSIS logic packaged and uploaded to PyPI
- Installable using pip
- Executable from the command line

🔗 PyPI Link:  
https://pypi.org/project/topsis-yashika-102303439/

## 3. Web Application
- Built using Flask
- Allows CSV upload, weights, impacts, and email input
- Automatically emails the result file to the user
- Deployed on Render cloud platform

🌐 Live Web App:  
https://topsis-9cec.onrender.com

## 4. User Interface 
<img width="100" height="300" alt="image" src="https://github.com/user-attachments/assets/ec2eb319-41a6-4c2f-bcec-5695c01b98a8" />

## Technologies Used
Python, Flask, Pandas, NumPy, HTML, CSS, SMTP(Simple Mail Tranfer Protocol), GitHub, Render

## Author
Yashika

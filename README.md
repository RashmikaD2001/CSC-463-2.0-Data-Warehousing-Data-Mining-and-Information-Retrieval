# ✈️ Airline Passenger Satisfaction Prediction – Machine Learning & Data Analytics

This project analyzes airline passenger satisfaction using **data mining**, **machine learning**, and **optimization techniques**.  
It includes a complete pipeline from **data cleaning** and **feature engineering** to **predictive modeling**, **visual analytics**, and **budget-based satisfaction optimization**.

Dataset - [Airline Customer Satisfaction](https://www.kaggle.com/datasets/raminhuseyn/airline-customer-satisfaction)
---

## 🚀 Project Overview

The goal of this project is to uncover key factors that influence passenger satisfaction and use machine learning to predict it.  
Additionally, an **optimization model (PuLP)** is applied to enhance satisfaction under budget constraints.

The project also features an **interactive dashboard** built with **Dash and Plotly** for dynamic data exploration and insight visualization.

---

## 🧠 Key Features

- **Data Cleaning & Preprocessing:**  
  Handled missing values, encoded categorical variables, and binned continuous features for analysis.

- **Exploratory Data Analysis (EDA):**  
  Visualized demographic and service-related patterns using Plotly and Dash components.

- **Machine Learning Modeling:**  
  Built and evaluated classification models (Logistic Regression, Random Forest, Decision Tree) using Scikit-learn to predict satisfaction.

- **Optimization with PuLP:**  
  Developed a linear programming model to maximize satisfaction scores while maintaining budget efficiency.

- **Interactive Dashboard:**  
  A Dash-based web app that visualizes:
  - Customer demographics  
  - Quantitative feature distributions  
  - Feature relationships and comparisons  
  - Satisfaction metrics and trends

---

## 🧩 Tech Stack

| Category | Tools / Libraries |
|-----------|------------------|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Optimization | PuLP |
| Visualization | Plotly, Dash, Dash Bootstrap Components |
| Notebook Analysis | Jupyter Notebook |
| Data Storage | CSV (cleaned dataset) |

---

## 📊 Dashboard Highlights

The **Airline Passenger Satisfaction Dashboard** allows interactive exploration of:
- Satisfaction levels by demographics and class  
- Delay times, travel types, and their impact on satisfaction  
- Quantitative and qualitative feature relationships  
- Model outcomes and derived insights  

---

## 🧮 Optimization Model (PuLP)

A linear optimization problem is formulated as:

**Objective:**  
Maximize total passenger satisfaction score  

**Subject to:**  
- Total improvement cost ≤ available budget  
- Service-level constraints (e.g., staff, equipment, upgrades)

Implemented using the **PuLP** library to determine the most efficient allocation of resources that improves satisfaction within budget limits.

---

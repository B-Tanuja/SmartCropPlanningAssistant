# 🌱 Smart Crop Planning Assistant

A web-based agriculture application that helps farmers choose a suitable crop based on their land and farming conditions.

## 📌 Project Overview

The Smart Crop Planning Assistant provides crop recommendations using farmer-provided information such as:

- Land area
- Soil type
- Season
- Available water
- Farming budget

The system evaluates available crops using a suitability score and provides additional information such as estimated cultivation cost, expected revenue, estimated profit, cultivation timeline, and fertilizer suggestions.

## 🎯 Objectives

- Help farmers make better crop-planning decisions
- Recommend suitable crops based on farming conditions
- Estimate cultivation cost and possible profit
- Provide a simple cultivation timeline
- Provide basic fertilizer information
- Generate a downloadable crop planning report

## ✨ Features

### 🌱 Crop Recommendation
Recommends suitable crops based on:
- Soil type
- Season
- Water availability
- Budget

### 🏆 Best Crop Selection
The crop with the highest suitability score is displayed as the best recommendation.

### 💰 Cost Estimation
Calculates estimated cultivation cost based on:

Land Area × Budget Per Acre

### 📈 Revenue & Profit Estimation
The system estimates expected revenue and profit using crop yield, land area, and market price information.

### 📅 Cultivation Timeline
Displays important cultivation activities according to crop growth stages.

### 🌿 Fertilizer Recommendation
Provides basic nutrient requirements and fertilizer application timing for supported crops.

### 📄 PDF Report
Generates a downloadable report containing farmer inputs, crop recommendation, cost, revenue, profit, timeline, and fertilizer information.

## 🛠️ Technologies Used

- Python
- Flask
- Pandas
- HTML
- CSS
- ReportLab
- CSV Dataset

## 📂 Project Structure

```text
SmartCropPlanningAssistant/
│
├── app.py
├── requirements.txt
├── README.md
│
├── dataset/
│   └── crop_dataset.csv
│
├── templates/
│   ├── index.html
│   └── result.html
│
└── static/
    └── style.css
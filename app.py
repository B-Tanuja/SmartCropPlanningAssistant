from flask import Flask, render_template, request, send_file
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
app = Flask(__name__)
# Cultivation timelines for different crops
cultivation_timelines = {
    "Rice": [
        ("Day 1", "🌱 Seed Sowing"),
        ("Day 20", "💧 First Irrigation"),
        ("Day 35", "🌿 Weed Management"),
        ("Day 50", "🌱 Fertilizer Application"),
        ("Day 75", "🌾 Crop Growth Monitoring"),
        ("Day 120", "🌾 Harvest")
    ],

    "Maize": [
        ("Day 1", "🌱 Seed Sowing"),
        ("Day 15", "💧 Irrigation"),
        ("Day 30", "🌿 Weed Management"),
        ("Day 45", "🌱 Fertilizer Application"),
        ("Day 70", "🌽 Crop Development"),
        ("Day 100", "🌾 Harvest")
    ],

    "Groundnut": [
        ("Day 1", "🌱 Seed Sowing"),
        ("Day 20", "💧 First Irrigation"),
        ("Day 35", "🌿 Weed Management"),
        ("Day 60", "🌱 Fertilizer Application"),
        ("Day 90", "🌼 Flowering"),
        ("Day 110", "🌾 Harvest")
    ],

    "Green Gram": [
        ("Day 1", "🌱 Seed Sowing"),
        ("Day 15", "💧 Irrigation"),
        ("Day 25", "🌿 Weed Management"),
        ("Day 40", "🌼 Flowering"),
        ("Day 55", "🌱 Pod Development"),
        ("Day 70", "🌾 Harvest")
    ],

    "Black Gram": [
        ("Day 1", "🌱 Seed Sowing"),
        ("Day 15", "💧 Irrigation"),
        ("Day 25", "🌿 Weed Management"),
        ("Day 40", "🌼 Flowering"),
        ("Day 55", "🌱 Pod Development"),
        ("Day 70", "🌾 Harvest")
    ]
}
# Fertilizer suggestions for crops
fertilizer_data = {
    "Rice": {
        "nutrients": ["Nitrogen", "Phosphorus", "Potassium"],
        "fertilizers": [
            ("Day 1", "DAP"),
            ("Day 25", "Urea"),
            ("Day 50", "Potash")
        ]
    },

    "Maize": {
        "nutrients": ["Nitrogen", "Phosphorus", "Potassium"],
        "fertilizers": [
            ("Day 1", "DAP"),
            ("Day 25", "Urea"),
            ("Day 45", "Potash")
        ]
    },

    "Groundnut": {
        "nutrients": ["Phosphorus", "Calcium", "Potassium"],
        "fertilizers": [
            ("Day 1", "DAP"),
            ("Day 30", "Gypsum"),
            ("Day 60", "Potash")
        ]
    },

    "Green Gram": {
        "nutrients": ["Phosphorus", "Potassium"],
        "fertilizers": [
            ("Day 1", "DAP"),
            ("Day 30", "Potash")
        ]
    },

    "Black Gram": {
        "nutrients": ["Phosphorus", "Potassium"],
        "fertilizers": [
            ("Day 1", "DAP"),
            ("Day 30", "Potash")
        ]
    }
}

# Load crop dataset
df = pd.read_csv("dataset/crop_dataset_expanded.csv")


@app.route('/')
def home():
    return render_template('index.html')
@app.route('/download_report', methods=['POST'])
def download_report():

    crop_name = request.form['crop_name']
    land_area = float(request.form['land_area'])
    soil_type = request.form['soil_type']
    season = request.form['season']
    water_level = request.form['water_level']
    budget = float(request.form['budget'])

    total_cost = float(request.form['total_cost'])
    expected_revenue = float(request.form['expected_revenue'])
    estimated_profit = float(request.form['estimated_profit'])
    score = float(request.form['score'])

    # Get timeline and fertilizer information
    timeline = cultivation_timelines.get(crop_name, [])

    fertilizer_info = fertilizer_data.get(
        crop_name,
        {
            "nutrients": [],
            "fertilizers": []
        }
    )

    pdf_path = "crop_planning_report.pdf"

    pdf = canvas.Canvas(pdf_path, pagesize=A4)

    width, height = A4
    y = height - 50

    # Title
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "Smart Crop Planning Report")

    y -= 40

    # Farmer Inputs
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Farmer Inputs")

    y -= 25
    pdf.setFont("Helvetica", 11)

    inputs = [
        f"Land Area: {land_area} Acres",
        f"Soil Type: {soil_type}",
        f"Season: {season}",
        f"Water Level: {water_level}",
        f"Budget: Rs. {budget:,.0f}"
    ]

    for item in inputs:
        pdf.drawString(60, y, item)
        y -= 20

    # Best Crop
    y -= 15
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Best Recommended Crop")

    y -= 25
    pdf.setFont("Helvetica", 11)

    crop_details = [
        f"Crop: {crop_name}",
        f"Suitability Score: {score:.0f}%",
        f"Total Cost: Rs. {total_cost:,.0f}",
        f"Expected Revenue: Rs. {expected_revenue:,.0f}",
        f"Estimated Profit: Rs. {estimated_profit:,.0f}"
    ]

    for item in crop_details:
        pdf.drawString(60, y, item)
        y -= 20

    # Cultivation Timeline
    y -= 15
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Cultivation Timeline")

    y -= 25
    pdf.setFont("Helvetica", 11)

    if timeline:
        for day, activity in timeline:
            pdf.drawString(60, y, f"{day} - {activity}")
            y -= 20

            # New page if required
            if y < 70:
                pdf.showPage()
                y = height - 50
                pdf.setFont("Helvetica", 11)

    else:
        pdf.drawString(
            60,
            y,
            "No cultivation timeline available."
        )
        y -= 20

    # Fertilizer Recommendation
    y -= 15

    if y < 150:
        pdf.showPage()
        y = height - 50

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Fertilizer Recommendation")

    y -= 25

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(60, y, "Recommended Nutrients:")

    y -= 20
    pdf.setFont("Helvetica", 11)

    if fertilizer_info["nutrients"]:

        for nutrient in fertilizer_info["nutrients"]:
            pdf.drawString(70, y, f"- {nutrient}")
            y -= 20

    else:
        pdf.drawString(
            70,
            y,
            "No nutrient information available."
        )
        y -= 20

    y -= 10

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(60, y, "Application Schedule:")

    y -= 20
    pdf.setFont("Helvetica", 11)

    if fertilizer_info["fertilizers"]:

        for day, fertilizer in fertilizer_info["fertilizers"]:
            pdf.drawString(
                70,
                y,
                f"{day} - {fertilizer}"
            )
            y -= 20

            if y < 70:
                pdf.showPage()
                y = height - 50
                pdf.setFont("Helvetica", 11)

    else:
        pdf.drawString(
            70,
            y,
            "No fertilizer information available."
        )
        y -= 20

    # Note
    y -= 20

    if y < 60:
        pdf.showPage()
        y = height - 50

    pdf.setFont("Helvetica-Oblique", 9)

    pdf.drawString(
        50,
        y,
        "Note: Fertilizer recommendations are general"
    )

    y -= 15

    pdf.drawString(
        50,
        y,
        "and should be adjusted based on soil testing"
    )

    y -= 15

    pdf.drawString(
        50,
        y,
        "and local agricultural guidance."
    )

    pdf.save()

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="Smart_Crop_Planning_Report.pdf"
    )

@app.route('/recommend', methods=['POST'])
def recommend():

    # Get values from farmer form
    land_area = float(request.form['land_area'])
    soil_type = request.form['soil_type']
    season = request.form['season']
    water_level = request.form['water_level']
    budget = float(request.form['budget'])

    # Create a copy of dataset
    results = df.copy()

    # Calculate suitability score
    results['Score'] = 0

    # Soil match
    results.loc[
        results['Soil_Type'] == soil_type,
        'Score'
    ] += 30

    # Season match
    results.loc[
        results['Season'] == season,
        'Score'
    ] += 30

    # Water match
    results.loc[
        results['Water_Level'] == water_level,
        'Score'
    ] += 20

    # Total cultivation cost
    results['Total_Cost'] = results['Budget_Per_Acre'] * land_area

    # Budget check
    results.loc[
        results['Total_Cost'] <= budget,
        'Score'
    ] += 20
    

    # Expected Revenue
    results['Expected_Revenue'] = (
        results['Expected_Yield_Kg'] *
        land_area *
        results['Market_Price_Per_Kg']
    )

    # Estimated Profit
    results['Estimated_Profit'] = (
        results['Expected_Revenue'] -
        results['Total_Cost']
    )
    # Sort by suitability score first,
# then by expected yield if scores are equal
    results = results.sort_values(
        by=['Score', 'Expected_Yield_Kg'],
        ascending=[False, False]
    )

    # Sort by score
    
    # Generate recommendation reasons
    reasons = []

    for _, crop in results.iterrows():

        crop_reasons = []

        if crop['Soil_Type'] == soil_type:
            crop_reasons.append("Soil type matches")

        if crop['Season'] == season:
            crop_reasons.append("Season matches")

        if crop['Water_Level'] == water_level:
            crop_reasons.append("Water availability matches")

        if crop['Total_Cost'] <= budget:
            crop_reasons.append("Fits within your budget")

        reasons.append(crop_reasons)

    results['Reasons'] = reasons

    # Get top 3 crops
    best_crop = results.iloc[0].to_dict()
    top_crops = results.head(3).to_dict('records')
        # Get best crop and top 3 crops
    best_crop = results.iloc[0].to_dict()
    top_crops = results.head(3).to_dict('records')

    # Get cultivation timeline for the best crop
    best_crop_name = best_crop['Crop']

    timeline = cultivation_timelines.get(
        best_crop_name,
        []
    )
    fertilizer_info = fertilizer_data.get(
        best_crop_name,
    {
        "nutrients": [],
        "fertilizers": []
    }
)

    return render_template(
    'result.html',
    crops=top_crops,
    best_crop=best_crop,
    land_area=land_area,
    budget=budget,
    timeline=timeline,
    fertilizer_info=fertilizer_info
)


if __name__ == '__main__':
    app.run(debug=True)
    # Get cultivation timeline for the best crop

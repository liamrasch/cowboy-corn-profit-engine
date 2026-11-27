# Cowboy Corn Profit Engine 🌽📊

A Python data-analysis tool built to evaluate event unit economics, identify break-even thresholds, and eliminate unprofitable bookings for **Muther Shuckers Cowboy Corn**.

## 🎯 The Business Problem
Mobile event food operations often generate strong profits at peak festivals while losing money at slow local events due to fixed vendor fees, labor, and prep overhead. This engine analyzes historical event performance to separate high-margin venues from money-losing bookings.

## 📐 Core Unit Economics Formula
- **Gross Revenue** = `Ears Sold × Price Per Ear` + `Add-On Sales (Drinks/Toppings)`
- **Total Costs** = `Vendor/Booth Fee` + `COGS (Corn, Butter, Seasoning, Supplies)` + `Labor Cost` + `Travel/Fuel`
- **Net Profit** = `Gross Revenue - Total Costs`
- **Break-Even Volume** = `Fixed Costs (Fee + Labor + Travel) ÷ Contribution Margin Per Ear`

## 🚀 Roadmap
- [x] V1: Core unit-economics calculator & event profitability ranker (`analyzer.py`)
- [x] V2: CSV ingestion from real historical Florida & Texas event logs
- [x] V3: Weather forecast & local festival attendance scoring predictor

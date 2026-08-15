# Inflationary Impact on Retail Consumer Basket Composition

**Student name:** [Enter your name]  
**Register number:** [Enter your register number]  
**Course:** Python Bootcamp Project  
**Date:** [Enter date]

## Abstract

This project examines whether consumer spending moves away from discretionary purchases toward necessities during high inflation. The analysis combines annual U.S. CPI-U inflation with Consumer Expenditure Survey data from 2020–2023. Using Python libraries pandas, NumPy, Matplotlib, and Seaborn, the project calculates necessity spending, luxury/discretionary spending, their shares of total expenditure, and the luxury-to-necessity ratio. A 4.5% annual inflation threshold is used to compare high- and lower-inflation years. The results are descriptive and do not establish causation.

## 1. Introduction

Inflation increases the prices paid by consumers. However, consumers may not change all purchases in the same way. They may prioritise essential goods and services such as food, housing, transport, and healthcare while reducing discretionary spending. This project investigates whether such a shift is visible in a small public dataset.

**Research question:** How does the luxury-to-necessity spending ratio change when annual inflation crosses 4.5%?

## 2. Dataset and sources

The dataset includes annual figures for all U.S. consumer units from 2020–2023. Consumer spending values were taken from the U.S. Bureau of Labor Statistics Consumer Expenditure Survey, and inflation data is annual CPI-U inflation from the BLS.

Data sources:

- BLS Consumer Expenditures in 2023
- BLS Consumer Price Index (CPI-U) data

All expenditure values are nominal annual U.S. dollars per consumer unit.

## 3. Tools and libraries

- **pandas** was used to read and manage the CSV data.
- **NumPy** was used to calculate totals and ratios.
- **Matplotlib** was used to create and save graphs.
- **Seaborn** was used to style charts and create the comparison plots.

## 4. Definitions and method

For this project, necessities are food at home, housing, transportation, and healthcare. The luxury/discretionary proxy includes food away from home, alcoholic beverages, apparel and services, entertainment, personal care, and reading.

The high-inflation threshold is 4.5%. The program calculates the following measures for each year:

1. Total necessity spending.
2. Total luxury/discretionary spending.
3. Necessity and luxury shares of total expenditure.
4. Luxury-to-necessity ratio.

The analysis then compares the average results for high-inflation and lower-inflation years.

## 5. Results

Insert the generated figures below.

### Figure 1: Inflation threshold

Insert `figures/01_inflation_threshold.png` here.

### Figure 2: Basket shares over time

Insert `figures/02_basket_shares_over_time.png` here.

### Figure 3: Threshold comparison

Insert `figures/03_threshold_comparison.png` here.

The program found that the average luxury-to-necessity ratio was approximately **0.221** in high-inflation years and **0.207** in lower-inflation years. The difference is small. Therefore, this dataset does not show a strong shift away from the defined discretionary basket once inflation crosses the selected threshold.

## 6. Discussion

The result should be interpreted carefully. An increase in nominal expenditure can result from higher prices instead of consumers purchasing more goods or services. The period also includes the COVID-19 pandemic, which affected restaurant, travel, and transportation spending. Therefore, the analysis demonstrates an observed pattern, not proof that inflation caused the change.

## 7. Limitations and future scope

This project uses only four annual observations and national averages. The definitions of luxury and necessity are assumptions and can vary by income, family size, and location. Future work could use a longer time period, analyse consumer income quintiles, adjust spending for inflation, and build regression or time-series forecasting models.

## 8. Conclusion

This project successfully connects a macroeconomic measure, CPI-U inflation, with household expenditure categories. It provides a reproducible Python workflow and shows how consumer-basket composition can be measured and compared across inflation regimes.

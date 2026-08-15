# Inflationary Impact on Retail Consumer Basket Composition

## Project overview

This Python project studies how a household's spending basket changes when inflation is high. It compares spending on a defined group of **necessities** with spending on a defined **luxury/discretionary proxy** using annual U.S. Consumer Expenditure Survey data from 2020–2023.

## Research question

**How does the luxury-to-necessity spending ratio change when annual inflation crosses 4.5%?**

## Dataset

The project uses the CSV file `data/consumer_basket_2020_2023.csv`. It contains annual U.S. consumer-unit spending and CPI-U inflation data for 2020–2023.

Sources:

- [U.S. Bureau of Labor Statistics, Consumer Expenditures in 2023](https://www.bls.gov/opub/reports/consumer-expenditures/2023/home.htm)
- [U.S. Bureau of Labor Statistics, CPI data](https://www.bls.gov/cpi/data.htm)

All expenditure values are nominal annual U.S. dollars per consumer unit.

## Project definitions

The categories below are project assumptions, not official BLS classifications.

| Basket | Categories included |
|---|---|
| Necessities | food at home, housing, transportation, healthcare |
| Luxury/discretionary proxy | food away from home, alcohol, apparel and services, entertainment, personal care, reading |

The threshold for high inflation is **4.5%** annual CPI-U inflation. The code labels 2021 and 2022 as high-inflation years; 2020 and 2023 are lower-inflation years.

## Libraries used

- **pandas**: reads, organises, and exports tabular data.
- **NumPy**: calculates totals, percentages, and ratios.
- **Matplotlib**: saves figures as PNG files.
- **Seaborn**: creates visually clear, styled charts.

## How to run

1. Open a terminal in this project folder.
2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Run the program:

   ```bash
   python analysis.py
   ```

## Output files

After running the program, these files are created:

- `results_summary.csv`: original data plus calculated spending measures.
- `figures/01_inflation_threshold.png`: annual inflation and the 4.5% threshold.
- `figures/02_basket_shares_over_time.png`: necessity and luxury/discretionary shares over time.
- `figures/03_threshold_comparison.png`: average basket shares for the two inflation groups.

The full table is also printed in the terminal, and the charts open on screen.

## Method

For each year, the program calculates:

```text
necessity spending = sum of necessity categories
luxury spending = sum of luxury/discretionary categories
necessity share = necessity spending / total spending × 100
luxury share = luxury spending / total spending × 100
luxury-to-necessity ratio = luxury spending / necessity spending
```

It then compares the average ratio in years below the threshold with the average ratio in years at or above the threshold.

## Main result

The average luxury-to-necessity ratio was approximately **0.221** in high-inflation years and **0.207** in lower-inflation years. In this short national dataset, the defined discretionary basket did not show a large decline during high inflation.

## Limitations

- Only four annual observations are available, so this is descriptive rather than a strong statistical test.
- The period includes the COVID-19 shock, which affected transport and dining-out spending.
- Nominal expenditure can increase because prices increase, not necessarily because households buy more.
- “Luxury” and “necessity” vary across households.

## Future scope

A stronger future study could use a longer time series, BLS public-use microdata, inflation-adjusted spending, income quintiles, and regression or time-series methods.

# LogiSight-360-- description 
An interactive Streamlit dashboard for analyzing last-mile delivery data, identifying delivery delays, and comparing vehicle, agent, area, and product category performance using Python, Pandas, and Plotly.



# LogiSight 360: Analysing Last-Mile Delivery Data for Performance Insights

## 1. Project Overview

LogiSight 360 is an interactive data analytics dashboard developed using Python and Streamlit for Formative Assessment 2 (FA-2) of Mathematics for AI-II under the Artificial Intelligence Career-related Programme.

The project focuses on analysing last-mile delivery data to understand delivery performance and explore how weather conditions, traffic levels, vehicle types, delivery areas, delivery agents, and product categories relate to delivery times.

The dashboard transforms raw delivery records into meaningful statistical summaries and interactive visualisations. It enables users to filter the dataset and explore delivery patterns to support data-driven operational decisions.

## 2. Project Objectives

The main objectives of this project are to:

- Load, inspect, clean, and prepare real-world delivery data using Python.
- Handle missing values and prepare relevant columns for analysis.
- Calculate average delivery time and the percentage of late deliveries.
- Group delivery records by relevant operational factors.
- Create the five compulsory visualisations specified in the FA-2 assignment.
- Develop an interactive Streamlit dashboard with filters that update visualisations dynamically.
- Present delivery insights through a clear and user-friendly interface.

## 3. Dataset Description

The project uses the dataset `Last mile Delivery Data.csv`.

The dataset contains information about delivery orders, delivery agents, environmental conditions, vehicles, geographical areas, delivery times, and product categories.

Important columns used in the analysis include:

| Column | Purpose |
|---|---|
| `Order_ID` | Identifies delivery orders |
| `Agent_Age` | Supports analysis by delivery agent age group |
| `Agent_Rating` | Used to explore agent ratings |
| `Order_Date` | Supports date-based filtering and trend analysis |
| `Weather` | Used to compare weather conditions |
| `Traffic` | Used to compare traffic conditions |
| `Vehicle` | Used to compare vehicle performance |
| `Area` | Used for area-based delivery analysis |
| `Delivery_Time` | Main numerical variable for performance analysis |
| `Category` | Used to compare product category delivery times |

Other available columns include store and drop-off coordinates, order time, and pickup time.

## 4. Data Cleaning and Preparation

The application uses Pandas to load and prepare the dataset before visualisation.

The implemented preparation steps include:

- Reading the CSV file and removing unnecessary whitespace from column names.
- Checking that required columns are present.
- Converting relevant numerical columns to numeric data types.
- Converting order dates to a datetime format.
- Removing leading and trailing whitespace from categorical values.
- Replacing missing weather values with the category `Unknown`.
- Inspecting missing values and duplicate records in the Data Explorer.

Other missing numerical and categorical values are reported for inspection rather than automatically replaced.

The prepared data is grouped by weather, traffic, vehicle, area, and product category to support the required visualisations.

## 5. Calculation of Late Deliveries

The assignment defines late deliveries using the mean delivery time plus one standard deviation.

The threshold is calculated as:

`Late-delivery threshold = Mean delivery time + Standard deviation`

A delivery is classified as late when:

`Delivery_Time > Late-delivery threshold`

The late-delivery percentage is calculated as:

`Late-delivery percentage = (Number of late deliveries / Number of valid deliveries analysed) × 100`

The application calculates the threshold from the full dataset and uses it to identify late deliveries within the selected records.

## 6. Required Visualisations

The dashboard implements the five compulsory visualisations specified in the FA-2 assignment.

### 6.1 Delay Analyzer — Bar Chart

**Variables:** `Delivery_Time`, `Weather`, `Traffic`

This bar chart compares average delivery time across different combinations of weather and traffic conditions.

It helps users identify environmental and traffic combinations associated with longer delivery times.

### 6.2 Vehicle Comparison — Bar Chart

**Variables:** `Delivery_Time`, `Vehicle`

This chart compares average delivery time across the available vehicle types.

The comparison helps users explore differences in delivery performance between vehicles. Summary statistics and record counts provide additional context.

### 6.3 Agent Performance — Scatter Plot

**Variables:** `Agent_Rating`, `Delivery_Time`, `Agent_Age`

The scatter plot displays agent rating on the x-axis and delivery time on the y-axis. Points are coloured by agent age group:

- Under 25
- 25–40
- Over 40

This visualisation helps explore relationships between agent ratings, age groups, and delivery times. The observed associations do not establish causation.

### 6.4 Area Heatmap

**Variables:** `Delivery_Time`, `Area`

The area heatmap compares average delivery time across geographical area classifications and traffic conditions.

It helps users identify area and traffic combinations that may require further investigation.

### 6.5 Category Visualizer — Box Plot

**Variables:** `Delivery_Time`, `Category`

The box plot compares delivery-time distributions across product categories. It allows users to examine medians, variability, and potential outliers.

This can help identify categories with different delivery-time patterns.

## 7. Additional Visualisations

In addition to the five compulsory visualisations, the dashboard includes:

- Daily order-volume trend.
- Average delivery time by area.
- Weather and traffic heatmap.
- Vehicle performance comparison.
- Average delivery time by agent age group.
- Summary tables for delivery performance.

These additional visuals provide further context for exploring the dataset.

## 8. Streamlit Interface and Interactivity

The dashboard is developed using Streamlit and includes sidebar navigation, KPI cards, filters, interactive charts, and a Data Explorer.

Users can filter records by:

- Order date range.
- Weather.
- Traffic.
- Vehicle type.
- Delivery area.
- Product category.
- Agent age range.
- Agent rating range.
- Order ID search.

The charts and summary metrics update according to the selected filters.

The dashboard contains the following sections:

1. Dashboard
2. Delay Analysis
3. Vehicle Performance
4. Agent Performance
5. Area Insights
6. Category Analysis
7. Data Explorer

The Data Explorer allows users to inspect filtered records, review missing values and column data types, check duplicate rows, and download filtered or full dataset records as CSV files.

## 9. Technologies Used

- **Python:** Application logic and data processing.
- **Pandas:** Data loading, cleaning, grouping, and statistical summaries.
- **Streamlit:** Dashboard interface, navigation, and interactive filters.
- **Plotly Express:** Interactive charts and visualisations.
- **Plotly Graph Objects:** Custom delivery trend visualisation.
- **GitHub:** Source code repository and version control.
- **Streamlit Community Cloud:** Hosting and deployment of the dashboard.

## 10. Project Structure

The project repository is organised as follows:

```text
LogiSight-360/
|
|-- app.py
|-- requirements.txt
|-- Last mile Delivery Data.csv
|-- README.md
```

The dataset must be accessible at the location expected by the application code.

## 11. Installation and Execution

### Prerequisites

- Python installed on the computer.
- The project files downloaded or cloned from GitHub.
- Required Python libraries installed.

### Step 1: Clone the Repository

Replace `YOUR_USERNAME` with the relevant GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/LogiSight-360.git
cd LogiSight-360
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Dashboard

```bash
python -m streamlit run app.py
```

Streamlit will provide a local address that can be opened in a web browser.

## 12. Requirements File

The `requirements.txt` file should contain the core libraries used by the application:

```text
streamlit
pandas
plotly
```

For reproducibility, compatible package versions can be specified after testing the application in the intended environment.

## 13. GitHub and Streamlit Cloud Deployment

The assignment requires the final dashboard to be hosted on Streamlit Community Cloud and supported by a GitHub repository.

Deployment procedure:

1. Create a GitHub repository named `LogiSight-360`.
2. Upload `app.py`, `requirements.txt`, the required dataset where permitted, and this README.
3. Confirm that the repository contains the correct final application code.
4. Sign in to Streamlit Community Cloud using the connected GitHub account.
5. Create a new application using the repository, branch, and `app.py` file path.
6. Deploy the application.
7. Test the deployed dashboard, including the dataset loading, visualisations, filters, and downloads.
8. Record the public dashboard URL for submission.

The dataset must be available to the deployed application. If it cannot be shared publicly, an appropriate permitted data-hosting approach must be used.

## 14. Expected Outcomes

The project provides an interactive way to explore last-mile delivery performance and identify patterns in the available data.

The expected outcomes include:

- Comparing average delivery times across vehicle types.
- Exploring delivery-time patterns under different weather and traffic conditions.
- Examining relationships between agent ratings, age groups, and delivery times.
- Comparing delivery-time distributions across product categories.
- Identifying deliveries classified as late under the assignment's statistical definition.
- Exploring area-based delivery performance.
- Inspecting data quality and exporting records for further analysis.

The findings can support further investigation and operational decision-making, while recognising that observed patterns alone do not prove causal relationships.

## 15. Academic Context

**Course:** Mathematics for AI-II  
**Programme:** Artificial Intelligence Career-related Programme  
**Assessment:** Formative Assessment 2 (FA-2)  
**Assignment:** Analysing Last-Mile Delivery Data for Performance Insights

This project addresses the assignment's three main assessment areas:

1. Data cleaning and preparation.
2. Implementation of the five compulsory visualisations.
3. Streamlit interface, interactivity, and deployment.

The final assessment depends on the application running correctly, the visualisations being clear and accurate, and the deployment requirements being fulfilled.

## Author

Developed as part of the Mathematics for AI-II Formative Assessment 2 project.

**Project name:** LogiSight 360  
**Project focus:** Last-mile delivery data analysis and performance insights

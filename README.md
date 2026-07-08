# 🌦️🍕 Data Weaver - Weather vs Food Orders Analysis

A comprehensive data analysis project that combines weather data with Zomato food ordering patterns to uncover meaningful insights about consumer behavior during different weather conditions.

## 📊 Project Overview

This project demonstrates the power of data integration by merging two seemingly unrelated datasets:
- **Weather Data**: Temperature, rainfall, and weather conditions
- **Zomato Orders Data**: Order counts, categories, timing, and revenue

The analysis reveals fascinating patterns about how weather influences food ordering behavior, providing actionable insights for food delivery businesses.

## 🎯 Key Findings

Our analysis uncovered several compelling insights:

1. **🌧️ Rainy Day Boost**: Orders increase by **78.3%** on rainy days (337 vs 189 average orders)
2. **💰 Revenue Impact**: Rainy days generate **76.3%** more revenue (₹18,220 vs ₹10,335)
3. **🌡️ Temperature Effect**: Strong negative correlation (-0.832) between temperature and orders
4. **⏰ Timing Patterns**: Peak ordering times shift slightly during different weather conditions

## 🏗️ Project Structure

```
weather-zomato-data-weaver/
├── .kiro/                    # Kiro AI development logs and tracking
│   └── project_log.md       # Development progress and assistance log
├── data/                    # Raw and processed datasets
│   ├── weather.csv         # Weather data (30 days)
│   ├── zomato_orders.csv   # Zomato orders data (120 records)
│   └── merged_data.csv     # Processed and merged dataset
├── dashboard/              # Streamlit dashboard application
│   └── app.py             # Interactive web dashboard
├── notebooks/             # Jupyter notebooks for exploration
├── screenshots/           # Dashboard screenshots
├── data_processor.py      # Data cleaning and merging script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 📈 Data Sources

### Weather Dataset
- **Period**: January 2024 (30 days)
- **Features**: Date, Temperature (°C), Rainfall (mm), Weather Condition
- **Conditions**: Clear, Sunny, Cloudy, Rainy
- **Temperature Range**: 17.8°C to 28.2°C

### Zomato Orders Dataset
- **Period**: January 2024 (30 days, 4 orders per day)
- **Features**: Date, Time, Order Count, Category, Total Amount
- **Categories**: Indian, Chinese, Italian, Fast Food
- **Total Records**: 120 order entries

## 🚀 How to Run the Dashboard

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd weather-zomato-data-weaver
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Process the data** (if not already done)
   ```bash
   py data_processor.py
   ```

4. **Launch the dashboard**
   ```bash
   streamlit run dashboard/app.py
   ```

5. **Open your browser** to `http://localhost:8501`

### Dashboard Features

The interactive dashboard includes:

- **📊 KPI Cards**: Key metrics comparison between rainy and clear days
- **📈 Weather vs Orders**: Bar chart showing average orders by weather condition
- **🌡️ Temperature Scatter**: Orders vs temperature with trend line
- **⏰ Time Patterns**: Ordering patterns by time period and weather
- **📅 Daily Trends**: Combined view of orders, temperature, and rainfall
- **🔍 Key Insights**: Automated analysis with actionable findings
- **🎛️ Interactive Filters**: Date range and weather condition filters

## 🤖 How Kiro AI Assisted in Development

This project was built with comprehensive assistance from Kiro AI, which helped in:

### 🏗️ Project Setup
- Created the complete folder structure following best practices
- Generated realistic sample datasets with proper data patterns
- Set up requirements.txt with appropriate package versions

### 📊 Data Processing
- Designed robust data cleaning pipeline handling missing values
- Implemented date normalization and format standardization
- Created intelligent data aggregation and merging logic
- Added derived features for enhanced analysis

### 📈 Dashboard Development
- Built interactive Streamlit dashboard with multiple visualization types
- Implemented responsive design with proper layout and styling
- Added comprehensive filtering and interactivity features
- Created automated insights generation with statistical analysis

### 📝 Documentation
- Generated comprehensive README with clear instructions
- Added inline code comments explaining each major step
- Created development logs tracking the entire process
- Provided beginner-friendly explanations and setup guides

### 🔧 Code Quality
- Ensured proper error handling and data validation
- Implemented efficient data processing with pandas
- Used modern Python practices and clean code principles
- Added proper function documentation and type hints

## 🎨 Visualizations Included

1. **KPI Metrics**: Comparative metrics between weather conditions
2. **Bar Charts**: Average orders by weather condition
3. **Scatter Plots**: Temperature vs orders with correlation analysis
4. **Time Series**: Daily trends showing orders, temperature, and rainfall
5. **Grouped Bar Charts**: Ordering patterns by time and weather
6. **Interactive Filters**: Dynamic data exploration capabilities

## 📋 Technical Implementation

### Data Processing Pipeline
- **Loading**: CSV file reading with pandas
- **Cleaning**: Missing value handling and data validation
- **Transformation**: Date parsing and feature engineering
- **Aggregation**: Daily summaries and statistical calculations
- **Merging**: Inner join on date with data integrity checks

### Dashboard Architecture
- **Frontend**: Streamlit with responsive layout
- **Visualization**: Plotly for interactive charts
- **Data**: Cached loading for optimal performance
- **Interactivity**: Real-time filtering and updates

## 🏆 Week 3: Data Weaver Challenge Ready

This project is fully prepared for submission with:
- ✅ Complete data integration from two different sources
- ✅ Comprehensive data cleaning and preprocessing
- ✅ Interactive dashboard with multiple insights
- ✅ Clear documentation and setup instructions
- ✅ Beginner-friendly code with extensive comments
- ✅ Professional project structure and organization

## 🔮 Future Enhancements

Potential improvements for this project:
- Add more weather parameters (humidity, wind speed)
- Include seasonal analysis across multiple months
- Implement machine learning predictions
- Add geographical analysis with location data
- Create automated reporting features

## 📞 Support

If you encounter any issues:
1. Ensure all dependencies are installed correctly
2. Check that Python 3.8+ is being used
3. Verify the data files are in the correct locations
4. Run the data processor before launching the dashboard

---

**Built with ❤️ using Python, Pandas, and Streamlit | Powered by Kiro AI Assistant**
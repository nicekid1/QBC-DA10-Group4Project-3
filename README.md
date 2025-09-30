# Basketball Data Analysis Project

A comprehensive basketball statistics analysis tool that crawls data from Basketball Reference, processes it through a MySQL database, and provides analytical insights through Jupyter notebooks.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Data Pipeline](#data-pipeline)
- [Cross-Platform Compatibility](#cross-platform-compatibility)
- [Contributing](#contributing)
- [License](#license)

## Overview

🏀 This project automates the collection, cleaning, and analysis of NBA basketball statistics from [Basketball Reference](https://www.basketball-reference.com). It features a complete data pipeline from web scraping to database storage and analytical visualization.

## Features

✨ **Key Capabilities:**

- **Automated Data Collection**: Web scraping from Basketball Reference
- **Data Cleaning Pipeline**: Automated data cleaning and standardization
- **MySQL Integration**: Structured database storage for efficient querying
- **Player Analysis**: Comprehensive player statistics including:
  - MVP candidates analysis
  - Champion team players
  - Top 50 players rankings
  - Team statistics
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Jupyter Notebook Analysis**: Interactive data exploration and visualization

## Prerequisites

🔧 **System Requirements:**

- Python 3.9 or higher
- MySQL Server (8+ recommended)
- pip package manager
- Git (for cloning the repository)

### Python Dependencies
```bash
selenium=4.34.2
seaborn-qqplot=0.5.0
seaborn=0.12.2
scikit-learn=1.6.1
requests=2.32.4
pandas=2.3.1
numpy=1.26.4
beautifulsoup4=4.13.4
mysql-connector-python=9.3.0
jupyterlab=4.4.7
```

## Installation

📦 **Step-by-step setup:**

1. **Clone the repository**
```bash
git clone https://github.com/nicekid1/QBC-DA10-Group4Project-3.git
cd QBC-DA10-Group4Project-3
```

2. **Create a virtual environment** (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install required packages**
```bash
pip install -r requirements.txt
```

4. **Set up MySQL Database**
   - Install MySQL Server if not already installed


5. **Configure database connection** (see [Configuration](#configuration) section)

## Project Structure

📁 **Directory Layout:**

```
basketball-analysis/
│
├── 📂 data/                      # Data storage directory
│   ├── all_players.csv           # Complete player roster
│   ├── all_teams.csv             # Team information
│   ├── csv_h1_1.csv              # Processed data files
│   ├── csv_h1_2.csv
│   ├── csv_h2_1.csv
│   ├── csv_h2_2.csv
│   ├── csv1_1.csv                # Analysis output files
│   ├── csv2_2.csv
│   ├── csv2_1.csv
│   ├── csv2_2.csv
│   ├── csv3.csv
│   ├── mvp_players.csv           # MVP candidate statistics
│   ├── nba_champs.csv            # Championship team data
│   └── top50_players.csv         # Top 50 players ranking
│
├── 📂 scripts/                   # Data collection scripts
│   ├── 🐍 champ_team_crawler.py  # Scrapes championship team data
│   ├── 🐍 clean_extract.py       # Data cleaning utilities
│   ├── 🐍 mvp_player_crawler.py  # MVP statistics scraper
│   ├── 🐍 player_crawler.py      # Individual player data scraper
│   ├── 🐍 prepare_data.py        # Data preparation pipeline
│   ├── 🐍 team_crawler.py        # Team statistics scraper
│   └── 🐍 top50_player_all.py    # Top 50 players analysis
│
├── 🔥 .gitignore                 # Git ignore file
├── 📊 Analysis.ipynb             # Main analysis notebook
├── 🔧 database_init.json         # Database configuration (create this)
├── 📁 report.pdf                 # Project documentation
├── 🐍 init.py                    # Main initialization script
└── 📝 query_final.sql            # SQL queries for analysis
```

## Configuration

⚙️ **Database Setup:**

### Database Configuration

Create a `database_init.json` file in the project root directory with your MySQL credentials:

```json
{
    "host": "localhost",
    "user": "your_mysql_username",
    "password": "your_mysql_password",
}
```

**⚠️ Important**: This file contains sensitive information and is included in `.gitignore`. Never commit this file to version control.

### Configuration Options

You can modify the following settings in `init.py`:
- Data collection year range
- Player statistics to track
- Team metrics to analyze
- Database table structures

## Usage

🚀 **Running the Project:**

### Initial Setup and Data Collection

1. **Run the initialization script**
```bash
python init.py
```

This script will:
- Check for existing data files
- If data is missing, automatically run all web scrapers
- Clean and prepare the collected data
- Initialize the MySQL database with proper schema
- Generate analysis-ready CSV files

### Data Analysis

2. **Open Jupyter Notebook for analysis**
```bash
jupyter notebook Analyzer_temp_update.ipynb
```

### Manual Data Collection

If you need to run individual scrapers:

```bash
# Collect player data
python scripts/player_crawler.py

# Collect team data
python scripts/team_crawler.py

# Collect MVP data
python scripts/mvp_player_crawler.py

# Collect championship data
python scripts/champ_team_crawler.py

# Collect Top 50 players data
python scripts/top50_player_ali.py
```

## Data Pipeline

🔄 **Processing Flow:**

1. **Data Collection**: Web scrapers collect raw data from Basketball Reference
2. **Data Cleaning**: `clean_extract.py` standardizes and cleans raw data and loads them into MySQL
3. **Database Query**: `prepare_data.py` gets filtered data from MySQL using `query_final.sql`
4. **Analysis Output**: Generates CSV files for visualization
5. **Visualization**: Jupyter notebooks create insights and charts

## Cross-Platform Compatibility

💻 **Operating System Support:**

This project is designed to work across different operating systems:

### Windows
- Use Command Prompt or PowerShell
- Path separators are handled automatically
- Ensure MySQL service is running

### macOS/Linux
- Use Terminal
- May need to use `python3` instead of `python`
- Check MySQL permissions for your user

### Common Issues and Solutions

**MySQL Connection Error**
- Verify MySQL service is running
- Check credentials in `database_init.json`
- Ensure database exists

**Module Import Error**
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

**Data Collection Timeout**
- Check internet connection
- Basketball Reference may have rate limiting
- Try running scrapers individually

## Contributing

🤝 **How to Contribute:**

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to new functions
- Update README for new features
- Test on multiple platforms

## Acknowledgments

🙏 **Credits:**

- Data sourced from [Basketball Reference](https://www.basketball-reference.com)
- Built with Python and MySQL
- Special thanks to all contributors

## Contact

📧 For questions or support, please open an issue on GitHub.

---

**Note**: This project is for educational and analytical purposes. Please respect Basketball Reference's terms of service and rate limits when collecting data.
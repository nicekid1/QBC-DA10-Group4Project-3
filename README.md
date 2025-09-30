# Quera Data Analysis Project

A comprehensive basketball statistics analysis tool that crawls data from Basketball Reference, processes it through a MySQL database, and provides analytical insights through Jupyter notebooks.

## 📋 Table of Contents
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

## 🏀 Overview

This project automates the collection, cleaning, and analysis of NBA basketball statistics from [Basketball Reference](https://www.basketball-reference.com). It features a complete data pipeline from web scraping to database storage and analytical visualization.

## ✨ Features

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

## 🔧 Prerequisites

- Python 3.9
- MySQL Server (8+ recommended)
- pip package manager
- Git (for cloning the repository)

### Python Dependencies
```bash
pandas>=1.3.0
numpy>=1.21.0
requests>=2.26.0
beautifulsoup4>=4.9.3
mysql-connector-python>=8.0.26
jupyter>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
```

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/basketball-analysis.git
cd basketball-analysis
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

## 📁 Project Structure

```
basketball-analysis/
│
├── 📂 data/                      # Data storage directory
│   ├── all_players.csv           # Complete player roster
│   ├── all_teams.csv             # Team information
│   ├── csv_h1_1.csv             # Processed data files
│   ├── csv_h1_2.csv
│   ├── csv_h2_1.csv
│   ├── csv_h2_2.csv
│   ├── csv1.csv                 # Analysis output files
│   ├── csv2.csv
│   ├── csv2_1.csv
│   ├── csv2_2.csv
│   ├── csv3.csv
│   ├── mvp_players.csv          # MVP candidate statistics
│   ├── nba_champs.csv           # Championship team data
│   └── top50_players.csv        # Top 50 players ranking
│
├── 📂 scripts/                   # Data collection scripts
│   ├── 🐍 champ_team_crawler.py # Scrapes championship team data
│   ├── 🐍 clean_extract.py      # Data cleaning utilities
│   ├── 🐍 mvp_player_crawler.py # MVP statistics scraper
│   ├── 🐍 player_crawler.py     # Individual player data scraper
│   ├── 🐍 prepare_data.py       # Data preparation pipeline
│   ├── 🐍 team_crawler.py       # Team statistics scraper
│   └── 🐍 top50_player_all.py   # Top 50 players analysis
│
├── 🔥 .gitignore                # Git ignore file
├── 📊 Analyzer_temp_update.ipynb # Main analysis notebook
├── 🔧 database_init.json        # Database configuration (create this)
├── 📁 explanation311.docx       # Project documentation
├── 🐍 init.py                   # Main initialization script
├── 📝 query_final.sql           # SQL queries for analysis
└── 📊 Visual_and_Statistical_test_functions.ipynb # Visualization tools
```

## ⚙️ Configuration

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

## 🚀 Usage

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
```

## 🔄 Data Pipeline

1. **Data Collection**: Web scrapers collect raw data from Basketball Reference
2. **Data Cleaning**: `clean_extract.py` standardizes and cleans raw data
3. **Database Storage**: `prepare_data.py` loads clean data into MySQL
4. **Query Processing**: `query_final.sql` creates analysis views
5. **Analysis Output**: Generates CSV files for visualization
6. **Visualization**: Jupyter notebooks create insights and charts

## 💻 Cross-Platform Compatibility

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

## 🤝 Contributing

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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Data sourced from [Basketball Reference](https://www.basketball-reference.com)
- Built with Python and MySQL
- Special thanks to all contributors

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This project is for educational and analytical purposes. Please respect Basketball Reference's terms of service and rate limits when collecting data.

# Wespire Report Generator

## Overview

Wespire Report Generator is a web application designed to help sales agents generate clean, professional-looking summary reports for their clients. The app can be run locally and is built using React for the frontend and Django for the backend.

## Features

- **User-friendly Interface:** Easy-to-use interface for generating reports.
- **Data Visualization:** Supports charts and graphs for data representation.
- **Easy Export:** download the report as a PDF file with ease.

## Prerequisites

- **Node.js** (version 14.x or higher)
- **Python** (version 3.8 or higher)
- **Django** (version 3.x or higher)
- **npm** (Node Package Manager)
- **pip** (Python Package Installer)

## Installation

### Backend Setup

1. **Clone the Repository:**

   ```
   git clone https://github.com/yourusername/sales-summary-report-generator.git
   cd sales-summary-report-generator/backend
   ```
2. **Create a Virtual Environment:**
   ```
   python -m venv venv
   ```
3. **Activate the Virtual Environment:**
   - Windows:
   ```
   venv\Scripts\activate
   ```
   - macOS/Linux:
   ```
   source venv/bin/activate
   ```
4. **Install Backend Dependencies:**
   ```
   pip install -r requirements.txt
   ```
5. **Apply Migrations:**
   ```
   python manage.py migrate
   ```
6. **Create a Superuser (optional):**
   ```
   python manage.py createsuperuser
   ```
7. **Run the Backend Server:**
   ```
   python manage.py runserver
   ```
The backend server will start at http://localhost:8000.

### Frontend Setup

1. **Navigate to the Frontend Directory:**
   ```
   cd ../frontend
   ```
2. **Install Frontend Dependencies:**
   ```
   npm install
   ```
3. **Start the Frontend Server:**
   ```
   npm start
   ```
The frontend server will start at http://localhost:3000.


### Usage

1. **Open the Application:**
   Visit http://localhost:3000 in your web browser.
   <img width="1728" alt="image" src="https://github.com/user-attachments/assets/30b6cd40-e088-4c49-80cc-0940678fb485">

3. **Login:**
  Register a new account using your email, or 
	3.	Generate Reports:
	•	Navigate to the “Create Report” section.
	•	Enter the required data and select the desired template.
	•	Preview and export the report.

   

   

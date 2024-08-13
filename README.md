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

2. **Login:**
  Register a new account using your email, or use the details of the superuser to login.

3. **Add a New Client**
   Navigate to the Clients page and add a new client:
   ![image](https://github.com/user-attachments/assets/db39ce0e-ad79-49c7-8443-8b89aa64ec2a)
4. **Generate a Client Report**
   Now, you can select a client you want to create a summary report for and enter the details:
   ![image](https://github.com/user-attachments/assets/553a89d6-6b0d-4023-8514-020e3ccb556d)
5. **View Reports**
   To view a report, navigate to the Summaries page, select a report, and click "Download PDF".
   ![image](https://github.com/user-attachments/assets/2463e665-fce4-47de-8f88-8e708612cc22)

#!/usr/bin/env python3
"""
Student Academic Performance Analyzer
A complete Flask-based web application for analyzing student data
Run with: python app.py
"""

from flask import Flask, render_template_string, request, jsonify, send_file
from flask_cors import CORS
import json
import csv
import io
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Default student data
DEFAULT_DATA = [
    {"id": 101, "name": "Arun", "dept": "CSE", "attendance": 92, "examMarks": 45, "totalMarks": 86},
    {"id": 102, "name": "Priya", "dept": "CSE", "attendance": 95, "examMarks": 47, "totalMarks": 90},
    {"id": 103, "name": "Karthik", "dept": "ECE", "attendance": 78, "examMarks": 38, "totalMarks": 72},
    {"id": 106, "name": "Sneha", "dept": "IT", "attendance": 97, "examMarks": 48, "totalMarks": 93},
    {"id": 107, "name": "Vijay", "dept": "IT", "attendance": 72, "examMarks": 35, "totalMarks": 67},
    {"id": 111, "name": "Manoj", "dept": "CSE", "attendance": 69, "examMarks": 32, "totalMarks": 62}
]

# In-memory storage
student_data = DEFAULT_DATA.copy()

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Academic Performance Analyzer</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
    <style>
        :root {
            --bg-primary: #0f0f0f;
            --bg-secondary: #1a1a1a;
            --bg-tertiary: #242424;
            --bg-hover: #2a2a2a;
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --text-muted: #808080;
            --border-color: #333333;
            --border-light: #404040;
            --accent-primary: #0070f3;
            --accent-hover: #0051cc;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #3b82f6;
            --shadow: rgba(0, 0, 0, 0.5);
            --transition: all 0.3s ease;
        }

        [data-theme="light"] {
            --bg-primary: #ffffff;
            --bg-secondary: #f5f5f5;
            --bg-tertiary: #ebebeb;
            --bg-hover: #e0e0e0;
            --text-primary: #0f0f0f;
            --text-secondary: #4f4f4f;
            --text-muted: #808080;
            --border-color: #e0e0e0;
            --border-light: #d0d0d0;
            --shadow: rgba(0, 0, 0, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            width: 100%;
            height: 100%;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            transition: var(--transition);
        }

        .container {
            display: flex;
            width: 100%;
            height: 100vh;
        }

        .sidebar {
            width: 260px;
            background-color: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            transition: var(--transition);
        }

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 24px 20px;
            border-bottom: 1px solid var(--border-color);
        }

        .brand-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #0070f3, #50e3c2);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: white;
        }

        .brand-text h3 {
            font-size: 16px;
            font-weight: 600;
            margin: 0;
        }

        .brand-text p {
            font-size: 12px;
            color: var(--text-muted);
            margin: 2px 0 0 0;
        }

        .sidebar-nav {
            flex: 1;
            padding: 16px 0;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 20px;
            color: var(--text-secondary);
            text-decoration: none;
            transition: var(--transition);
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
        }

        .nav-item:hover {
            background-color: var(--bg-hover);
            color: var(--text-primary);
        }

        .nav-item.active {
            background-color: var(--bg-tertiary);
            color: var(--accent-primary);
            border-left: 3px solid var(--accent-primary);
            padding-left: 17px;
        }

        .nav-item i {
            width: 20px;
            text-align: center;
        }

        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .header {
            background-color: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            padding: 16px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 16px;
            flex: 1;
        }

        .page-title {
            font-size: 20px;
            font-weight: 600;
            margin: 0;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .search-box {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background-color: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            min-width: 200px;
        }

        .search-box i {
            color: var(--text-muted);
        }

        .search-box input {
            flex: 1;
            background: none;
            border: none;
            color: var(--text-primary);
            font-size: 14px;
            outline: none;
        }

        .search-box input::placeholder {
            color: var(--text-muted);
        }

        .theme-toggle, .refresh-btn {
            background: none;
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            width: 36px;
            height: 36px;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: var(--transition);
            font-size: 16px;
        }

        .theme-toggle:hover, .refresh-btn:hover {
            background-color: var(--bg-hover);
            color: var(--text-primary);
        }

        .section {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
        }

        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }

        .kpi-card {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            display: flex;
            gap: 16px;
            align-items: flex-start;
            transition: var(--transition);
        }

        .kpi-card:hover {
            border-color: var(--border-light);
            box-shadow: 0 4px 12px var(--shadow);
        }

        .kpi-icon {
            width: 48px;
            height: 48px;
            background-color: var(--bg-tertiary);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: var(--accent-primary);
            flex-shrink: 0;
        }

        .kpi-label {
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .kpi-value {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .kpi-sublabel {
            font-size: 12px;
            color: var(--text-secondary);
            margin: 0;
        }

        .filter-section {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 24px;
        }

        .filter-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }

        .filter-header h2 {
            font-size: 16px;
            font-weight: 600;
            margin: 0;
        }

        .filter-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 16px;
        }

        .filter-btn {
            padding: 8px 14px;
            border: 1px solid var(--border-color);
            background-color: var(--bg-tertiary);
            color: var(--text-secondary);
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }

        .filter-btn:hover {
            background-color: var(--bg-hover);
            color: var(--text-primary);
            border-color: var(--border-light);
        }

        .filter-btn.active {
            background-color: var(--accent-primary);
            border-color: var(--accent-primary);
            color: white;
        }

        .sort-section {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .sort-section select {
            padding: 6px 10px;
            background-color: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 13px;
            cursor: pointer;
        }

        .table-container {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            overflow: hidden;
            margin-bottom: 24px;
        }

        .table-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }

        .table-header h2 {
            font-size: 16px;
            font-weight: 600;
            margin: 0;
        }

        .export-btn {
            background-color: var(--accent-primary);
            border: none;
            color: white;
            padding: 8px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .export-btn:hover {
            background-color: var(--accent-hover);
        }

        .table-wrapper {
            overflow-x: auto;
            margin-bottom: 16px;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }

        .data-table thead {
            background-color: var(--bg-tertiary);
            position: sticky;
            top: 0;
        }

        .data-table th {
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: var(--text-secondary);
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            user-select: none;
        }

        .data-table th:hover {
            color: var(--text-primary);
        }

        .data-table td {
            padding: 12px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
        }

        .data-table tbody tr:hover {
            background-color: var(--bg-hover);
        }

        .dept-badge {
            display: inline-block;
            padding: 4px 8px;
            background-color: var(--bg-tertiary);
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            color: var(--accent-primary);
        }

        .attendance-high {
            color: var(--success);
            font-weight: 600;
        }

        .attendance-low {
            color: var(--warning);
            font-weight: 600;
        }

        .exam-pass {
            color: var(--success);
            font-weight: 600;
        }

        .exam-fail {
            color: var(--danger);
            font-weight: 600;
        }

        .chart-container {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 24px;
        }

        .chart-canvas {
            position: relative;
            height: 300px;
            width: 100%;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
        }

        .stat-card {
            background-color: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            display: flex;
            gap: 12px;
            align-items: center;
        }

        .stat-icon {
            width: 36px;
            height: 36px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            color: white;
            flex-shrink: 0;
        }

        .stat-icon.success {
            background-color: rgba(16, 185, 145, 0.2);
            color: var(--success);
        }

        .stat-icon.danger {
            background-color: rgba(239, 68, 68, 0.2);
            color: var(--danger);
        }

        .stat-label {
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
        }

        .stat-value {
            font-size: 20px;
            font-weight: 700;
        }

        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 14px 16px;
            border-radius: 6px;
            font-size: 13px;
            display: none;
            align-items: center;
            gap: 8px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        }

        .toast.show {
            display: flex;
        }

        .toast.success {
            border-left: 3px solid var(--success);
        }

        .toast.error {
            border-left: 3px solid var(--danger);
        }

        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        .upload-section {
            display: none;
            flex-direction: column;
            gap: 16px;
        }

        .upload-section.active {
            display: flex;
        }

        .upload-card {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 32px;
            text-align: center;
        }

        .upload-dropzone {
            border: 2px dashed var(--border-light);
            border-radius: 8px;
            padding: 32px;
            background-color: var(--bg-tertiary);
            cursor: pointer;
            transition: var(--transition);
            margin-bottom: 16px;
        }

        .upload-dropzone:hover {
            border-color: var(--accent-primary);
            background-color: var(--bg-hover);
        }

        .upload-btn {
            background-color: var(--accent-primary);
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
        }

        .upload-btn:hover {
            background-color: var(--accent-hover);
        }

        @media (max-width: 768px) {
            .sidebar {
                position: absolute;
                left: 0;
                top: 0;
                height: 100vh;
                z-index: 500;
                transform: translateX(-100%);
                transition: var(--transition);
            }

            .sidebar.open {
                transform: translateX(0);
            }

            .menu-toggle {
                display: block;
            }

            .kpi-grid {
                grid-template-columns: 1fr;
            }

            .filter-buttons {
                flex-direction: column;
            }

            .filter-btn {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-brand">
                <div class="brand-icon">
                    <i class="fas fa-chart-bar"></i>
                </div>
                <div class="brand-text">
                    <h3>Analytics</h3>
                    <p>Dashboard</p>
                </div>
            </div>

            <nav class="sidebar-nav">
                <a class="nav-item active" onclick="switchSection('dashboard')" data-section="dashboard">
                    <i class="fas fa-home"></i>
                    <span>Dashboard</span>
                </a>
                <a class="nav-item" onclick="switchSection('upload')" data-section="upload">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <span>Upload Data</span>
                </a>
                <a class="nav-item" onclick="switchSection('analytics')" data-section="analytics">
                    <i class="fas fa-chart-line"></i>
                    <span>Analytics</span>
                </a>
                <a class="nav-item" onclick="switchSection('settings')" data-section="settings">
                    <i class="fas fa-cog"></i>
                    <span>Settings</span>
                </a>
            </nav>

            <div style="padding: 16px 20px; border-top: 1px solid var(--border-color);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #0070f3, #50e3c2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 12px;">AD</div>
                    <div>
                        <p style="font-size: 12px; font-weight: 600; margin: 0;">Admin</p>
                        <p style="font-size: 11px; color: var(--text-muted); margin: 0;">Online</p>
                    </div>
                </div>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Header -->
            <header class="header">
                <div class="header-left">
                    <h1 class="page-title">Student Academic Performance</h1>
                </div>

                <div class="header-right">
                    <div class="search-box">
                        <i class="fas fa-search"></i>
                        <input type="text" id="searchInput" placeholder="Search students...">
                    </div>
                    <button class="theme-toggle" id="themeToggle" onclick="toggleTheme()">
                        <i class="fas fa-moon"></i>
                    </button>
                    <button class="refresh-btn" onclick="loadData()">
                        <i class="fas fa-sync-alt"></i>
                    </button>
                </div>
            </header>

            <!-- Dashboard Section -->
            <section id="dashboard" class="section" style="display: block;">
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-icon"><i class="fas fa-users"></i></div>
                        <div>
                            <p class="kpi-label">Total Students</p>
                            <h3 class="kpi-value" id="totalStudents">0</h3>
                            <p class="kpi-sublabel">in current view</p>
                        </div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-icon"><i class="fas fa-pencil-alt"></i></div>
                        <div>
                            <p class="kpi-label">Avg Exam Marks</p>
                            <h3 class="kpi-value" id="avgExamMarks">0</h3>
                            <p class="kpi-sublabel">out of 50</p>
                        </div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-icon"><i class="fas fa-clock"></i></div>
                        <div>
                            <p class="kpi-label">Avg Attendance</p>
                            <h3 class="kpi-value" id="avgAttendance">0</h3>
                            <p class="kpi-sublabel">attendance %</p>
                        </div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-icon"><i class="fas fa-star"></i></div>
                        <div>
                            <p class="kpi-label">Avg Total Marks</p>
                            <h3 class="kpi-value" id="avgTotalMarks">0</h3>
                            <p class="kpi-sublabel">out of 100</p>
                        </div>
                    </div>
                </div>

                <div class="filter-section">
                    <div class="filter-header">
                        <h2>DataFrame Filters</h2>
                    </div>

                    <div class="filter-buttons">
                        <button class="filter-btn active" onclick="applyFilter('all')">
                            <i class="fas fa-check-circle"></i> Show All
                        </button>
                        <button class="filter-btn" onclick="applyFilter('cse')">
                            <i class="fas fa-laptop-code"></i> CSE Only
                        </button>
                        <button class="filter-btn" onclick="applyFilter('highAttendance')">
                            <i class="fas fa-check"></i> High Attendance (>90%)
                        </button>
                        <button class="filter-btn" onclick="applyFilter('needsSupport')">
                            <i class="fas fa-exclamation-circle"></i> Needs Support (<40)
                        </button>
                    </div>

                    <div class="sort-section">
                        <label>Sort By:</label>
                        <select id="sortBy" onchange="applySort()">
                            <option value="name">Name (A-Z)</option>
                            <option value="attendance">Attendance (High to Low)</option>
                            <option value="examMarks">Exam Marks (High to Low)</option>
                            <option value="totalMarks">Total Marks (High to Low)</option>
                        </select>
                    </div>
                </div>

                <div class="table-container">
                    <div class="table-header">
                        <h2>Student Records</h2>
                        <button class="export-btn" onclick="exportCSV()">
                            <i class="fas fa-download"></i> Export CSV
                        </button>
                    </div>

                    <div class="table-wrapper">
                        <table class="data-table" id="dataTable">
                            <thead>
                                <tr>
                                    <th onclick="sortTable('id')">ID</th>
                                    <th onclick="sortTable('name')">Name</th>
                                    <th onclick="sortTable('dept')">Department</th>
                                    <th onclick="sortTable('attendance')">Attendance</th>
                                    <th onclick="sortTable('examMarks')">Exam Marks</th>
                                    <th onclick="sortTable('totalMarks')">Total Marks</th>
                                </tr>
                            </thead>
                            <tbody id="tableBody"></tbody>
                        </table>
                    </div>
                </div>

                <div class="chart-container">
                    <h3 style="margin: 0 0 16px 0;">Performance Comparison</h3>
                    <div class="chart-canvas">
                        <canvas id="performanceChart"></canvas>
                    </div>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon success"><i class="fas fa-arrow-up"></i></div>
                        <div>
                            <p class="stat-label">Highest Marks</p>
                            <p class="stat-value" id="highestMarks">0</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon danger"><i class="fas fa-arrow-down"></i></div>
                        <div>
                            <p class="stat-label">Lowest Marks</p>
                            <p class="stat-value" id="lowestMarks">0</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon" style="background-color: rgba(59, 130, 246, 0.2); color: var(--info);"><i class="fas fa-graduation-cap"></i></div>
                        <div>
                            <p class="stat-label">Pass Rate</p>
                            <p class="stat-value" id="passRate">0%</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Upload Section -->
            <section id="upload" class="section upload-section">
                <div class="upload-card">
                    <div style="font-size: 48px; margin-bottom: 16px;"><i class="fas fa-cloud-upload-alt"></i></div>
                    <h2 style="margin-bottom: 8px;">Upload Dataset</h2>
                    <p style="color: var(--text-secondary); margin-bottom: 24px;">Upload a CSV or JSON file containing student data</p>

                    <div class="upload-dropzone" id="dropzone" ondrop="handleDrop(event)" ondragover="handleDragOver(event)">
                        <i class="fas fa-file-import" style="font-size: 40px; color: var(--accent-primary); margin-bottom: 12px; display: block;"></i>
                        <p>Drag and drop your file here</p>
                        <p style="color: var(--text-muted); margin: 12px 0;">or</p>
                        <button class="upload-btn" onclick="document.getElementById('fileInput').click()">
                            <i class="fas fa-folder-open"></i> Click to Browse
                        </button>
                        <input type="file" id="fileInput" accept=".csv,.json" style="display: none;" onchange="handleFileUpload(event)">
                    </div>

                    <div style="text-align: left; margin-top: 24px;">
                        <h3>Required Columns:</h3>
                        <ul>
                            <li>id - Student ID (number)</li>
                            <li>name - Student Name (text)</li>
                            <li>dept - Department (text)</li>
                            <li>attendance - Attendance % (0-100)</li>
                            <li>examMarks - Exam Marks (0-50)</li>
                            <li>totalMarks - Total Marks (0-100)</li>
                        </ul>

                        <h3 style="margin-top: 16px;">Example CSV:</h3>
                        <pre style="background-color: var(--bg-tertiary); padding: 12px; border-radius: 6px; overflow-x: auto;">id,name,dept,attendance,examMarks,totalMarks
101,Arun,CSE,92,45,86
102,Priya,CSE,95,47,90</pre>
                    </div>
                </div>
            </section>

            <!-- Analytics Section -->
            <section id="analytics" class="section" style="display: none;">
                <div class="chart-container">
                    <h3 style="margin: 0 0 16px 0;">Department Performance</h3>
                    <div class="chart-canvas">
                        <canvas id="deptChart"></canvas>
                    </div>
                </div>

                <div class="chart-container">
                    <h3 style="margin: 0 0 16px 0;">Attendance Distribution</h3>
                    <div class="chart-canvas">
                        <canvas id="attendanceChart"></canvas>
                    </div>
                </div>
            </section>

            <!-- Settings Section -->
            <section id="settings" class="section" style="display: none;">
                <div class="filter-section" style="max-width: 500px;">
                    <h2 style="margin-bottom: 20px;">Settings</h2>

                    <div style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 8px; font-weight: 600;">Pass Threshold (Exam Marks):</label>
                        <input type="number" id="passThreshold" min="0" max="50" value="40" style="width: 100%; padding: 8px; background-color: var(--bg-tertiary); border: 1px solid var(--border-color); border-radius: 6px; color: var(--text-primary);">
                    </div>

                    <div style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 8px; font-weight: 600;">Theme:</label>
                        <select id="themeSelect" onchange="setTheme()" style="width: 100%; padding: 8px; background-color: var(--bg-tertiary); border: 1px solid var(--border-color); border-radius: 6px; color: var(--text-primary);">
                            <option value="dark">Dark Mode</option>
                            <option value="light">Light Mode</option>
                        </select>
                    </div>

                    <button onclick="resetData()" style="width: 100%; padding: 10px; background-color: var(--danger); color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">
                        <i class="fas fa-trash"></i> Reset to Default Data
                    </button>

                    <p style="margin-top: 20px; font-size: 12px; color: var(--text-muted);">
                        <strong>Student Academic Performance Analyzer v1.0</strong><br>
                        Built with Flask + Chart.js<br>
                        All data is processed client-side
                    </p>
                </div>
            </section>
        </main>
    </div>

    <div id="toast" class="toast"></div>

    <script>
        let allData = [];
        let filteredData = [];
        let currentFilter = 'all';
        let chartInstance = null;
        let deptChartInstance = null;
        let attendanceChartInstance = null;
        let passThreshold = 40;

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            loadData();
            initializeEventListeners();
            const savedTheme = localStorage.getItem('theme') || 'dark';
            document.documentElement.setAttribute('data-theme', savedTheme);
            document.getElementById('themeSelect').value = savedTheme;
        });

        function initializeEventListeners() {
            document.getElementById('searchInput').addEventListener('input', function() {
                applyFilters();
                renderTable();
            });
        }

        function loadData() {
            fetch('/api/students')
                .then(r => r.json())
                .then(data => {
                    allData = data;
                    applyFilters();
                    renderDashboard();
                    showToast('Data refreshed', 'success');
                })
                .catch(e => showToast('Error loading data', 'error'));
        }

        function applyFilter(filter) {
            currentFilter = filter;
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.closest('.filter-btn').classList.add('active');
            applyFilters();
            renderDashboard();
        }

        function applyFilters() {
            filteredData = allData.slice();

            switch(currentFilter) {
                case 'cse':
                    filteredData = filteredData.filter(s => s.dept === 'CSE');
                    break;
                case 'highAttendance':
                    filteredData = filteredData.filter(s => s.attendance > 90);
                    break;
                case 'needsSupport':
                    filteredData = filteredData.filter(s => s.examMarks < passThreshold);
                    break;
            }

            const search = document.getElementById('searchInput').value.toLowerCase();
            if (search) {
                filteredData = filteredData.filter(s =>
                    s.name.toLowerCase().includes(search) ||
                    s.dept.toLowerCase().includes(search) ||
                    s.id.toString().includes(search)
                );
            }

            applySort();
        }

        function applySort() {
            const sortBy = document.getElementById('sortBy').value;
            filteredData.sort((a, b) => {
                let aVal = a[sortBy];
                let bVal = b[sortBy];
                if (typeof aVal === 'string') {
                    aVal = aVal.toLowerCase();
                    bVal = bVal.toLowerCase();
                }
                return aVal > bVal ? -1 : 1;
            });
        }

        function sortTable(column) {
            document.getElementById('sortBy').value = column;
            applySort();
            renderTable();
        }

        function renderDashboard() {
            calculateStats();
            renderTable();
            renderPerformanceChart();
        }

        function calculateStats() {
            const total = filteredData.length;
            if (total === 0) {
                document.getElementById('totalStudents').textContent = '0';
                document.getElementById('avgExamMarks').textContent = '0';
                document.getElementById('avgAttendance').textContent = '0';
                document.getElementById('avgTotalMarks').textContent = '0';
                return;
            }

            const avgExam = (filteredData.reduce((s, x) => s + x.examMarks, 0) / total).toFixed(1);
            const avgAtt = (filteredData.reduce((s, x) => s + x.attendance, 0) / total).toFixed(1);
            const avgTotal = (filteredData.reduce((s, x) => s + x.totalMarks, 0) / total).toFixed(1);
            const highest = Math.max(...filteredData.map(x => x.totalMarks));
            const lowest = Math.min(...filteredData.map(x => x.totalMarks));
            const passing = filteredData.filter(x => x.examMarks >= passThreshold).length;
            const passRate = ((passing / total) * 100).toFixed(0);

            document.getElementById('totalStudents').textContent = total;
            document.getElementById('avgExamMarks').textContent = avgExam;
            document.getElementById('avgAttendance').textContent = avgAtt;
            document.getElementById('avgTotalMarks').textContent = avgTotal;
            document.getElementById('highestMarks').textContent = highest;
            document.getElementById('lowestMarks').textContent = lowest;
            document.getElementById('passRate').textContent = passRate + '%';
        }

        function renderTable() {
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';

            filteredData.forEach(student => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${student.id}</td>
                    <td><strong>${student.name}</strong></td>
                    <td><span class="dept-badge">${student.dept}</span></td>
                    <td class="${student.attendance >= 90 ? 'attendance-high' : 'attendance-low'}">${student.attendance}%</td>
                    <td class="${student.examMarks >= passThreshold ? 'exam-pass' : 'exam-fail'}">${student.examMarks}</td>
                    <td>${student.totalMarks}</td>
                `;
            });
        }

        function renderPerformanceChart() {
            const ctx = document.getElementById('performanceChart').getContext('2d');
            if (chartInstance) chartInstance.destroy();

            if (filteredData.length === 0) {
                ctx.fillText('No data to display', 50, 150);
                return;
            }

            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: filteredData.map(s => s.name),
                    datasets: [
                        {
                            label: 'Total Marks',
                            data: filteredData.map(s => s.totalMarks),
                            backgroundColor: '#10b981',
                            borderRadius: 4,
                        },
                        {
                            label: 'Exam Marks',
                            data: filteredData.map(s => s.examMarks),
                            backgroundColor: '#3b82f6',
                            borderRadius: 4,
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, max: 100 }
                    }
                }
            });
        }

        function switchSection(section) {
            document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
            document.getElementById(section).style.display = section === 'upload' ? 'flex' : section === 'analytics' ? 'flex' : 'block';

            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            event.target.closest('.nav-item').classList.add('active');

            if (section === 'analytics') {
                setTimeout(() => renderAnalyticsCharts(), 100);
            }
        }

        function renderAnalyticsCharts() {
            const depts = [...new Set(allData.map(x => x.dept))];
            const deptData = depts.map(d => {
                const students = allData.filter(x => x.dept === d);
                return { dept: d, avg: (students.reduce((s, x) => s + x.totalMarks, 0) / students.length).toFixed(1) };
            });

            const ctx = document.getElementById('deptChart').getContext('2d');
            if (deptChartInstance) deptChartInstance.destroy();
            deptChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: deptData.map(x => x.dept),
                    datasets: [{
                        label: 'Average Marks',
                        data: deptData.map(x => x.avg),
                        backgroundColor: '#50e3c2',
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    scales: { x: { beginAtZero: true, max: 100 } }
                }
            });
        }

        function exportCSV() {
            fetch('/api/export', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(filteredData)
            })
            .then(r => r.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'students.csv';
                a.click();
                showToast('CSV exported', 'success');
            });
        }

        function handleDragOver(e) {
            e.preventDefault();
            e.stopPropagation();
            e.target.style.borderColor = 'var(--accent-primary)';
        }

        function handleDrop(e) {
            e.preventDefault();
            e.stopPropagation();
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                uploadFile(files[0]);
            }
        }

        function handleFileUpload(e) {
            if (e.target.files.length > 0) {
                uploadFile(e.target.files[0]);
            }
        }

        function uploadFile(file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch('/api/upload', {
                method: 'POST',
                body: formData
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    loadData();
                    showToast('Data uploaded successfully', 'success');
                } else {
                    showToast(data.message || 'Upload failed', 'error');
                }
            })
            .catch(e => showToast('Upload error', 'error'));
        }

        function toggleTheme() {
            const current = document.documentElement.getAttribute('data-theme') || 'dark';
            const newTheme = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            document.getElementById('themeToggle').innerHTML = newTheme === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        }

        function setTheme() {
            const theme = document.getElementById('themeSelect').value;
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
        }

        function resetData() {
            if (confirm('Reset to default data?')) {
                fetch('/api/reset', { method: 'POST' })
                    .then(r => r.json())
                    .then(() => {
                        loadData();
                        showToast('Data reset', 'success');
                    });
            }
        }

        function showToast(msg, type = 'info') {
            const toast = document.getElementById('toast');
            toast.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i> ${msg}`;
            toast.className = `toast show ${type}`;
            setTimeout(() => toast.classList.remove('show'), 3000);
        }
    </script>
</body>
</html>
'''

# Routes
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/students')
def get_students():
    return jsonify(student_data)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    global student_data
    
    try:
        file = request.files['file']
        if not file:
            return jsonify({'success': False, 'message': 'No file provided'})

        filename = file.filename.lower()
        
        if filename.endswith('.csv'):
            stream = io.StringIO(file.stream.read().decode('utf-8'))
            reader = csv.DictReader(stream)
            data = list(reader)
            
            # Convert to proper types
            student_data = []
            for row in data:
                student_data.append({
                    'id': int(row['id']),
                    'name': row['name'],
                    'dept': row['dept'],
                    'attendance': int(row['attendance']),
                    'examMarks': int(row['examMarks']),
                    'totalMarks': int(row['totalMarks'])
                })
        
        elif filename.endswith('.json'):
            data = json.loads(file.stream.read().decode('utf-8'))
            if not isinstance(data, list):
                return jsonify({'success': False, 'message': 'JSON must be an array'})
            student_data = data
        
        else:
            return jsonify({'success': False, 'message': 'Only CSV and JSON supported'})
        
        return jsonify({'success': True, 'message': f'Loaded {len(student_data)} records'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/export', methods=['POST'])
def export_data():
    try:
        data = request.json
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=['id', 'name', 'dept', 'attendance', 'examMarks', 'totalMarks'])
        writer.writeheader()
        writer.writerows(data)
        
        output.seek(0)
        return app.response_class(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=students_export.csv'}
        )
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/reset', methods=['POST'])
def reset():
    global student_data
    student_data = DEFAULT_DATA.copy()
    return jsonify({'success': True})

if __name__ == '__main__':
    print('''
    ╔════════════════════════════════════════════════════════════╗
    ║  Student Academic Performance Analyzer                     ║
    ║  Flask Application                                          ║
    ╚════════════════════════════════════════════════════════════╝
    
    🚀 Starting server...
    📊 Open: http://localhost:5000
    
    Features:
    ✅ Real-time filtering & sorting
    ✅ CSV/JSON file upload
    ✅ Data export
    ✅ Interactive charts
    ✅ Dark/Light theme
    ✅ Responsive design
    
    Press Ctrl+C to stop
    ''')
    
    app.run(debug=True, host='0.0.0.0', port=5000)

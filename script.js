// ==================== Global State ====================
let allData = [];
let filteredData = [];
let currentFilter = 'all';
let currentSort = 'name';
let sortOrder = 'asc';
let passThreshold = 40;
let chartInstance = null;
let deptChartInstance = null;
let attendanceChartInstance = null;

// Default student data
const defaultData = [
    { id: 101, name: "Arun", dept: "CSE", attendance: 92, examMarks: 45, totalMarks: 86 },
    { id: 102, name: "Priya", dept: "CSE", attendance: 95, examMarks: 47, totalMarks: 90 },
    { id: 103, name: "Karthik", dept: "ECE", attendance: 78, examMarks: 38, totalMarks: 72 },
    { id: 106, name: "Sneha", dept: "IT", attendance: 97, examMarks: 48, totalMarks: 93 },
    { id: 107, name: "Vijay", dept: "IT", attendance: 72, examMarks: 35, totalMarks: 67 },
    { id: 111, name: "Manoj", dept: "CSE", attendance: 69, examMarks: 32, totalMarks: 62 }
];

// ==================== Initialization ====================
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Load data from localStorage or use default
    const savedData = localStorage.getItem('studentData');
    allData = savedData ? JSON.parse(savedData) : [...defaultData];

    // Load theme preference
    const theme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    updateThemeToggle(theme);

    // Load pass threshold
    passThreshold = parseInt(localStorage.getItem('passThreshold')) || 40;
    document.getElementById('passThreshold').value = passThreshold;

    // Initialize event listeners
    initializeEventListeners();

    // Render initial data
    renderDashboard();
}

function initializeEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', handleNavigation);
    });

    // Filters
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', handleFilter);
    });

    // Sorting
    document.getElementById('sortBy').addEventListener('change', handleSortChange);

    // Table column sorting
    document.querySelectorAll('.data-table .sortable').forEach(th => {
        th.addEventListener('click', handleTableSort);
    });

    // Search
    document.getElementById('searchInput').addEventListener('input', handleSearch);

    // Theme toggle
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
    document.querySelectorAll('input[name="theme"]').forEach(radio => {
        radio.addEventListener('change', handleThemeChange);
    });

    // Refresh button
    document.getElementById('refreshBtn').addEventListener('click', refreshData);

    // Reset filters
    document.getElementById('resetFilters').addEventListener('click', resetAllFilters);

    // File upload
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = dropzone.querySelector('.upload-btn');

    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileUpload);
    dropzone.addEventListener('dragover', handleDragOver);
    dropzone.addEventListener('drop', handleFileDrop);

    // Export
    document.getElementById('exportBtn').addEventListener('click', exportToCSV);

    // Template downloads
    document.getElementById('downloadCSV').addEventListener('click', downloadCSVTemplate);
    document.getElementById('downloadJSON').addEventListener('click', downloadJSONTemplate);

    // Settings
    document.getElementById('saveSettings').addEventListener('click', saveSettings);
    document.getElementById('resetData').addEventListener('click', resetToDefaultData);

    // Menu toggle (mobile)
    document.getElementById('menuToggle').addEventListener('click', toggleSidebar);

    // Modal close
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', closeModal);
    });

    document.getElementById('detailModal').addEventListener('click', function(e) {
        if (e.target === this) closeModal();
    });
}

// ==================== Navigation ====================
function handleNavigation(e) {
    e.preventDefault();
    const section = this.getAttribute('data-section');

    // Update active nav item
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    this.classList.add('active');

    // Show active section
    document.querySelectorAll('.section').forEach(sec => {
        sec.classList.remove('active');
    });
    document.getElementById(section + '-section').classList.add('active');

    // Close sidebar on mobile
    if (window.innerWidth < 768) {
        document.querySelector('.sidebar').classList.remove('open');
    }

    // Render charts for analytics section
    if (section === 'analytics') {
        setTimeout(() => {
            renderDepartmentChart();
            renderAttendanceChart();
        }, 100);
    }
}

function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('open');
}

// ==================== Filtering & Sorting ====================
function handleFilter(e) {
    const filterType = this.getAttribute('data-filter');
    currentFilter = filterType;

    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    this.classList.add('active');

    applyFilters();
    renderDashboard();
}

function applyFilters() {
    filteredData = [...allData];

    // Apply filter
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

    // Apply search if active
    const searchTerm = document.getElementById('searchInput').value;
    if (searchTerm) {
        filteredData = filteredData.filter(s =>
            s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            s.dept.toLowerCase().includes(searchTerm.toLowerCase()) ||
            s.id.toString().includes(searchTerm)
        );
    }

    // Apply sort
    sortData();
}

function handleSortChange(e) {
    currentSort = e.target.value;
    applyFilters();
    renderTable();
}

function handleTableSort(e) {
    const column = this.getAttribute('data-column');
    
    if (currentSort === column) {
        sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort = column;
        sortOrder = 'asc';
    }

    applyFilters();
    renderTable();
}

function sortData() {
    const sortMap = {
        'name': 'name',
        'attendance': 'attendance',
        'examMarks': 'examMarks',
        'totalMarks': 'totalMarks',
        'dept': 'dept'
    };

    const sortKey = sortMap[currentSort] || 'name';

    filteredData.sort((a, b) => {
        let aVal = a[sortKey];
        let bVal = b[sortKey];

        if (typeof aVal === 'string') {
            aVal = aVal.toLowerCase();
            bVal = bVal.toLowerCase();
        }

        if (aVal > bVal) return sortOrder === 'asc' ? 1 : -1;
        if (aVal < bVal) return sortOrder === 'asc' ? -1 : 1;
        return 0;
    });
}

function handleSearch(e) {
    applyFilters();
    renderTable();
}

function resetAllFilters() {
    currentFilter = 'all';
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-filter') === 'all') {
            btn.classList.add('active');
        }
    });
    document.getElementById('searchInput').value = '';
    applyFilters();
    renderDashboard();
    showToast('Filters reset', 'info');
}

// ==================== Rendering ====================
function renderDashboard() {
    calculateStats();
    renderTable();
    renderPerformanceChart();
}

function calculateStats() {
    const total = filteredData.length;
    const avgExam = total > 0 ? (filteredData.reduce((sum, s) => sum + s.examMarks, 0) / total).toFixed(1) : 0;
    const avgAttendance = total > 0 ? (filteredData.reduce((sum, s) => sum + s.attendance, 0) / total).toFixed(1) : 0;
    const avgTotal = total > 0 ? (filteredData.reduce((sum, s) => sum + s.totalMarks, 0) / total).toFixed(1) : 0;

    const highest = total > 0 ? Math.max(...filteredData.map(s => s.totalMarks)) : 0;
    const lowest = total > 0 ? Math.min(...filteredData.map(s => s.totalMarks)) : 0;
    const highestStudent = total > 0 ? filteredData.find(s => s.totalMarks === highest)?.name : '-';
    const lowestStudent = total > 0 ? filteredData.find(s => s.totalMarks === lowest)?.name : '-';
    const passCount = filteredData.filter(s => s.examMarks >= passThreshold).length;
    const passRate = total > 0 ? ((passCount / total) * 100).toFixed(0) : 0;
    const atRisk = filteredData.filter(s => s.examMarks < passThreshold).length;

    // Update KPI cards
    document.getElementById('totalStudents').textContent = total;
    document.getElementById('avgExamMarks').textContent = avgExam;
    document.getElementById('avgAttendance').textContent = avgAttendance;
    document.getElementById('avgTotalMarks').textContent = avgTotal;

    // Update stat cards
    document.getElementById('highestMarks').textContent = highest;
    document.getElementById('highestStudent').textContent = highestStudent;
    document.getElementById('lowestMarks').textContent = lowest;
    document.getElementById('lowestStudent').textContent = lowestStudent;
    document.getElementById('passRate').textContent = passRate + '%';
    document.getElementById('atRisk').textContent = atRisk;
}

function renderTable() {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';

    if (filteredData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 20px; color: var(--text-muted);">No students found</td></tr>';
    }

    filteredData.forEach(student => {
        const row = document.createElement('tr');
        const attendanceClass = student.attendance >= 90 ? 'attendance-high' : 'attendance-low';
        const examClass = student.examMarks >= passThreshold ? 'exam-pass' : 'exam-fail';

        row.innerHTML = `
            <td>${student.id}</td>
            <td><strong>${student.name}</strong></td>
            <td><span class="dept-badge">${student.dept}</span></td>
            <td class="${attendanceClass}">${student.attendance}%</td>
            <td class="${examClass}">${student.examMarks}</td>
            <td>${student.totalMarks}</td>
            <td>
                <button class="action-btn" onclick="showStudentDetails(${student.id})" title="View details">
                    <i class="fas fa-eye"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });

    document.getElementById('recordCount').textContent = `Showing ${filteredData.length} of ${allData.length} records`;
}

function renderPerformanceChart() {
    const ctx = document.getElementById('performanceChart').getContext('2d');

    if (chartInstance) {
        chartInstance.destroy();
    }

    if (filteredData.length === 0) {
        ctx.fillStyle = 'var(--text-muted)';
        ctx.font = '14px -apple-system';
        ctx.textAlign = 'center';
        ctx.fillText('No data to display', ctx.canvas.width / 2, ctx.canvas.height / 2);
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
                    borderSkipped: false,
                },
                {
                    label: 'Exam Marks',
                    data: filteredData.map(s => s.examMarks),
                    backgroundColor: '#3b82f6',
                    borderRadius: 4,
                    borderSkipped: false,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: 'var(--text-secondary)',
                        font: { size: 12 },
                        padding: 16,
                        usePointStyle: true,
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: 'var(--text-muted)',
                        font: { size: 12 }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    }
                },
                x: {
                    ticks: {
                        color: 'var(--text-muted)',
                        font: { size: 12 }
                    },
                    grid: {
                        display: false,
                        drawBorder: false
                    }
                }
            }
        }
    });
}

function renderDepartmentChart() {
    const departments = [...new Set(allData.map(s => s.dept))];
    const deptData = departments.map(dept => {
        const deptStudents = allData.filter(s => s.dept === dept);
        const avgMarks = deptStudents.reduce((sum, s) => sum + s.totalMarks, 0) / deptStudents.length;
        return { dept, avgMarks };
    });

    const ctx = document.getElementById('deptChart').getContext('2d');

    if (deptChartInstance) {
        deptChartInstance.destroy();
    }

    deptChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: deptData.map(d => d.dept),
            datasets: [{
                label: 'Average Total Marks',
                data: deptData.map(d => d.avgMarks),
                backgroundColor: '#50e3c2',
                borderRadius: 4,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: 'var(--text-secondary)', font: { size: 12 } }
                }
            },
            scales: {
                x: {
                    ticks: { color: 'var(--text-muted)', font: { size: 12 } },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                },
                y: {
                    ticks: { color: 'var(--text-muted)', font: { size: 12 } },
                    grid: { display: false }
                }
            }
        }
    });
}

function renderAttendanceChart() {
    const buckets = [
        { range: '0-50%', min: 0, max: 50, count: 0 },
        { range: '50-70%', min: 50, max: 70, count: 0 },
        { range: '70-90%', min: 70, max: 90, count: 0 },
        { range: '90-100%', min: 90, max: 100, count: 0 }
    ];

    allData.forEach(s => {
        const att = s.attendance;
        if (att < 50) buckets[0].count++;
        else if (att < 70) buckets[1].count++;
        else if (att < 90) buckets[2].count++;
        else buckets[3].count++;
    });

    const ctx = document.getElementById('attendanceChart').getContext('2d');

    if (attendanceChartInstance) {
        attendanceChartInstance.destroy();
    }

    attendanceChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: buckets.map(b => b.range),
            datasets: [{
                data: buckets.map(b => b.count),
                backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981'],
                borderColor: 'var(--bg-secondary)',
                borderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: 'var(--text-secondary)', font: { size: 12 }, padding: 16 }
                }
            }
        }
    });
}

// ==================== File Upload ====================
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('dropzone').style.borderColor = 'var(--accent-primary)';
}

function handleFileDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('dropzone').style.borderColor = 'var(--border-light)';

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload({ target: { files } });
    }
}

function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const fileName = file.name.toLowerCase();
    const isCSV = fileName.endsWith('.csv');
    const isJSON = fileName.endsWith('.json');

    if (!isCSV && !isJSON) {
        showToast('Only CSV and JSON files are supported', 'error');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(event) {
        try {
            let data = [];

            if (isCSV) {
                data = parseCSV(event.target.result);
            } else if (isJSON) {
                data = JSON.parse(event.target.result);
            }

            if (!Array.isArray(data)) {
                throw new Error('Data must be an array');
            }

            // Validate data structure
            const required = ['id', 'name', 'dept', 'attendance', 'examMarks', 'totalMarks'];
            const isValid = data.every(row =>
                required.every(field => field in row)
            );

            if (!isValid) {
                throw new Error('Missing required columns: ' + required.join(', '));
            }

            // Convert string numbers to actual numbers
            data = data.map(row => ({
                id: Number(row.id),
                name: String(row.name),
                dept: String(row.dept),
                attendance: Number(row.attendance),
                examMarks: Number(row.examMarks),
                totalMarks: Number(row.totalMarks)
            }));

            allData = data;
            localStorage.setItem('studentData', JSON.stringify(allData));
            applyFilters();
            renderDashboard();
            showToast(`Successfully loaded ${data.length} records`, 'success');

            // Reset file input
            document.getElementById('fileInput').value = '';
        } catch (error) {
            showToast('Error: ' + error.message, 'error');
        }
    };

    reader.readAsText(file);
}

function parseCSV(csv) {
    const lines = csv.trim().split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    const data = [];

    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(v => v.trim());
        const row = {};
        headers.forEach((header, index) => {
            row[header] = values[index];
        });
        data.push(row);
    }

    return data;
}

function downloadCSVTemplate() {
    const csv = `id,name,dept,attendance,examMarks,totalMarks
101,Arun,CSE,92,45,86
102,Priya,CSE,95,47,90
103,Karthik,ECE,78,38,72
106,Sneha,IT,97,48,93
107,Vijay,IT,72,35,67
111,Manoj,CSE,69,32,62`;

    downloadFile(csv, 'students_template.csv', 'text/csv');
    showToast('CSV template downloaded', 'success');
}

function downloadJSONTemplate() {
    const json = JSON.stringify([
        { id: 101, name: "Arun", dept: "CSE", attendance: 92, examMarks: 45, totalMarks: 86 },
        { id: 102, name: "Priya", dept: "CSE", attendance: 95, examMarks: 47, totalMarks: 90 },
        { id: 103, name: "Karthik", dept: "ECE", attendance: 78, examMarks: 38, totalMarks: 72 },
        { id: 106, name: "Sneha", dept: "IT", attendance: 97, examMarks: 48, totalMarks: 93 },
        { id: 107, name: "Vijay", dept: "IT", attendance: 72, examMarks: 35, totalMarks: 67 },
        { id: 111, name: "Manoj", dept: "CSE", attendance: 69, examMarks: 32, totalMarks: 62 }
    ], null, 2);

    downloadFile(json, 'students_template.json', 'application/json');
    showToast('JSON template downloaded', 'success');
}

function exportToCSV() {
    if (filteredData.length === 0) {
        showToast('No data to export', 'error');
        return;
    }

    let csv = 'id,name,dept,attendance,examMarks,totalMarks\n';
    filteredData.forEach(s => {
        csv += `${s.id},${s.name},${s.dept},${s.attendance},${s.examMarks},${s.totalMarks}\n`;
    });

    downloadFile(csv, 'student_data_export.csv', 'text/csv');
    showToast('Data exported as CSV', 'success');
}

function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// ==================== Theme Management ====================
function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = current === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
}

function handleThemeChange(e) {
    applyTheme(e.target.value);
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateThemeToggle(theme);
}

function updateThemeToggle(theme) {
    const toggle = document.getElementById('themeToggle');
    toggle.innerHTML = theme === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    document.getElementById(theme + 'Theme').checked = true;
}

// ==================== Settings Management ====================
function saveSettings() {
    const newThreshold = parseInt(document.getElementById('passThreshold').value);
    if (isNaN(newThreshold) || newThreshold < 0 || newThreshold > 50) {
        showToast('Pass threshold must be between 0 and 50', 'error');
        return;
    }

    passThreshold = newThreshold;
    localStorage.setItem('passThreshold', passThreshold);

    // Update data if needed
    applyFilters();
    renderDashboard();
    showToast('Settings saved successfully', 'success');
}

function resetToDefaultData() {
    if (confirm('Are you sure you want to reset to default data? This cannot be undone.')) {
        allData = [...defaultData];
        localStorage.setItem('studentData', JSON.stringify(allData));
        currentFilter = 'all';
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.getAttribute('data-filter') === 'all') {
                btn.classList.add('active');
            }
        });
        applyFilters();
        renderDashboard();
        showToast('Data reset to default', 'success');
    }
}

function refreshData() {
    applyFilters();
    renderDashboard();
    showToast('Data refreshed', 'success');
}

// ==================== Student Details Modal ====================
function showStudentDetails(id) {
    const student = allData.find(s => s.id === id);
    if (!student) return;

    const examStatus = student.examMarks >= passThreshold ? 
        '<span style="color: var(--success);">✓ Pass</span>' : 
        '<span style="color: var(--danger);">✗ Fail</span>';

    const attendanceStatus = student.attendance >= 90 ? 
        '<span style="color: var(--success);">Excellent</span>' : 
        'Needs Improvement';

    const modal = document.getElementById('detailModal');
    const body = document.getElementById('modalBody');

    body.innerHTML = `
        <h2 style="margin-bottom: 16px;">${student.name}</h2>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
            <div>
                <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 4px;">Student ID</p>
                <p style="font-size: 16px; font-weight: 600;">${student.id}</p>
            </div>
            <div>
                <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 4px;">Department</p>
                <p style="font-size: 16px; font-weight: 600;">${student.dept}</p>
            </div>
        </div>

        <div style="background-color: var(--bg-tertiary); padding: 16px; border-radius: 8px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                <span style="color: var(--text-secondary);">Attendance</span>
                <span style="font-weight: 600;">${student.attendance}%</span>
            </div>
            <div style="width: 100%; height: 4px; background-color: var(--bg-hover); border-radius: 2px; overflow: hidden;">
                <div style="width: ${student.attendance}%; height: 100%; background: linear-gradient(90deg, var(--success), var(--warning));"></div>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); margin-top: 8px; margin-bottom: 0;">Status: ${attendanceStatus}</p>
        </div>

        <div style="background-color: var(--bg-tertiary); padding: 16px; border-radius: 8px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                <span style="color: var(--text-secondary);">Exam Marks</span>
                <span style="font-weight: 600;">${student.examMarks}/50</span>
            </div>
            <div style="width: 100%; height: 4px; background-color: var(--bg-hover); border-radius: 2px; overflow: hidden;">
                <div style="width: ${(student.examMarks/50)*100}%; height: 100%; background: ${student.examMarks >= passThreshold ? 'var(--success)' : 'var(--danger)'};"></div>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); margin-top: 8px; margin-bottom: 0;">Status: ${examStatus}</p>
        </div>

        <div style="background-color: var(--bg-tertiary); padding: 16px; border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                <span style="color: var(--text-secondary);">Total Marks</span>
                <span style="font-weight: 600;">${student.totalMarks}/100</span>
            </div>
            <div style="width: 100%; height: 4px; background-color: var(--bg-hover); border-radius: 2px; overflow: hidden;">
                <div style="width: ${student.totalMarks}%; height: 100%; background: linear-gradient(90deg, var(--info), var(--success));"></div>
            </div>
        </div>
    `;

    modal.classList.add('show');
}

function closeModal() {
    document.getElementById('detailModal').classList.remove('show');
}

// ==================== Notifications ====================
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        info: 'fa-info-circle'
    };

    toast.innerHTML = `<i class="fas ${icons[type]}"></i> ${message}`;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ==================== Window Resize Handler ====================
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        document.querySelector('.sidebar').classList.remove('open');
    }
});

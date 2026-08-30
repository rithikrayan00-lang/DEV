# Student Academic Performance Analyzer 📊

A modern, professional web dashboard for analyzing student academic data with real-time filtering, sorting, visualization, and dataset upload capabilities. Built with vanilla HTML, CSS, and JavaScript.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Size](https://img.shields.io/badge/size-~200KB-orange)

## ✨ Features

### Core Features
- 🎯 **Real-time KPI Cards** - Total Students, Average Exam Marks, Average Attendance, Average Total Marks
- 🔍 **Advanced Filtering** - Filter by department, attendance, exam performance
- 🔄 **Multi-column Sorting** - Sort by any field with ascending/descending order
- 📊 **Interactive Charts** - Bar charts, department comparison, attendance distribution
- 📁 **File Upload** - Support for CSV and JSON dataset formats
- 💾 **Data Export** - Export filtered data as CSV files
- 🌓 **Theme Support** - Dark and light mode with persistent preference storage
- 📱 **Responsive Design** - Fully responsive layout for desktop, tablet, and mobile
- ⚙️ **Customizable Settings** - Adjustable pass threshold and data management

### Advanced Features
- Search functionality across student records
- Student detail modal with progress visualizations
- Real-time statistics and analytics
- Department-wise performance analysis
- Attendance distribution tracking
- Pass/fail rate calculations
- At-risk student identification
- Local data persistence with localStorage
- Toast notifications for user feedback
- Sidebar navigation with section management

## 📁 File Structure

```
student-dashboard/
├── index.html          # Main HTML file with structure
├── style.css           # Complete styling (dark theme)
├── script.js           # JavaScript functionality
└── README.md           # Documentation
```

## 🚀 Quick Start

### Option 1: Direct File Open (No Setup)
Simply open `index.html` in your browser:
```bash
# Windows
double-click index.html

# Mac/Linux
open index.html
# or
firefox index.html
```

### Option 2: Local Server (Recommended)
```bash
# Using Python 3
python -m http.server 8000

# Using Python 2
python -m SimpleHTTPServer 8000

# Using Node.js (with http-server)
npx http-server

# Using PHP
php -S localhost:8000
```

Then open `http://localhost:8000` in your browser.

### Option 3: Deploy Online

#### Deploy to Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Your app will be live at a unique URL
```

#### Deploy to Netlify
```bash
# Option 1: Drag and drop
# Visit https://netlify.com and drag the folder

# Option 2: Using CLI
npm install -g netlify-cli
netlify deploy --prod
```

#### Deploy to GitHub Pages
```bash
# Create repository
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/student-dashboard.git
git push -u origin main

# Enable Pages in repository settings
# Your app will be live at https://yourusername.github.io/student-dashboard
```

## 📖 Usage Guide

### Dashboard Overview
1. **KPI Cards** - Display real-time statistics from filtered data
2. **Filter Controls** - Apply various filters to the dataset
3. **Data Table** - View filtered student records in an interactive table
4. **Charts Section** - Visualize performance data with interactive charts

### Applying Filters

#### Show All
Resets all filters and displays the complete dataset.

#### CSE Students Only
Filters to show only Computer Science and Engineering students.

#### High Attendance (>90%)
Shows students with attendance above 90% threshold.

#### Needs Support (<40)
Identifies students with exam marks below the pass threshold (customizable).

### Sorting Data

1. **Column Header Sorting** - Click any table column header to sort
   - First click: Sort ascending
   - Second click: Sort descending
   - Third click: Sort by different column

2. **Select Dropdown** - Use the "Sort By" dropdown for quick sorting options
   - Name (A-Z)
   - Attendance (High to Low)
   - Exam Marks (High to Low)
   - Total Marks (High to Low)
   - Department

### Searching
Use the search box in the header to find students by:
- Name
- Student ID
- Department

### Uploading Data

#### Supported Formats
- **CSV** - Comma-separated values with headers
- **JSON** - Array of objects with student data

#### Upload Methods
1. **Drag and Drop** - Drag a file onto the dropzone
2. **Click Browse** - Click the upload button to select a file
3. **Download Template** - Use provided templates to format data

#### CSV Format Example
```csv
id,name,dept,attendance,examMarks,totalMarks
101,Arun,CSE,92,45,86
102,Priya,CSE,95,47,90
103,Karthik,ECE,78,38,72
```

#### JSON Format Example
```json
[
  { "id": 101, "name": "Arun", "dept": "CSE", "attendance": 92, "examMarks": 45, "totalMarks": 86 },
  { "id": 102, "name": "Priya", "dept": "CSE", "attendance": 95, "examMarks": 47, "totalMarks": 90 }
]
```

#### Required Columns
- **id** (number) - Unique student identifier
- **name** (text) - Student full name
- **dept** (text) - Department code (CSE, ECE, IT, etc.)
- **attendance** (number) - Attendance percentage (0-100)
- **examMarks** (number) - Exam marks (0-50)
- **totalMarks** (number) - Total marks (0-100)

### Exporting Data
Click the "Export" button to download filtered data as CSV file.

### Analyzing Data

#### KPI Cards
- **Total Students** - Count of students in current view
- **Avg Exam Marks** - Average exam performance
- **Avg Attendance** - Average attendance percentage
- **Avg Total Marks** - Average overall performance

#### Stat Cards
- **Highest Marks** - Student with highest total marks
- **Lowest Marks** - Student with lowest total marks
- **Pass Rate** - Percentage of students passing exams
- **At Risk** - Number of students below pass threshold

#### Performance Chart
- Compares Total Marks vs Exam Marks for each student
- Shows performance patterns and gaps
- Hover for exact values

#### Department Chart
- Shows average performance by department
- Helps identify department-wide trends

#### Attendance Chart
- Distribution of students across attendance ranges
- Visual representation of engagement levels

### Managing Settings

#### Theme
- **Dark Mode** (default) - Easy on the eyes
- **Light Mode** - High contrast option

#### Pass Threshold
- Customizable exam marks threshold (0-50)
- Used for identifying at-risk students
- Affects pass rate calculations

#### Data Management
- **Reset to Default Data** - Restore original dataset
- **Save Settings** - Persist changes

### Keyboard Shortcuts (Planned for v2.0)
- `Ctrl+K` / `Cmd+K` - Open search
- `Esc` - Close modal/sidebar
- `1-4` - Quick filter selection

## 💾 Data Storage

### Local Storage
- Student data is saved in browser's localStorage
- Persists across browser sessions
- Theme preference is saved
- Settings are retained

### Exporting Data
- Export as CSV for backup or analysis
- Download templates for data import

### Browser Compatibility
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🎨 Customization

### Modifying Colors
Edit CSS variables in `style.css`:
```css
:root {
    --accent-primary: #0070f3;    /* Primary accent color */
    --success: #10b981;            /* Success green */
    --danger: #ef4444;             /* Danger red */
    --warning: #f59e0b;            /* Warning amber */
}
```

### Changing Default Data
Edit the `defaultData` array in `script.js`:
```javascript
const defaultData = [
    { id: 101, name: "Student Name", dept: "CSE", attendance: 92, examMarks: 45, totalMarks: 86 },
    // Add more students...
];
```

### Adding New Filters
1. Add filter button in HTML
2. Add filter case in `applyFilters()` function
3. Add event listener to new button

Example:
```javascript
case 'excellent':
    filteredData = filteredData.filter(s => s.totalMarks > 85);
    break;
```

### Customizing Charts
Modify chart configuration in `renderPerformanceChart()` function in `script.js`.

## 🔧 Technical Details

### Dependencies
- **Chart.js** (4.4.1) - Data visualization
- **Font Awesome** (6.4.0) - Icons
- No framework dependencies (pure vanilla JavaScript)

### Browser APIs Used
- localStorage - Data persistence
- FileReader - File upload handling
- Canvas API - Chart rendering
- DOM API - Dynamic content

### Performance Optimizations
- Efficient data filtering and sorting
- Chart reuse with destroy/recreate pattern
- Debounced search functionality
- Responsive grid layouts
- Minimal DOM manipulation

## 🐛 Troubleshooting

### Charts Not Displaying
- Clear browser cache
- Check browser console for errors
- Ensure Chart.js is loaded
- Refresh the page

### Data Not Saving
- Check if localStorage is enabled
- Verify browser storage limits
- Try exporting as CSV backup

### Upload Failures
- Verify file format (CSV or JSON)
- Check required columns exist
- Ensure data types are correct
- Check file size (<5MB)

### Responsive Layout Issues
- Zoom to 100% (Ctrl+0)
- Test in incognito/private mode
- Clear browser cache
- Update browser to latest version

## 📊 Analytics Features

### Dashboard Statistics
- Real-time KPI calculations
- Dynamic stat cards
- Performance metrics
- Pass/fail analysis

### Charts & Visualizations
- Performance comparison bar chart
- Department performance analysis
- Attendance distribution donut chart
- Interactive hover tooltips

### Filters & Search
- Multi-criteria filtering
- Full-text search
- Department filtering
- Performance threshold filtering

## 🔒 Data Privacy & Security

- All data processing happens client-side
- No data sent to external servers
- Data stored only in browser localStorage
- Safe for sensitive student information
- GDPR compliant (no tracking)

## 📱 Responsive Breakpoints

- **Desktop** (>1024px) - Full layout with sidebar
- **Tablet** (768-1024px) - Adjusted grid layouts
- **Mobile** (<768px) - Collapsed sidebar, stacked columns

## 🚀 Future Enhancements (v2.0)

- [ ] Database integration (Firebase/MongoDB)
- [ ] User authentication & roles
- [ ] Export to PDF/Excel
- [ ] Advanced analytics & trends
- [ ] Custom report builder
- [ ] Email notifications
- [ ] Multi-year data comparison
- [ ] Predictive analytics
- [ ] API integration
- [ ] Collaboration features

## 🤝 Contributing

Feel free to:
- Report bugs via GitHub issues
- Suggest features via discussions
- Submit pull requests with improvements
- Share usage examples

## 📄 License

MIT License - Free to use and modify

## 👨‍💻 Author

Built with ❤️ for educational institutions

## 📞 Support

### Common Questions

**Q: Can I add more students?**
A: Yes, upload a CSV/JSON file with additional students

**Q: Is there a maximum number of students?**
A: No limits on the client-side; browser storage can handle thousands

**Q: Can I backup my data?**
A: Yes, use the Export button to download as CSV

**Q: Is my data secure?**
A: Yes, all data stays in your browser; nothing is sent to servers

**Q: Can I use this in production?**
A: Yes, deploy to Vercel, Netlify, or GitHub Pages

## 🎓 Educational Use

Perfect for:
- Academic institutions
- Student performance tracking
- Data analysis learning
- Dashboard development practice
- Educational dashboards

## 📚 Resources

- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)

## 🎉 Getting Started Checklist

- [ ] Download files (index.html, style.css, script.js)
- [ ] Open index.html in browser
- [ ] Explore default student data
- [ ] Try applying filters
- [ ] Sort columns by clicking headers
- [ ] Upload your own CSV/JSON file
- [ ] Customize theme and settings
- [ ] Deploy to your server
- [ ] Share with colleagues!

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Built With:** HTML, CSS, JavaScript, Chart.js

**Made with ❤️ for educators and students worldwide** 🎓

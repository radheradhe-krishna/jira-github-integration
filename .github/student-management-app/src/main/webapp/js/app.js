// Student Management Application - Frontend JavaScript

// API Base URL (adjust based on your servlet configuration)
const API_BASE_URL = '/api/students';

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    loadAllStudents();
    loadStatistics();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Search on Enter key
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchStudents();
        }
    });

    // Close modal when clicking outside
    window.onclick = function(event) {
        const modal = document.getElementById('studentModal');
        if (event.target === modal) {
            closeModal();
        }
    };
}

// Load all students
async function loadAllStudents() {
    try {
        showLoading();
        
        // Simulating API call with dummy data for demo purposes
        // In production, uncomment the fetch call below
        const students = getDummyStudents();
        displayStudents(students);
        
        /* Uncomment for real API call:
        const response = await fetch(API_BASE_URL);
        if (!response.ok) throw new Error('Failed to load students');
        const students = await response.json();
        displayStudents(students);
        */
        
    } catch (error) {
        console.error('Error loading students:', error);
        showError('Failed to load students. Please try again.');
    }
}

// Search students by name
async function searchStudents() {
    const searchTerm = document.getElementById('searchInput').value.trim();
    
    if (!searchTerm) {
        loadAllStudents();
        return;
    }

    try {
        showLoading();
        
        // Simulating search with dummy data
        const allStudents = getDummyStudents();
        const filteredStudents = allStudents.filter(student => 
            student.firstName.toLowerCase().includes(searchTerm.toLowerCase()) ||
            student.lastName.toLowerCase().includes(searchTerm.toLowerCase())
        );
        displayStudents(filteredStudents);
        
        /* Uncomment for real API call:
        const response = await fetch(`${API_BASE_URL}/search?name=${encodeURIComponent(searchTerm)}`);
        if (!response.ok) throw new Error('Search failed');
        const students = await response.json();
        displayStudents(students);
        */
        
    } catch (error) {
        console.error('Error searching students:', error);
        showError('Search failed. Please try again.');
    }
}

// Display students in table
function displayStudents(students) {
    const tbody = document.getElementById('studentsTableBody');
    
    if (!students || students.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="loading">No students found</td></tr>';
        return;
    }

    tbody.innerHTML = students.map(student => `
        <tr>
            <td>${student.id}</td>
            <td><strong>${student.firstName} ${student.lastName}</strong></td>
            <td>${student.email}</td>
            <td>${student.major}</td>
            <td>${getGPABadge(student.gpa)}</td>
            <td>
                <button class="btn btn-info" onclick="viewStudentDetails(${student.id})">
                    View Details
                </button>
            </td>
        </tr>
    `).join('');
}

// Get GPA badge with color coding
function getGPABadge(gpa) {
    let badgeClass = '';
    if (gpa >= 3.7) badgeClass = 'gpa-excellent';
    else if (gpa >= 3.0) badgeClass = 'gpa-good';
    else if (gpa >= 2.5) badgeClass = 'gpa-average';
    else badgeClass = 'gpa-poor';
    
    return `<span class="gpa-badge ${badgeClass}">${gpa.toFixed(2)}</span>`;
}

// View student details in modal
async function viewStudentDetails(studentId) {
    try {
        // Simulating API call with dummy data
        const students = getDummyStudents();
        const student = students.find(s => s.id === studentId);
        
        if (student) {
            displayStudentDetails(student);
        }
        
        /* Uncomment for real API call:
        const response = await fetch(`${API_BASE_URL}/${studentId}`);
        if (!response.ok) throw new Error('Student not found');
        const student = await response.json();
        displayStudentDetails(student);
        */
        
    } catch (error) {
        console.error('Error loading student details:', error);
        showError('Failed to load student details.');
    }
}

// Display student details in modal
function displayStudentDetails(student) {
    const detailsDiv = document.getElementById('studentDetails');
    
    detailsDiv.innerHTML = `
        <div class="detail-item">
            <div class="detail-label">Student ID</div>
            <div class="detail-value">${student.id}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Full Name</div>
            <div class="detail-value">${student.firstName} ${student.lastName}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Email</div>
            <div class="detail-value">${student.email}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Phone</div>
            <div class="detail-value">${student.phone}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Major</div>
            <div class="detail-value">${student.major}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Age</div>
            <div class="detail-value">${student.age} years</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">GPA</div>
            <div class="detail-value">${getGPABadge(student.gpa)}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Enrollment Date</div>
            <div class="detail-value">${student.enrollmentDate}</div>
        </div>
        <div class="detail-item full-width">
            <div class="detail-label">Address</div>
            <div class="detail-value">${student.address}</div>
        </div>
    `;
    
    openModal();
}

// Load statistics
async function loadStatistics() {
    try {
        // Simulating statistics
        const students = getDummyStudents();
        const totalStudents = students.length;
        const averageGPA = students.reduce((sum, s) => sum + s.gpa, 0) / students.length;
        
        document.getElementById('totalStudents').textContent = totalStudents;
        document.getElementById('averageGPA').textContent = averageGPA.toFixed(2);
        
        /* Uncomment for real API call:
        const response = await fetch(`${API_BASE_URL}/stats`);
        if (!response.ok) throw new Error('Failed to load stats');
        const stats = await response.json();
        document.getElementById('totalStudents').textContent = stats.totalStudents;
        document.getElementById('averageGPA').textContent = stats.averageGPA.toFixed(2);
        */
        
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Modal functions
function openModal() {
    document.getElementById('studentModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('studentModal').style.display = 'none';
}

// Utility functions
function showLoading() {
    const tbody = document.getElementById('studentsTableBody');
    tbody.innerHTML = '<tr><td colspan="6" class="loading">Loading students...</td></tr>';
}

function showError(message) {
    const tbody = document.getElementById('studentsTableBody');
    tbody.innerHTML = `<tr><td colspan="6" class="error-message">${message}</td></tr>`;
}

// Dummy data for demonstration (remove in production)
function getDummyStudents() {
    return [
        {
            id: 1,
            firstName: "John",
            lastName: "Doe",
            email: "john.doe@university.edu",
            phone: "555-0101",
            major: "Computer Science",
            age: 20,
            address: "123 Main St, Boston, MA",
            gpa: 3.8,
            enrollmentDate: "2022-09-01"
        },
        {
            id: 2,
            firstName: "Jane",
            lastName: "Smith",
            email: "jane.smith@university.edu",
            phone: "555-0102",
            major: "Business Administration",
            age: 21,
            address: "456 Oak Ave, Cambridge, MA",
            gpa: 3.9,
            enrollmentDate: "2021-09-01"
        },
        {
            id: 3,
            firstName: "Michael",
            lastName: "Johnson",
            email: "m.johnson@university.edu",
            phone: "555-0103",
            major: "Engineering",
            age: 22,
            address: "789 Pine Rd, Somerville, MA",
            gpa: 3.6,
            enrollmentDate: "2020-09-01"
        },
        {
            id: 4,
            firstName: "Emily",
            lastName: "Williams",
            email: "emily.w@university.edu",
            phone: "555-0104",
            major: "Mathematics",
            age: 19,
            address: "321 Elm St, Newton, MA",
            gpa: 3.95,
            enrollmentDate: "2023-09-01"
        },
        {
            id: 5,
            firstName: "David",
            lastName: "Brown",
            email: "david.brown@university.edu",
            phone: "555-0105",
            major: "Physics",
            age: 20,
            address: "654 Maple Dr, Brookline, MA",
            gpa: 3.7,
            enrollmentDate: "2022-09-01"
        },
        {
            id: 6,
            firstName: "Sarah",
            lastName: "Davis",
            email: "sarah.davis@university.edu",
            phone: "555-0106",
            major: "Chemistry",
            age: 21,
            address: "987 Cedar Ln, Quincy, MA",
            gpa: 3.85,
            enrollmentDate: "2021-09-01"
        },
        {
            id: 7,
            firstName: "James",
            lastName: "Miller",
            email: "james.miller@university.edu",
            phone: "555-0107",
            major: "Computer Science",
            age: 23,
            address: "147 Birch Ct, Waltham, MA",
            gpa: 3.4,
            enrollmentDate: "2019-09-01"
        },
        {
            id: 8,
            firstName: "Lisa",
            lastName: "Wilson",
            email: "lisa.wilson@university.edu",
            phone: "555-0108",
            major: "Biology",
            age: 20,
            address: "258 Spruce Way, Medford, MA",
            gpa: 3.75,
            enrollmentDate: "2022-09-01"
        }
    ];
}

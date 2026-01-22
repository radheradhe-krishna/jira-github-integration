# 🎓 Student Management System

A simple web-based student management application built with Java, HTML, CSS, and JavaScript.

## Features

- 📊 View all students in a table format
- 🔍 Search students by name
- 👁️ View detailed student information in a modal
- 📈 Display statistics (total students, average GPA)
- 🎨 Modern, responsive UI with gradient design
- 🏷️ Color-coded GPA badges

## Project Structure

```
student-management-app/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── studentapp/
│   │   │           ├── model/
│   │   │           │   └── Student.java
│   │   │           ├── service/
│   │   │           │   └── StudentService.java
│   │   │           └── servlet/
│   │   │               └── StudentServlet.java
│   │   ├── resources/
│   │   │   ├── application.properties
│   │   │   └── messages.properties
│   │   └── webapp/
│   │       ├── css/
│   │       │   └── styles.css
│   │       ├── js/
│   │       │   └── app.js
│   │       └── index.html
└── README.md
```

## Technologies Used

- **Backend**: Java (Servlet API)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Data Format**: JSON
- **Build Tool**: Maven (recommended)

## Setup Instructions

### Prerequisites

- Java JDK 8 or higher
- Apache Tomcat 8.5+ or any servlet container
- Maven (optional, for building)

### Running the Application

#### Option 1: Using a Servlet Container (Tomcat)

1. Deploy the application to Tomcat's webapps directory
2. Start Tomcat server
3. Access the application at: `http://localhost:8080/student-app/`

#### Option 2: Standalone Demo (No Server Required)

For quick demonstration, simply open `index.html` in a web browser. The application includes dummy data and works without a backend server.

```bash
# Navigate to the webapp directory
cd src/main/webapp

# Open in browser (Windows)
start index.html

# Open in browser (Mac)
open index.html

# Open in browser (Linux)
xdg-open index.html
```

## Configuration

### Application Properties

Edit `src/main/resources/application.properties` to configure:

- Server port
- Database settings (for future database integration)
- Application settings (max records, default values)
- Feature flags

### Messages Properties

Edit `src/main/resources/messages.properties` to customize:

- UI labels and messages
- Error messages
- Button text

## Features Breakdown

### Student Model (`Student.java`)

- Represents student entity with properties: ID, name, email, phone, major, age, address, GPA, enrollment date
- Includes getters, setters, and utility methods

### Student Service (`StudentService.java`)

- Business logic layer
- CRUD operations for students
- Search and filter functionality
- Statistics calculations (total students, average GPA)
- Initialized with 8 dummy students for demonstration

### Student Servlet (`StudentServlet.java`)

- REST API endpoints for student operations
- Endpoints:
  - `GET /api/students` - Get all students
  - `GET /api/students/{id}` - Get student by ID
  - `GET /api/students/search?name={name}` - Search students
  - `GET /api/students/stats` - Get statistics
  - `POST /api/students` - Add new student

### Frontend (`index.html`, `styles.css`, `app.js`)

- Responsive design with gradient theme
- Interactive table with hover effects
- Modal for detailed student view
- Real-time search functionality
- Statistics dashboard
- Color-coded GPA badges:
  - 🟢 Excellent (3.7+)
  - 🔵 Good (3.0-3.69)
  - 🟡 Average (2.5-2.99)
  - 🔴 Poor (<2.5)

## API Usage Examples

### Get All Students

```javascript
GET /api/students
Response: Array of student objects
```

### Get Student by ID

```javascript
GET /api/students/1
Response: Single student object
```

### Search Students

```javascript
GET /api/students/search?name=John
Response: Array of matching students
```

### Get Statistics

```javascript
GET /api/students/stats
Response: {"totalStudents": 8, "averageGPA": 3.74}
```

## Future Enhancements

- [ ] Add database integration (H2, MySQL, PostgreSQL)
- [ ] Implement add/edit/delete student functionality
- [ ] Add authentication and authorization
- [ ] Export students to CSV/PDF
- [ ] Advanced filtering (by major, GPA range, etc.)
- [ ] Pagination for large datasets
- [ ] Student photo uploads
- [ ] Grade management system
- [ ] Course enrollment tracking

## Demo Data

The application comes pre-loaded with 8 dummy students:

- John Doe (Computer Science, GPA: 3.8)
- Jane Smith (Business Administration, GPA: 3.9)
- Michael Johnson (Engineering, GPA: 3.6)
- Emily Williams (Mathematics, GPA: 3.95)
- David Brown (Physics, GPA: 3.7)
- Sarah Davis (Chemistry, GPA: 3.85)
- James Miller (Computer Science, GPA: 3.4)
- Lisa Wilson (Biology, GPA: 3.75)

## License

This is a demo application for educational purposes.

## Author

Created as a demonstration project for learning Java web development.

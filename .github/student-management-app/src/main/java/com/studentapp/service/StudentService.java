package com.studentapp.service;

import com.studentapp.model.Student;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Student Service Class
 * Handles business logic for student operations
 */
public class StudentService {
    
    private static List<Student> students = new ArrayList<>();
    
    // Initialize with some dummy data
    static {
        students.add(new Student(1, "John", "Doe", "john.doe@university.edu", 
                                 "555-0101", "Computer Science", 20, 
                                 "123 Main St, Boston, MA", 3.8, "2022-09-01"));
        
        students.add(new Student(2, "Jane", "Smith", "jane.smith@university.edu", 
                                 "555-0102", "Business Administration", 21, 
                                 "456 Oak Ave, Cambridge, MA", 3.9, "2021-09-01"));
        
        students.add(new Student(3, "Michael", "Johnson", "m.johnson@university.edu", 
                                 "555-0103", "Engineering", 22, 
                                 "789 Pine Rd, Somerville, MA", 3.6, "2020-09-01"));
        
        students.add(new Student(4, "Emily", "Williams", "emily.w@university.edu", 
                                 "555-0104", "Mathematics", 19, 
                                 "321 Elm St, Newton, MA", 3.95, "2023-09-01"));
        
        students.add(new Student(5, "David", "Brown", "david.brown@university.edu", 
                                 "555-0105", "Physics", 20, 
                                 "654 Maple Dr, Brookline, MA", 3.7, "2022-09-01"));
        
        students.add(new Student(6, "Sarah", "Davis", "sarah.davis@university.edu", 
                                 "555-0106", "Chemistry", 21, 
                                 "987 Cedar Ln, Quincy, MA", 3.85, "2021-09-01"));
        
        students.add(new Student(7, "James", "Miller", "james.miller@university.edu", 
                                 "555-0107", "Computer Science", 23, 
                                 "147 Birch Ct, Waltham, MA", 3.4, "2019-09-01"));
        
        students.add(new Student(8, "Lisa", "Wilson", "lisa.wilson@university.edu", 
                                 "555-0108", "Biology", 20, 
                                 "258 Spruce Way, Medford, MA", 3.75, "2022-09-01"));
    }
    
    /**
     * Get all students
     */
    public List<Student> getAllStudents() {
        return new ArrayList<>(students);
    }
    
    /**
     * Get student by ID
     */
    public Student getStudentById(int id) {
        Optional<Student> student = students.stream()
                .filter(s -> s.getId() == id)
                .findFirst();
        return student.orElse(null);
    }
    
    /**
     * Search students by name
     */
    public List<Student> searchStudentsByName(String name) {
        String searchTerm = name.toLowerCase();
        return students.stream()
                .filter(s -> s.getFullName().toLowerCase().contains(searchTerm))
                .collect(Collectors.toList());
    }
    
    /**
     * Get students by major
     */
    public List<Student> getStudentsByMajor(String major) {
        return students.stream()
                .filter(s -> s.getMajor().equalsIgnoreCase(major))
                .collect(Collectors.toList());
    }
    
    /**
     * Add a new student
     */
    public boolean addStudent(Student student) {
        if (student != null && getStudentById(student.getId()) == null) {
            students.add(student);
            return true;
        }
        return false;
    }
    
    /**
     * Update student information
     */
    public boolean updateStudent(Student student) {
        for (int i = 0; i < students.size(); i++) {
            if (students.get(i).getId() == student.getId()) {
                students.set(i, student);
                return true;
            }
        }
        return false;
    }
    
    /**
     * Delete student by ID
     */
    public boolean deleteStudent(int id) {
        return students.removeIf(s -> s.getId() == id);
    }
    
    /**
     * Get total number of students
     */
    public int getTotalStudents() {
        return students.size();
    }
    
    /**
     * Get average GPA of all students
     */
    public double getAverageGPA() {
        return students.stream()
                .mapToDouble(Student::getGpa)
                .average()
                .orElse(0.0);
    }
}

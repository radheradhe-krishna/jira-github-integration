package com.studentapp.model;

import java.io.Serializable;

/**
 * Student Model Class
 * Represents a student entity with basic details
 */
public class Student implements Serializable {
    private static final long serialVersionUID = 1L;
    
    private int id;
    private String firstName;
    private String lastName;
    private String email;
    private String phone;
    private String major;
    private int age;
    private String address;
    private double gpa;
    private String enrollmentDate;
    
    // Default constructor
    public Student() {
    }
    
    // Parameterized constructor
    public Student(int id, String firstName, String lastName, String email, 
                   String phone, String major, int age, String address, 
                   double gpa, String enrollmentDate) {
        this.id = id;
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.phone = phone;
        this.major = major;
        this.age = age;
        this.address = address;
        this.gpa = gpa;
        this.enrollmentDate = enrollmentDate;
    }
    
    // Getters and Setters
    public int getId() {
        return id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    
    public String getFirstName() {
        return firstName;
    }
    
    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }
    
    public String getLastName() {
        return lastName;
    }
    
    public void setLastName(String lastName) {
        this.lastName = lastName;
    }
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        this.email = email;
    }
    
    public String getPhone() {
        return phone;
    }
    
    public void setPhone(String phone) {
        this.phone = phone;
    }
    
    public String getMajor() {
        return major;
    }
    
    public void setMajor(String major) {
        this.major = major;
    }
    
    public int getAge() {
        return age;
    }
    
    public void setAge(int age) {
        this.age = age;
    }
    
    public String getAddress() {
        return address;
    }
    
    public void setAddress(String address) {
        this.address = address;
    }
    
    public double getGpa() {
        return gpa;
    }
    
    public void setGpa(double gpa) {
        this.gpa = gpa;
    }
    
    public String getEnrollmentDate() {
        return enrollmentDate;
    }
    
    public void setEnrollmentDate(String enrollmentDate) {
        this.enrollmentDate = enrollmentDate;
    }
    
    public String getFullName() {
        return firstName + " " + lastName;
    }
    
    @Override
    public String toString() {
        return "Student{" +
                "id=" + id +
                ", name='" + getFullName() + '\'' +
                ", email='" + email + '\'' +
                ", major='" + major + '\'' +
                ", gpa=" + gpa +
                '}';
    }
}

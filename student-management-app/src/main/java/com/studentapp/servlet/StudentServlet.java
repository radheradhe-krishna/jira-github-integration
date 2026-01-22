package com.studentapp.servlet;

import com.studentapp.model.Student;
import com.studentapp.service.StudentService;
import com.google.gson.Gson;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

/**
 * Student Servlet
 * Handles HTTP requests for student operations
 */
@WebServlet("/api/students/*")
public class StudentServlet extends HttpServlet {
    
    private StudentService studentService;
    private Gson gson;
    
    @Override
    public void init() throws ServletException {
        studentService = new StudentService();
        gson = new Gson();
    }
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
        PrintWriter out = response.getWriter();
        
        String pathInfo = request.getPathInfo();
        
        try {
            if (pathInfo == null || pathInfo.equals("/")) {
                // Get all students
                List<Student> students = studentService.getAllStudents();
                String json = gson.toJson(students);
                out.print(json);
                
            } else if (pathInfo.matches("/\\d+")) {
                // Get student by ID
                int id = Integer.parseInt(pathInfo.substring(1));
                Student student = studentService.getStudentById(id);
                
                if (student != null) {
                    String json = gson.toJson(student);
                    out.print(json);
                } else {
                    response.setStatus(HttpServletResponse.SC_NOT_FOUND);
                    out.print("{\"error\": \"Student not found\"}");
                }
                
            } else if (pathInfo.equals("/search")) {
                // Search students by name
                String name = request.getParameter("name");
                List<Student> students = studentService.searchStudentsByName(name);
                String json = gson.toJson(students);
                out.print(json);
                
            } else if (pathInfo.equals("/stats")) {
                // Get statistics
                String stats = String.format(
                    "{\"totalStudents\": %d, \"averageGPA\": %.2f}",
                    studentService.getTotalStudents(),
                    studentService.getAverageGPA()
                );
                out.print(stats);
            }
            
        } catch (Exception e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            out.print("{\"error\": \"" + e.getMessage() + "\"}");
        }
        
        out.flush();
    }
    
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
        PrintWriter out = response.getWriter();
        
        try {
            // Read student data from request body
            Student student = gson.fromJson(request.getReader(), Student.class);
            
            if (studentService.addStudent(student)) {
                response.setStatus(HttpServletResponse.SC_CREATED);
                out.print(gson.toJson(student));
            } else {
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                out.print("{\"error\": \"Failed to add student\"}");
            }
            
        } catch (Exception e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            out.print("{\"error\": \"" + e.getMessage() + "\"}");
        }
        
        out.flush();
    }
}

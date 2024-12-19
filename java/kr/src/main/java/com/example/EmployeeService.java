package com.example;

import org.hibernate.Session;
import org.hibernate.Transaction;
import org.hibernate.query.Query;

import java.time.LocalDate;
import java.util.List;

public class EmployeeService {

    public void addEmployee(Employee employee) {
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            Transaction transaction = session.beginTransaction();
            session.save(employee);
            transaction.commit();
        }
    }

    public Employee findEmployeeById(Long id) {
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            return session.get(Employee.class, id);
        }
    }

    public List<Employee> findEmployeesByName(String firstName) {
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            Query<Employee> query = session.createQuery("FROM Employee WHERE firstName = :firstName", Employee.class);
            query.setParameter("firstName", firstName);
            return query.list();
        }
    }

    public List<Employee> findEmployeesByBirthDate(LocalDate birthDate) {
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            Query<Employee> query = session.createQuery("FROM Employee WHERE birthDate = :birthDate", Employee.class);
            query.setParameter("birthDate", birthDate);
            return query.list();
        }
    }

    public void updateEmployee(Employee employee) {
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            Transaction transaction = session.beginTransaction();
            session.update(employee);
            transaction.commit();
        }
    }

    public void deleteEmployee(Long id) {
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            Transaction transaction = session.beginTransaction();
            Employee employee = session.get(Employee.class, id);
            if (employee != null) {
                session.delete(employee);
            }
            transaction.commit();
        }
    }

    public Double calculateTotalSalary() {
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            Query<Double> query = session.createQuery("SELECT SUM(salary) FROM Employee", Double.class);
            return query.uniqueResult();
        }
    }
}

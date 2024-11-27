package com.example;

import java.sql.*;

public class Main {

    public static void main(String[] args) {
        String url = "jdbc:h2:./moviesdb";
        String username = "sa";
        String password = "";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            System.out.println("Connected to the database.");

            try (Statement statement = connection.createStatement()) {
                statement.execute("DROP TABLE IF EXISTS movies");
                statement.execute("""
                        CREATE TABLE movies (
                            id INT PRIMARY KEY AUTO_INCREMENT,
                            title VARCHAR(255) NOT NULL,
                            genre VARCHAR(50),
                            year INT
                        )
                        """);
                System.out.println("Table 'movies' created.");
            }

            try (PreparedStatement insertStmt = connection.prepareStatement("""
                    INSERT INTO movies (title, genre, year) VALUES (?, ?, ?)
                    """)) {
                insertStmt.setString(1, "Inception");
                insertStmt.setString(2, "Sci-Fi");
                insertStmt.setInt(3, 2010);
                insertStmt.executeUpdate();

                insertStmt.setString(1, "The Godfather");
                insertStmt.setString(2, "Crime");
                insertStmt.setInt(3, 1972);
                insertStmt.executeUpdate();

                insertStmt.setString(1, "The Dark Knight");
                insertStmt.setString(2, "Action");
                insertStmt.setInt(3, 2008);
                insertStmt.executeUpdate();

                insertStmt.setString(1, "Pulp Fiction");
                insertStmt.setString(2, "Crime");
                insertStmt.setInt(3, 1994);
                insertStmt.executeUpdate();

                System.out.println("4 records inserted.");
                printAllMovies(connection);
            }

            try (PreparedStatement updateStmt = connection.prepareStatement("""
                    UPDATE movies SET genre = ? WHERE id = ?
                    """)) {
                updateStmt.setString(1, "Drama");
                updateStmt.setInt(2, 2);
                int rowsUpdated = updateStmt.executeUpdate();
                printAllMovies(connection);
                System.out.println(rowsUpdated + " record(s) updated.");
            }

            try (PreparedStatement deleteStmt = connection.prepareStatement("""
                    DELETE FROM movies WHERE id = ?
                    """)) {
                deleteStmt.setInt(1, 4);
                int rowsDeleted = deleteStmt.executeUpdate();
                printAllMovies(connection);
                System.out.println(rowsDeleted + " record(s) deleted.");
            }

            try (PreparedStatement searchByYearStmt = connection.prepareStatement("""
                    SELECT * FROM movies WHERE year = ?
                    """)) {
                searchByYearStmt.setInt(1, 2010);
                try (ResultSet resultSet = searchByYearStmt.executeQuery()) {
                    System.out.println("");
                    System.out.println("Movies from the year 2010:");
                    while (resultSet.next()) {
                        System.out.println(resultSet.getString("title"));
                    }
                    System.out.println("");
                }
            }

            try (PreparedStatement searchByGenreStmt = connection.prepareStatement("""
                    SELECT * FROM movies WHERE genre = ?
                    """)) {
                searchByGenreStmt.setString(1, "Sci-Fi");
                try (ResultSet resultSet = searchByGenreStmt.executeQuery()) {
                    System.out.println("Sci-Fi movies:");
                    System.out.println("");
                    while (resultSet.next()) {
                        System.out.println(resultSet.getString("title"));
                    }
                    System.out.println("");
                }
            }

            try (PreparedStatement searchByTitleStmt = connection.prepareStatement("""
                    SELECT * FROM movies WHERE title = ?
                    """)) {
                searchByTitleStmt.setString(1, "Inception");
                try (ResultSet resultSet = searchByTitleStmt.executeQuery()) {
                    System.out.println("Search by title 'Inception':");
                    if (resultSet.next()) {
                        System.out.println("Found movie: " + resultSet.getString("title"));
                    } else {
                        System.out.println("No movie found with title 'Inception'.");
                    }
                }
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private static void printAllMovies(Connection connection) {
        try (Statement statement = connection.createStatement();
             ResultSet resultSet = statement.executeQuery("SELECT * FROM movies")) {

            System.out.println("");
            while (resultSet.next()) {
                int id = resultSet.getInt("id");
                String title = resultSet.getString("title");
                String genre = resultSet.getString("genre");
                int year = resultSet.getInt("year");
                System.out.printf("ID: %d, Title: %s, Genre: %s, Year: %d%n", id, title, genre, year);
            }
            System.out.println("");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}

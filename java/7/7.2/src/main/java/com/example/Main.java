package com.example;

import java.util.List;
import java.util.Optional;
import java.sql.*;
import java.util.ArrayList;

class Movie {

    private int id;
    private String title;
    private String genre;
    private int year;

    public Movie(int id, String title, String genre, int year) {
        this.id = id;
        this.title = title;
        this.genre = genre;
        this.year = year;
    }

    // Геттеры и сеттеры
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getGenre() {
        return genre;
    }

    public void setGenre(String genre) {
        this.genre = genre;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    @Override
    public String toString() {
        return "Movie{id=" + id + ", title='" + title + "', genre='" + genre + "', year=" + year + '}';
    }
}


interface MovieDAO {
    void createTable();
    void deleteTable();
    void createMovie(final Movie movie);
    void deleteMovie(int id);
    void updateMoviesTitle(int id, String newTitle);
    Movie findMovieById(int id);
    List<Movie> findByTitle(String title);
    List<Movie> findByGenre(String genre);
    List<Movie> findByYear(int year);
    void printAllMovies();
}

class MovieDAOImpl implements MovieDAO {

    private final Connection connection;

    public MovieDAOImpl(Connection connection) {
        this.connection = connection;
    }

    @Override
    public void createTable() {
        String query = """
                CREATE TABLE IF NOT EXISTS movies (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    title VARCHAR(255) NOT NULL,
                    genre VARCHAR(50),
                    year INT
                )
                """;
        try (Statement statement = connection.createStatement()) {
            statement.execute(query);
            System.out.println("Table 'movies' created.");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void deleteTable() {
        String query = "DROP TABLE IF EXISTS movies";
        try (Statement statement = connection.createStatement()) {
            statement.execute(query);
            System.out.println("Table 'movies' deleted.");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void createMovie(final Movie movie) {
        String query = "INSERT INTO movies (title, genre, year) VALUES (?, ?, ?)";
        try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
            preparedStatement.setString(1, movie.getTitle());
            preparedStatement.setString(2, movie.getGenre());
            preparedStatement.setInt(3, movie.getYear());
            preparedStatement.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void deleteMovie(int id) {
        String query = "DELETE FROM movies WHERE id = ?";
        try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
            preparedStatement.setInt(1, id);
            int rowsDeleted = preparedStatement.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void updateMoviesTitle(int id, String newTitle) {
        String query = "UPDATE movies SET title = ? WHERE id = ?";
        try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
            preparedStatement.setString(1, newTitle);
            preparedStatement.setInt(2, id);
            int rowsUpdated = preparedStatement.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public Movie findMovieById(int id) {
        String query = "SELECT * FROM movies WHERE id = ?";
        try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
            preparedStatement.setInt(1, id);
            try (ResultSet resultSet = preparedStatement.executeQuery()) {
                if (resultSet.next()) {
                    return new Movie(
                            resultSet.getInt("id"),
                            resultSet.getString("title"),
                            resultSet.getString("genre"),
                            resultSet.getInt("year")
                    );
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    public List<Movie> findByTitle(String title) {
        List<Movie> movies = new ArrayList<>();
        String query = "SELECT * FROM movies WHERE title LIKE ?";
        try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
            preparedStatement.setString(1, "%" + title + "%");
            try (ResultSet resultSet = preparedStatement.executeQuery()) {
                while (resultSet.next()) {
                    movies.add(new Movie(
                            resultSet.getInt("id"),
                            resultSet.getString("title"),
                            resultSet.getString("genre"),
                            resultSet.getInt("year")
                    ));
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return movies;
    }

    @Override
    public List<Movie> findByGenre(String genre) {
        List<Movie> movies = new ArrayList<>();
        String query = "SELECT * FROM movies WHERE genre LIKE ?";
        try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
            preparedStatement.setString(1, "%" + genre + "%");
            try (ResultSet resultSet = preparedStatement.executeQuery()) {
                while (resultSet.next()) {
                    movies.add(new Movie(
                            resultSet.getInt("id"),
                            resultSet.getString("title"),
                            resultSet.getString("genre"),
                            resultSet.getInt("year")
                    ));
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return movies;
    }

    @Override
    public List<Movie> findByYear(int year) {
        List<Movie> movies = new ArrayList<>();
        String query = "SELECT * FROM movies WHERE year = ?";
        try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
            preparedStatement.setInt(1, year);
            try (ResultSet resultSet = preparedStatement.executeQuery()) {
                while (resultSet.next()) {
                    movies.add(new Movie(
                            resultSet.getInt("id"),
                            resultSet.getString("title"),
                            resultSet.getString("genre"),
                            resultSet.getInt("year")
                    ));
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return movies;
    }

    @Override
    public void printAllMovies() {
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

public class Main {

    public static void main(String[] args) {
        String url = "jdbc:h2:./moviesdb";
        String username = "sa";
        String password = "";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            System.out.println("Connected to the database.");
            
            MovieDAO movieDAO = new MovieDAOImpl(connection);

            movieDAO.createTable();

            Movie movie1 = new Movie(0, "Inception", "Sci-Fi", 2010);
            movieDAO.createMovie(movie1);
            movieDAO.printAllMovies();

            Movie movie2 = new Movie(0, "The Dark Knight", "Action", 2008);
            movieDAO.createMovie(movie2);
            movieDAO.printAllMovies();

            movieDAO.updateMoviesTitle(1, "Inception: The Beginning");
            movieDAO.printAllMovies();

            movieDAO.findByTitle("Inception").forEach(System.out::println);

            movieDAO.deleteMovie(2);
            movieDAO.printAllMovies();

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}

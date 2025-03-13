package com.example.demo.repository;

import com.example.demo.model.RegisteredUser;
import org.springframework.data.jpa.repository.JpaRepository;

import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.List;

@Repository
public interface RegisteredUserRepository extends JpaRepository<RegisteredUser, Long> {
    Optional<RegisteredUser> findByUsername(String username);
    Optional<RegisteredUser> findById(Long id);
    List<RegisteredUser> findAll();

    @Modifying
    @Query("UPDATE RegisteredUser u SET u.enabled = :enabled WHERE u.id = :id")
    void toggleUserStatus(@Param("id") Long id, @Param("enabled") boolean enabled);

    @Modifying
    @Query("DELETE FROM RegisteredUser u WHERE u.id = :id")
    void deleteUserById(@Param("id") Long id);
}

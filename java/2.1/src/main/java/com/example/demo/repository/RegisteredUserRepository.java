package com.example.demo.repository;

import com.example.demo.model.RegisteredUser;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface RegisteredUserRepository extends JpaRepository<RegisteredUser, Long>
{
    Optional<RegisteredUser> findByUsername(String username);
}

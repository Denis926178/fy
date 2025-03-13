package com.example.demo.repository;

import com.example.demo.model.UserAction;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface UserActionRepository extends JpaRepository<UserAction, Long> {
    List<UserAction> findByUserId(Long userId);
}

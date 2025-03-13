package com.example.demo.service;

import com.example.demo.model.RegisteredUser;
import com.example.demo.repository.RegisteredUserRepository;
import org.springframework.transaction.annotation.Transactional;

import org.springframework.stereotype.Service;
import java.util.Optional;
import java.util.List;

@Service
public class RegisteredUserService
{
    private final RegisteredUserRepository userRepository;

    public RegisteredUserService(RegisteredUserRepository userRepository)
    {
        this.userRepository = userRepository;
    }

    public Optional<RegisteredUser> findByUsername(String username)
    {
        return userRepository.findByUsername(username);
    }

    public RegisteredUser getUserById(Long id) {
        return userRepository.findById(id).orElseThrow(() -> new RuntimeException("User not found"));
    }

    public List<RegisteredUser> getAllUsers() {
        return userRepository.findAll();
    }

    @Transactional
    public void toggleUserStatus(Long id) {
        RegisteredUser user = getUserById(id);
        userRepository.toggleUserStatus(id, !user.isEnabled());
    }

    @Transactional
    public void updateUser(Long id, String username, String role) {
        RegisteredUser user = getUserById(id);

        if (username != null && !username.isEmpty()) {
            user.setUsername(username);
        }
        if (role != null && !role.isEmpty()) {
            user.setRole(role);
        }

        userRepository.save(user);
    }

    @Transactional
    public void addUser(String username, String password, String role) {
        RegisteredUser user = new RegisteredUser();
        user.setUsername(username);
        user.setPassword(password);
        user.setRole(role);
        userRepository.save(user);
    }

    @Transactional
    public void deleteUser(Long id) {
        userRepository.deleteUserById(id);
    }

    @Transactional
    public void saveUser(RegisteredUser user)
    {
        userRepository.save(user);
    }
}

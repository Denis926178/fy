package com.example.demo.service;

import com.example.demo.model.RegisteredUser;
import com.example.demo.repository.RegisteredUserRepository;

import org.springframework.stereotype.Service;
import java.util.Optional;

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

    public void saveUser(RegisteredUser user)
    {
        userRepository.save(user);
    }
}

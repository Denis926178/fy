package com.example.demo.config;

import com.example.demo.model.RegisteredUser;
import com.example.demo.repository.RegisteredUserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {

    private final RegisteredUserRepository registeredUserRepository;
    private final PasswordEncoder passwordEncoder;

    public DataInitializer(RegisteredUserRepository registeredUserRepository, PasswordEncoder passwordEncoder) {
        this.registeredUserRepository = registeredUserRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public void run(String... args) throws Exception {
        if (registeredUserRepository.findByUsername("admin1").isEmpty()) {
            RegisteredUser admin = new RegisteredUser();
            admin.setUsername("admin1");
            admin.setPassword(passwordEncoder.encode("admin123"));
            admin.setRole("ROLE_ADMIN");
            registeredUserRepository.save(admin);
            System.out.println("Администратор создан: admin1 / admin123");
        }
    }
}

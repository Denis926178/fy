package com.example.demo.controller;

import com.example.demo.model.RegisteredUser;
import com.example.demo.service.RegisteredUserService;
import jakarta.validation.Valid;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class AuthController {
    private final RegisteredUserService registeredUserService;
    private final PasswordEncoder passwordEncoder;

    public AuthController(RegisteredUserService registeredUserService, PasswordEncoder passwordEncoder) {
        this.registeredUserService = registeredUserService;
        this.passwordEncoder = passwordEncoder;
    }

    @GetMapping("/")
    public String showHomePage(Model model) {
        return "index";
    }

    @GetMapping("/login")
    public String showLoginPage() {
        System.out.println("Showing login page");
        return "login";
    }

    @GetMapping("/register")
    public String showRegisterPage() {
        return "register";
    }

    @PostMapping("/register")
    public String registerUser(@RequestParam String username, 
                              @RequestParam String password, 
                              Model model) {
        // Проверка на пустые поля
        if (username == null || username.isEmpty() || password == null || password.isEmpty()) {
            model.addAttribute("error", "Имя пользователя и пароль не могут быть пустыми!");
            return "register";
        }

        // Проверка, существует ли пользователь
        if (registeredUserService.findByUsername(username).isPresent()) {
            model.addAttribute("error", "Пользователь уже существует!");
            return "register";
        }

        // Создание нового пользователя
        RegisteredUser user = new RegisteredUser();
        user.setUsername(username);
        user.setPassword(passwordEncoder.encode(password));
        registeredUserService.saveUser(user);

        // Перенаправление на страницу входа
        return "redirect:/login";
    }
}

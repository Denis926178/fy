package com.example.demo.controller;

import com.example.demo.model.RegisteredUser;
import com.example.demo.service.RegisteredUserService;

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
        if (username == null || username.isEmpty() || password == null || password.isEmpty()) {
            model.addAttribute("error", "Имя пользователя и пароль не могут быть пустыми!");
            return "register";
        }

        if (registeredUserService.findByUsername(username).isPresent()) {
            model.addAttribute("error", "Пользователь уже существует!");
            return "register";
        }

        RegisteredUser user = new RegisteredUser();
        user.setUsername(username);
        user.setPassword(passwordEncoder.encode(password));
        registeredUserService.saveUser(user);
    
        return "redirect:/login";
    }
}

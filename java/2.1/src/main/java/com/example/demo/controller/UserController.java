package com.example.demo.controller;

import com.example.demo.model.User;
import com.example.demo.service.UserService;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@Controller
public class UserController
{

    private final UserService userService;

    public UserController(UserService userService)
    {
        this.userService = userService;
    }

    @GetMapping("/index")
    public String showIndexPage(Model model) {
        List<User> users = userService.getAllUsers();
        model.addAttribute("users", users);
        return "index";
    }

    @PostMapping("/add")
    public String addUser(@RequestParam String name, @RequestParam String email, Model model)
    {
        if (name.isEmpty() || email.isEmpty()) {
            model.addAttribute("error", "Имя и email обязательны!");
            return "index";
        }

        User user = new User();
        user.setName(name);
        user.setEmail(email);
        userService.saveUser(user);
        return "redirect:/index";
    }

    @PostMapping("/delete")
    public String deleteUser(@RequestParam Long id)
    {
        userService.deleteUser(id);
        return "redirect:/index";
    }

    @GetMapping("/edit/{id}")
    public String showEditPage(@PathVariable Long id, Model model) {
        Optional<User> userOptional = userService.getUserById(id);
        if (userOptional.isPresent()) {
            model.addAttribute("user", userOptional.get());
            return "edit";
        } else {
            return "redirect:/index";
        }
    }

    @PostMapping("/update")
    public String updateUser(@RequestParam Long id, 
                            @RequestParam String name, 
                            @RequestParam String email, 
                            Model model) {
        Optional<User> userOptional = userService.getUserById(id);
        if (userOptional.isPresent()) {
            User user = userOptional.get();
            user.setName(name);
            user.setEmail(email);
            userService.saveUser(user);
        }
        return "redirect:/index";
    }
}

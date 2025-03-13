package com.example.demo.controller;

import com.example.demo.model.RegisteredUser;
import com.example.demo.model.CurrencyRate;
import com.example.demo.model.UserAction;
import com.example.demo.service.RegisteredUserService;
import com.example.demo.service.UserActionService;
import com.example.demo.service.CurrencyRateService;

import org.springframework.security.crypto.password.PasswordEncoder;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@Controller
@RequestMapping("/admin")
public class AdminController {

    private final RegisteredUserService userService;
    private final UserActionService userActionService;
    private final PasswordEncoder passwordEncoder;
    private final CurrencyRateService currencyRateService;

    public AdminController(
        RegisteredUserService userService,
        UserActionService userActionService,
        CurrencyRateService currencyRateService,
        PasswordEncoder passwordEncoder) {
        this.userService = userService;
        this.userActionService = userActionService;
        this.currencyRateService = currencyRateService;
        this.passwordEncoder = passwordEncoder;
    }
    
    // start init admin-panel pages

    @GetMapping("/panel")
    public String adminPanel(Model model) {
        return "admin-panel";
    }

    @GetMapping("/panel-currency-rates")
    public String adminPanelCurrencyRates(Model model) {
        List<CurrencyRate> currencyRates = currencyRateService.getAllCurrencyRates();
        model.addAttribute("currencyRates", currencyRates);
        return "admin-panel-currency-rates";
    }

    @GetMapping("/panel-users")
    public String adminPanelUsers(Model model) {
        List<RegisteredUser> users = userService.getAllUsers();
        model.addAttribute("users", users);
        return "admin-panel-users";
    }

    // end init admin-panel pages


    // start init add info pages

    @GetMapping("/add-currency-rate")
    public String addCurrencyRateForm() {
        return "add-currency-rate";
    }

    @PostMapping("/add-currency-rate")
    public String addCurrencyRate(@RequestParam String currency, @RequestParam double rate) {
        currencyRateService.addCurrencyRate(currency, rate);
        return "redirect:/admin/panel-currency-rates";
    }

    @GetMapping("/add-user")
    public String addUserForm() {
        return "add-user";
    }

    @PostMapping("/add-user")
    public String addUser(@RequestParam String username, @RequestParam String password, @RequestParam String role) {
        userService.addUser(username, passwordEncoder.encode(password), role);
        return "redirect:/admin/panel-users";
    }

    // end init add info pagees

    // start init edit info pages

    @GetMapping("/edit-currency-rate/{id}")
    public String editCurrencyRateForm(@PathVariable Long id, Model model) {
        CurrencyRate currencyRate = currencyRateService.getCurrencyRateById(id);
        model.addAttribute("currencyRate", currencyRate);
        return "edit-currency-rate";
    }

    @PostMapping("/edit-currency-rate/{id}")
    public String editCurrencyRate(@PathVariable Long id, @RequestParam double rate) {
        currencyRateService.updateCurrencyRate(id, rate);
        return "redirect:/admin/panel-currency-rates";
    }

    @GetMapping("/edit-user/{id}")
    public String editUserForm(@PathVariable Long id, Model model) {
        RegisteredUser user = userService.getUserById(id);
        model.addAttribute("user", user);
        return "edit-user";
    }

    @PostMapping("/edit-user/{id}")
    public String editUser(@PathVariable Long id, @RequestParam String username, @RequestParam String role) {
        userService.updateUser(id, username, role);
        return "redirect:/admin/panel-users";
    }

    @GetMapping("/toggle-user/{id}")
    public String toggleUserStatus(@PathVariable Long id) {
        userService.toggleUserStatus(id);
        return "redirect:/admin/panel-users";
    }

    // end init edit info pages

    // other

    @GetMapping("/view-history/{id}")
    public String viewUserHistory(@PathVariable Long id, Model model) {
        List<UserAction> actions = userActionService.getUserActions(id);
        model.addAttribute("user_actions", actions);
        return "history";
    }

    @GetMapping("/delete-currency-rate/{id}")
    public String deleteCurrencyRate(@PathVariable Long id) {
        currencyRateService.deleteCurrencyRate(id);
        return "redirect:/admin/panel-currency-rates";
    }
}

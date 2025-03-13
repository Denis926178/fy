package com.example.demo.controller;

import com.example.demo.model.UserAction;
import com.example.demo.service.UserActionService;
import com.example.demo.model.RegisteredUser;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class HistoryController {

    @Autowired
    private UserActionService userActionService;

    @GetMapping("/history")
    public String showHistory(@AuthenticationPrincipal RegisteredUser user, Model model) {
        if (user != null) {
            List<UserAction> userActions = userActionService.getUserActions(user.getId());
            model.addAttribute("user_actions", userActions);
        }
        return "history";
    }
}

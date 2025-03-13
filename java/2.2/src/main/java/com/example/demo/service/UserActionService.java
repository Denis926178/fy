package com.example.demo.service;

import com.example.demo.model.RegisteredUser;
import com.example.demo.model.UserAction;
import com.example.demo.repository.UserActionRepository;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class UserActionService {

    private final UserActionRepository userActionRepository;
    private final ObjectMapper objectMapper;

    public UserActionService(UserActionRepository userActionRepository, ObjectMapper objectMapper) {
        this.userActionRepository = userActionRepository;
        this.objectMapper = objectMapper;
    }

    public void logCurrencyConversion(
        RegisteredUser user,
        String fromCurrency,
        String toCurrency,
        double amount,
        String result) {
        try {
            ObjectNode details = objectMapper.createObjectNode();

            details.put("fromCurrency", fromCurrency);
            details.put("toCurrency", toCurrency);
            details.put("amount", amount);
            details.put("result", result);

            String detailsString = objectMapper.writeValueAsString(details);
           
            UserAction action = new UserAction();

            action.setUser(user);
            action.setActionType("CURRENCY_CONVERSION");
            action.setDetails(detailsString);
            action.setCreatedAt(LocalDateTime.now());

            userActionRepository.save(action);

        } catch (Exception e) {
            throw new RuntimeException("Failed to log user action", e);
        }
    }

    public void logOhmLawCalculation(
        RegisteredUser user,
        Double voltage,
        Double current,
        Double resistance,
        String result) {
        try {
            ObjectNode details = objectMapper.createObjectNode();
    
            if (voltage != null) details.put("voltage", voltage);
            if (current != null) details.put("current", current);
            if (resistance != null) details.put("resistance", resistance);
            details.put("result", result);

            String detailsString = objectMapper.writeValueAsString(details);
           
            UserAction action = new UserAction();

            action.setUser(user);
            action.setActionType("OHM_LAW_CALCULATION");
            action.setDetails(detailsString);
            action.setCreatedAt(LocalDateTime.now());

            userActionRepository.save(action);

        } catch (Exception e) {
            throw new RuntimeException("Failed to log user action", e);
        }
    }

    public List<UserAction> getUserActions(Long userId) {
        return userActionRepository.findByUserId(userId);
    }
}

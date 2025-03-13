package com.example.demo.controller;

import com.example.demo.model.CurrencyRate;
import com.example.demo.service.CurrencyRateService;
import com.example.demo.service.UserActionService;
import com.example.demo.model.RegisteredUser;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.security.core.annotation.AuthenticationPrincipal;

import java.util.Comparator;
import java.util.List;

import jakarta.servlet.http.HttpSession;

@Controller
public class UserController {

    @Autowired
    private CurrencyRateService currencyRateService;

    @Autowired
    private UserActionService userActionService;

    @GetMapping("/currency-converter")
    public String showCurrencyConverterPage(HttpSession session, Model model) {
        String fromCurrency = (String) session.getAttribute("fromCurrency");
        String toCurrency = (String) session.getAttribute("toCurrency");
        Double amount = (Double) session.getAttribute("amount");

        model.addAttribute("fromCurrency", fromCurrency);
        model.addAttribute("toCurrency", toCurrency);
        model.addAttribute("amount", amount);

        List<CurrencyRate> currencies = currencyRateService.getAllCurrencyRates();
        currencies.sort(Comparator.comparing(CurrencyRate::getCurrency));
        model.addAttribute("currency_rates", currencies);

        return "currency-converter";
    }

    @GetMapping("/ohm-law")
    public String showOhmLawPage(HttpSession session, Model model) {
        model.addAttribute("voltage", session.getAttribute("voltage"));
        model.addAttribute("current", session.getAttribute("current"));
        model.addAttribute("resistance", session.getAttribute("resistance"));
        return "ohm-law";
    }

    @PostMapping("/convert")
        public String convertCurrency(
            @RequestParam String fromCurrency,
            @RequestParam String toCurrency,
            @RequestParam double amount,
            @AuthenticationPrincipal RegisteredUser user,
            HttpSession session,
            Model model) {
        double result;

        try {
            result = currencyRateService.convert(fromCurrency, toCurrency, amount);
            String formattedResult = String.format("%.2f", result);
            model.addAttribute("result", formattedResult);

            userActionService.logCurrencyConversion(user, fromCurrency, toCurrency, amount, formattedResult);

        } catch (IllegalArgumentException e) {
            model.addAttribute("error", e.getMessage());
        }

        session.setAttribute("fromCurrency", fromCurrency);
        session.setAttribute("toCurrency", toCurrency);
        session.setAttribute("amount", amount);

        return showCurrencyConverterPage(session, model);
    }

    @PostMapping("/ohm-calculate")
    public String calculateOhmLaw(
            @RequestParam(required = false) Double voltage,
            @RequestParam(required = false) Double current,
            @RequestParam(required = false) Double resistance,
            @AuthenticationPrincipal RegisteredUser user,
            HttpSession session,
            Model model) {
        int filledFields = 0;
        if (voltage != null) filledFields++;
        if (current != null) filledFields++;
        if (resistance != null) filledFields++;

        if (filledFields != 2) {
            model.addAttribute("error", "Необходимо заполнить ровно два поля для расчета.");
            return showOhmLawPage(session, model);
        }

        session.setAttribute("voltage", voltage);
        session.setAttribute("current", current);
        session.setAttribute("resistance", resistance);

         try {
            String result = null;
            if (voltage != null && current != null) {
                // Расчет сопротивления: R = U / I
                double calculatedResistance = voltage / current;
                session.setAttribute("resistance", calculatedResistance);
                result = String.format("Сопротивление: %.2f Ом", calculatedResistance);
                model.addAttribute("result", result);
            } else if (voltage != null && resistance != null) {
                // Расчет силы тока: I = U / R
                double calculatedCurrent = voltage / resistance;
                session.setAttribute("current", calculatedCurrent);
                result = String.format("Сила тока: %.2f А", calculatedCurrent);
                model.addAttribute("result", result);
            } else if (current != null && resistance != null) {
                // Расчет напряжения: U = I * R
                double calculatedVoltage = current * resistance;
                session.setAttribute("voltage", calculatedVoltage);
                result = String.format("Напряжение: %.2f В", calculatedVoltage);
                model.addAttribute("result", result);
            }

            userActionService.logOhmLawCalculation(user, voltage, current, resistance, result);
        } catch (Exception e) {
            model.addAttribute("error", "Ошибка при расчете: " + e.getMessage());
        }

        return showOhmLawPage(session, model);
    }
}

package com.example.demo.service;

import com.example.demo.model.CurrencyRate;
import com.example.demo.repository.CurrencyRateRepository;
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@Service
public class CurrencyRateService {

    private final CurrencyRateRepository currencyRateRepository;

    @Autowired
    public CurrencyRateService(CurrencyRateRepository currencyRateRepository) {
        this.currencyRateRepository = currencyRateRepository;
    }

    public double convert(String fromCurrency, String toCurrency, double amount) {
        CurrencyRate fromRate = currencyRateRepository.findByCurrency(fromCurrency)
            .orElseThrow(() -> new RuntimeException("Курс для валюты " + fromCurrency + " не найден"));
        CurrencyRate toRate = currencyRateRepository.findByCurrency(toCurrency)
            .orElseThrow(() -> new RuntimeException("Курс для валюты " + toCurrency + " не найден"));

        double result = amount * (toRate.getRate() / fromRate.getRate());
        return result;
    }

    public CurrencyRate getCurrencyRateById(Long id) {
        CurrencyRate currencyRate = currencyRateRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Currency rate not found"));

        return currencyRate;
    }

    public List<CurrencyRate> getAllCurrencyRates() {
        return currencyRateRepository.findAll();
    }

    public void addCurrencyRate(String currency, double rate) {
        CurrencyRate currencyRate = new CurrencyRate();
        currencyRate.setCurrency(currency);
        currencyRate.setRate(rate);
        currencyRateRepository.save(currencyRate);
    }

    public void updateCurrencyRate(Long id, double rate) {
        CurrencyRate currencyRate = currencyRateRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Currency rate not found"));
        currencyRate.setRate(rate);
        currencyRateRepository.save(currencyRate);
    }

    public void deleteCurrencyRate(Long id) {
        currencyRateRepository.deleteById(id);
    }
}

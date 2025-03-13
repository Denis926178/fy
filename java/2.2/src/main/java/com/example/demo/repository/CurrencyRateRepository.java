package com.example.demo.repository;

import com.example.demo.model.CurrencyRate;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;
import java.util.List;

public interface CurrencyRateRepository extends JpaRepository<CurrencyRate, Long> {
    Optional<CurrencyRate> findByCurrency(String currency);
    Optional<CurrencyRate> findById(Long id);

    List<CurrencyRate> findAll();
}

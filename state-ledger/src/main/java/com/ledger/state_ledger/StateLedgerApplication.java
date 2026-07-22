package com.ledger.state_ledger;

import com.ledger.state_ledger.model.StateBlock;
import com.ledger.state_ledger.repository.LedgerRepository;
import com.ledger.state_ledger.util.HashUtils;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.Optional;

@SpringBootApplication
public class StateLedgerApplication {

    public static void main(String[] args) {
        SpringApplication.run(StateLedgerApplication.class, args);
    }

    @Bean
    public CommandLineRunner testLedgerPipeline(LedgerRepository repository) {
        return args -> {
            System.out.println("--- TESTING SPRING DATA JPA LEDGER ---");

            // 1. Fetch latest block or assign genesis hash
            Optional<StateBlock> latestBlock = repository.findLatestBlock();
            String previousHash = latestBlock.map(StateBlock::getCurrentHash)
                    .orElse("0000000000000000000000000000000000000000000000000000000000000000");

            // 2. Mock payload
            String actionIntent = "{\"action\": \"INITIALIZE_AGENT\", \"version\": \"1.0\"}";
            String executionResult = "{\"status\": \"READY\"}";

            // 3. Hash calculation
            String currentHash = HashUtils.calculateSHA256(previousHash, actionIntent, executionResult);

            // 4. Save block to PostgreSQL
            StateBlock newBlock = new StateBlock(previousHash, currentHash, actionIntent, executionResult);
            StateBlock savedBlock = repository.save(newBlock);

            System.out.println("Successfully inserted Block ID: " + savedBlock.getBlockId());
            System.out.println("Computed SHA-256 Hash: " + savedBlock.getCurrentHash());
            System.out.println("-------------------------------------");
        };
    }
}
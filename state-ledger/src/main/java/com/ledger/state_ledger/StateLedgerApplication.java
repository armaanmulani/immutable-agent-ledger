package com.ledger.state_ledger;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ledger.state_ledger.model.ActionIntent;
import com.ledger.state_ledger.model.ExecutionResult;
import com.ledger.state_ledger.model.StateBlock;
import com.ledger.state_ledger.model.SystemContext;
import com.ledger.state_ledger.repository.LedgerRepository;
import com.ledger.state_ledger.util.HashUtils;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.Map;
import java.util.Optional;

@SpringBootApplication
public class StateLedgerApplication {

    public static void main(String[] args) {
        SpringApplication.run(StateLedgerApplication.class, args);
    }

    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper();
    }

    // Explicitly define the ObjectMapper bean for dependency injection
    @Bean
    CommandLineRunner testLedgerPipeline(LedgerRepository ledgerRepository, ObjectMapper objectMapper) {
        return args -> {
            ActionIntent intent = new ActionIntent("SEARCH", Map.of("query", "test query"));
            SystemContext context = new SystemContext("development", "test_session_01");
            ExecutionResult executionResult = new ExecutionResult("SUCCESS");

            Optional<StateBlock> latestBlock = ledgerRepository.findLatestBlock();
            String previousHash = latestBlock.map(StateBlock::getCurrentHash)
                    .orElse("0000000000000000000000000000000000000000000000000000000000000000");

            String intentJson = objectMapper.writeValueAsString(intent);
            String executionResultJson = objectMapper.writeValueAsString(executionResult);

            // HashUtils expects Strings for hashing
            String currentHash = HashUtils.calculateSHA256(previousHash, intentJson, executionResultJson);

            // StateBlock takes the ExecutionResult object for the jsonb column
            StateBlock block = new StateBlock(previousHash, currentHash, intent, context, executionResult);
            StateBlock saved = ledgerRepository.save(block);

            System.out.println("Successfully inserted Block ID: " + saved.getBlockId());
            System.out.println("Computed SHA-256 Hash: " + saved.getCurrentHash());
        };
    }
}
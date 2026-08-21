package com.ledger.state_ledger.controller;

import com.ledger.state_ledger.model.ActionIntent;
import com.ledger.state_ledger.model.ExecutionResult; // Make sure this is imported
import com.ledger.state_ledger.model.StateBlock;
import com.ledger.state_ledger.model.SystemContext;
import com.ledger.state_ledger.repository.LedgerRepository;
import com.ledger.state_ledger.service.GatekeeperService;
import com.ledger.state_ledger.util.HashUtils;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/ledger")
public class LedgerController {

    private final LedgerRepository ledgerRepository;
    private final GatekeeperService gatekeeperService;
    private final ObjectMapper objectMapper;

    public LedgerController(LedgerRepository ledgerRepository, GatekeeperService gatekeeperService, ObjectMapper objectMapper) {
        this.ledgerRepository = ledgerRepository;
        this.gatekeeperService = gatekeeperService;
        this.objectMapper = objectMapper;
    }

    @GetMapping("/latest")
    public ResponseEntity<?> getLatestBlock() {
        Optional<StateBlock> latest = ledgerRepository.findLatestBlock();
        if (latest.isPresent()) {
            return ResponseEntity.ok(latest.get());
        }
        return ResponseEntity.status(404).body(Map.of("error", "Ledger is empty."));
    }

    @PostMapping("/commit")
    public ResponseEntity<?> commitBlock(@RequestBody Map<String, Object> payload) {
        try {
            // Map JSON fragments to strongly-typed objects
            ActionIntent actionIntent = objectMapper.convertValue(payload.get("action_intent"), ActionIntent.class);
            SystemContext systemContext = objectMapper.convertValue(payload.get("system_context"), SystemContext.class);

            // Convert execution_result to our ExecutionResult object instead of a raw String
            ExecutionResult executionResult = objectMapper.convertValue(payload.get("execution_result"), ExecutionResult.class);

            // Run through Gatekeeper validation
            gatekeeperService.validateActionIntent(actionIntent);

            // Get previous hash
            Optional<StateBlock> latestBlock = ledgerRepository.findLatestBlock();
            String previousHash = latestBlock.map(StateBlock::getCurrentHash)
                    .orElse("0000000000000000000000000000000000000000000000000000000000000000");

            // Calculate new hash (serialize objects back to strings for hashing consistency)
            String actionIntentJson = objectMapper.writeValueAsString(actionIntent);
            String executionResultJson = objectMapper.writeValueAsString(executionResult);
            String currentHash = HashUtils.calculateSHA256(previousHash, actionIntentJson, executionResultJson);

            // Save to database (passing the ExecutionResult object)
            StateBlock newBlock = new StateBlock(previousHash, currentHash, actionIntent, systemContext, executionResult);
            StateBlock savedBlock = ledgerRepository.save(newBlock);

            return ResponseEntity.ok(savedBlock);

        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("status", "REJECTED", "reason", e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("status", "REJECTED", "reason", "Malformed JSON payload: " + e.getMessage()));
        }
    }
}
package com.ledger.state_ledger.model;

import jakarta.persistence.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.OffsetDateTime;

@Entity
@Table(name = "ledger_blocks")
public class StateBlock {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "block_id")
    private Long blockId;

    @Column(name = "timestamp", insertable = false, updatable = false)
    private OffsetDateTime timestamp;

    @Column(name = "previous_hash", nullable = false)
    private String previousHash;

    @Column(name = "current_hash", nullable = false)
    private String currentHash;

    // Tell Hibernate to cast Java String to PostgreSQL JSONB
    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "action_intent", columnDefinition = "jsonb", nullable = false)
    private String actionIntent;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "execution_result", columnDefinition = "jsonb")
    private String executionResult;

    @Column(name = "status", nullable = false)
    private String status = "COMMITTED";

    public StateBlock() {}

    public StateBlock(String previousHash, String currentHash, String actionIntent, String executionResult) {
        this.previousHash = previousHash;
        this.currentHash = currentHash;
        this.actionIntent = actionIntent;
        this.executionResult = executionResult;
    }

    // Getters and Setters
    public Long getBlockId() { return blockId; }
    public String getPreviousHash() { return previousHash; }
    public String getCurrentHash() { return currentHash; }
    public String getActionIntent() { return actionIntent; }
    public String getExecutionResult() { return executionResult; }
    public String getStatus() { return status; }
}
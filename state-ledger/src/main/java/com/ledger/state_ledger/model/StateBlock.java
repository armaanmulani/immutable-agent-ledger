package com.ledger.state_ledger.model;

import jakarta.persistence.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import org.springframework.data.domain.Persistable;
import java.time.OffsetDateTime;

@Entity
@Table(name = "ledger_blocks")
public class StateBlock implements Persistable<Long> {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "block_id")
    private Long blockId;

    @Column(name = "timestamp", insertable = false, updatable = false)
    private OffsetDateTime timestamp;

    @Column(name = "previous_hash", nullable = false, updatable = false)
    private String previousHash;

    @Column(name = "current_hash", nullable = false, updatable = false)
    private String currentHash;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "action_intent", columnDefinition = "jsonb", nullable = false, updatable = false)
    private ActionIntent actionIntent;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "system_context", columnDefinition = "jsonb", updatable = false)
    private SystemContext systemContext;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "execution_result", columnDefinition = "jsonb", updatable = false)
    private ExecutionResult executionResult;

    @Column(name = "status", nullable = false, updatable = false)
    private String status = "COMMITTED";

    @Transient
    private boolean isNew = true;

    public StateBlock() {}

    // Constructor updated to accept ExecutionResult object
    public StateBlock(String previousHash, String currentHash, ActionIntent actionIntent, SystemContext systemContext, ExecutionResult executionResult) {
        this.previousHash = previousHash;
        this.currentHash = currentHash;
        this.actionIntent = actionIntent;
        this.systemContext = systemContext;
        this.executionResult = executionResult;
        this.isNew = true;
    }

    @Override
    public Long getId() {
        return blockId;
    }

    @Override
    public boolean isNew() {
        return isNew;
    }

    @PostPersist
    @PostLoad
    public void markNotNew() {
        this.isNew = false;
    }

    // Getters
    public Long getBlockId() { return blockId; }
    public OffsetDateTime getTimestamp() { return timestamp; }
    public String getPreviousHash() { return previousHash; }
    public String getCurrentHash() { return currentHash; }
    public ActionIntent getActionIntent() { return actionIntent; }
    public SystemContext getSystemContext() { return systemContext; }
    public ExecutionResult getExecutionResult() { return executionResult; }
    public String getStatus() { return status; }
}
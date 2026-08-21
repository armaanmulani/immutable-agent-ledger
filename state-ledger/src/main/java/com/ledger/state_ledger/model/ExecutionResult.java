package com.ledger.state_ledger.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Objects;

public class ExecutionResult {
    @JsonProperty("status")
    private String status;

    public ExecutionResult() {}

    public ExecutionResult(String status) {
        this.status = status;
    }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ExecutionResult that = (ExecutionResult) o;
        return Objects.equals(status, that.status);
    }

    @Override
    public int hashCode() {
        return Objects.hash(status);
    }
}
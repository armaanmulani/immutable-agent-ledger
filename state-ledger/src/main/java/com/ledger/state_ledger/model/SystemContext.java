package com.ledger.state_ledger.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class SystemContext {

    @JsonProperty("environment")
    private String environment;

    @JsonProperty("session_id")
    private String sessionId;

    public SystemContext() {}

    public SystemContext(String environment, String sessionId) {
        this.environment = environment;
        this.sessionId = sessionId;
    }

    public String getEnvironment() {
        return environment;
    }

    public void setEnvironment(String environment) {
        this.environment = environment;
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }
}
package com.ledger.state_ledger.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Map;

public class ActionIntent {

    @JsonProperty("action_type")
    private String actionType;

    @JsonProperty("parameters")
    private Map<String, Object> parameters;

    public ActionIntent() {}

    public ActionIntent(String actionType, Map<String, Object> parameters) {
        this.actionType = actionType;
        this.parameters = parameters;
    }

    public String getActionType() {
        return actionType;
    }

    public void setActionType(String actionType) {
        this.actionType = actionType;
    }

    public Map<String, Object> getParameters() {
        return parameters;
    }

    public void setParameters(Map<String, Object> parameters) {
        this.parameters = parameters;
    }
}
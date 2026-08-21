package com.ledger.state_ledger.service;

import com.ledger.state_ledger.model.ActionIntent;
import org.springframework.stereotype.Service;

@Service
public class GatekeeperService {

    public void validateActionIntent(ActionIntent actionIntent) {
        if (actionIntent == null) {
            throw new IllegalArgumentException("Validation Error: Action intent payload cannot be null.");
        }

        String actionType = actionIntent.getActionType();
        if (actionType == null || actionType.isBlank()) {
            throw new IllegalArgumentException("Validation Error: Missing required field 'action_type'.");
        }

        if (actionIntent.getParameters() == null) {
            throw new IllegalArgumentException("Validation Error: Missing required field 'parameters'.");
        }

        if (!actionType.equals("SEARCH") && !actionType.equals("EXECUTE") && !actionType.equals("TERMINATE")) {
            throw new IllegalArgumentException("Validation Error: Unauthorized action type '" + actionType + "'.");
        }
    }
}
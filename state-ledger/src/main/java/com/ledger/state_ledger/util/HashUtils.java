package com.ledger.state_ledger.util;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

public class HashUtils {

    public static String calculateSHA256(String previousHash, String actionIntent, String executionResult) {
        try {
            String rawData = previousHash + "|" + actionIntent + "|" + (executionResult != null ? executionResult : "");
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] encodedHash = digest.digest(rawData.getBytes(StandardCharsets.UTF_8));

            StringBuilder hexString = new StringBuilder(2 * encodedHash.length);
            for (byte b : encodedHash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (Exception e) {
            throw new RuntimeException("Error computing cryptographic hash", e);
        }
    }
}
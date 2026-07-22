package com.ledger.state_ledger.repository;

import com.ledger.state_ledger.model.StateBlock;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface LedgerRepository extends JpaRepository<StateBlock, Long> {

    // Custom query to fetch the latest committed block
    @Query(value = "SELECT * FROM ledger_blocks ORDER BY block_id DESC LIMIT 1", nativeQuery = true)
    Optional<StateBlock> findLatestBlock();
}
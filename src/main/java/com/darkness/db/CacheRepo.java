package com.darkness.db;

import org.springframework.data.repository.CrudRepository;
import java.util.Optional;

public interface CacheRepo extends CrudRepository<CacheDB, Integer> {
    Optional<CacheDB> findByMapName(String mapName);
}

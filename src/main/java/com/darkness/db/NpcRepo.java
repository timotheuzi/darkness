package com.darkness.db;

import org.springframework.data.repository.CrudRepository;
import java.util.List;

public interface NpcRepo extends CrudRepository<NpcDB, Integer> {
    NpcDB findByName(String name);
    List<NpcDB> findByLocation(Integer location);
    
    List<NpcDB> findByLocationAndHpGreaterThan(Integer location, Integer hp);
}

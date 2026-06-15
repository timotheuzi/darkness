package com.darkness.db;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import java.util.List;

public interface UserRepo extends CrudRepository<UserDB, Integer> {
    UserDB findByName(String name);
    List<UserDB> findByLocation(Integer location);
    
    @Query("SELECT u FROM UserDB u WHERE u.online = 1")
    List<UserDB> findAllOnline();

    @Query("SELECT u FROM UserDB u WHERE u.online = 1 AND u.location = ?1")
    List<UserDB> findOnlineInLocation(Integer location);
}

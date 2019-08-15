package com.darkness.db;

import org.springframework.data.repository.CrudRepository;

import com.darkness.db.userDB;
 
public interface userRepo extends CrudRepository<userDB, Integer> 
{
	Boolean findIfUserExists(String name);
	userDB findByName(String name);
	userDB findByLocation(Integer location);
}
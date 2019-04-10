package com.darkness.db;

import org.springframework.data.repository.CrudRepository;

import com.darkness.db.cacheDB;
 
public interface cacheRepo extends CrudRepository<cacheDB, Integer> 
{
	cacheDB findById(int intValue);
}
package com.darkness.db;

import java.util.Optional;

import org.springframework.data.repository.CrudRepository;

import com.darkness.db.mapDB;
 
public interface mapRepo extends CrudRepository<mapDB, Integer> 
{
	//mapDB findByName(String name);

	//Optional<mapDB> findById(Integer intValue);
}
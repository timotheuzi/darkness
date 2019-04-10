package com.darkness.db;

import org.springframework.data.repository.CrudRepository;

import com.darkness.db.npcDB;
 
public interface npcRepo extends CrudRepository<npcDB, Integer> 
{
	npcDB findByName(String name);
	npcDB findByLocation(Integer location);
}